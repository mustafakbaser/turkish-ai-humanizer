#!/usr/bin/env python3
"""
analiz.py: Türkçe metinlerde yapay zekâ yazım imzalarını ölçer.

Bu araç bir "AI detektörü" DEĞİLDİR ve ticari detektörlerin skorunu tahmin
etmez. Yeniden yazımı yönlendirmek için açıklanabilir ve tekrarlanabilir
sinyaller üretir: cümle ritmi, çeviri kalıpları, ek yükü, geçiş ifadeleri,
noktalama, belge yapısı ve gizli karakterler.

Yalnızca Python standart kütüphanesini kullanır (3.9+).

Kullanım:
    python3 analiz.py metin.txt
    python3 analiz.py - < metin.txt
    python3 analiz.py metin.txt --uslup akademik
    python3 analiz.py once.txt --karsilastir sonra.txt
    python3 analiz.py --karsilastir - < ikisi.txt   # kaynak ve taslak tek akışta,
                                                    # "===TASLAK===" satırıyla ayrılır
    python3 analiz.py - --profil < ornekler.txt
    python3 analiz.py metin.txt --json
    python3 analiz.py metin.txt --esik 40      # puan 40'ı aşarsa çıkış kodu 1
    python3 analiz.py --kaliplar               # kalıp sözlüğünü listeler
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

SURUM = "1.0.1"
GUVEN_KELIME = 100   # bu sınırın altında puan "düşük güvenli" sayılır
GUVEN_CUMLE = 5
UZUNLUK_TOLERANSI = 0.20  # SKILL.md'deki ±%20 kuralı
AYRAC = "===TASLAK==="     # --karsilastir - kipinde kaynak ile taslağı ayıran satır
AZAMI_KARAKTER = 400_000   # daha uzun belgeler bölüm bölüm ölçülür
KISA_METIN_TABANI = 60     # kalıp yoğunluğu puanlanırken payda en az bu kadar kelime sayılır
KALIP_DOSYASI = Path(__file__).resolve().with_name("kaliplar.json")

# Üslup profilleri. Eşikler sezgiseldir; tests/fixtures üzerinde ayarlanmıştır.
#   cv_hedef:          bu değerin üstündeki cümle uzunluğu varyasyonu "doğal" sayılır
#   mektedir_tolerans: cümle başına kabul edilen -mekte/-makta oranı
#   gecis_carpani:     resmi geçişle açılan cümle cezasının çarpanı
#   adfiil_esik:       100 kelimede kabul edilen -ma/-me ad-fiil sayısı
#   kategori_carpani:  kalıp kategorilerinin bu üsluptaki ağırlık çarpanı
USLUPLAR: Dict[str, Dict] = {
    "genel": dict(cv_hedef=0.50, mektedir_tolerans=0.10, gecis_carpani=1.0,
                  adfiil_esik=4.0, kategori_carpani={}),
    "resmi": dict(cv_hedef=0.35, mektedir_tolerans=0.45, gecis_carpani=0.4,
                  adfiil_esik=8.0,
                  kategori_carpani={"gecis": 0.4, "burokratik": 0.3}),
    "akademik": dict(cv_hedef=0.40, mektedir_tolerans=0.35, gecis_carpani=0.7,
                     adfiil_esik=7.0,
                     kategori_carpani={"gecis": 0.7, "burokratik": 0.6}),
    "profesyonel": dict(cv_hedef=0.45, mektedir_tolerans=0.10, gecis_carpani=1.0,
                        adfiil_esik=4.5, kategori_carpani={}),
    "gazetecilik": dict(cv_hedef=0.45, mektedir_tolerans=0.10, gecis_carpani=1.0,
                        adfiil_esik=4.5, kategori_carpani={}),
    "deneme": dict(cv_hedef=0.55, mektedir_tolerans=0.05, gecis_carpani=1.2,
                   adfiil_esik=3.5, kategori_carpani={}),
    "edebi": dict(cv_hedef=0.55, mektedir_tolerans=0.0, gecis_carpani=1.2,
                  adfiil_esik=3.0, kategori_carpani={}),
}

# Cümle başında "resmi geçiş" sayılan ifadeler. Doğal bağlaçlar (ama, oysa,
# üstelik, çünkü, hatta, zaten...) bilinçli olarak listede yok.
RESMI_GECISLER: Tuple[str, ...] = (
    "bunun yanı sıra", "bunların yanı sıra", "buna ek olarak", "bunlara ek olarak",
    "ek olarak", "öte yandan", "diğer taraftan", "diğer yandan", "bununla birlikte",
    "bununla beraber", "sonuç olarak", "özetle", "kısacası", "dolayısıyla",
    "bu nedenle", "bu sebeple", "bu bağlamda", "bu çerçevede", "bu doğrultuda",
    "bu noktada", "bu kapsamda", "son olarak", "ilk olarak", "öncelikle",
    "aynı zamanda", "nihayetinde", "buna karşın", "buna rağmen", "ayrıca", "her şeyden önce",
)

# Raporlarda gösterilen Türkçe adlar (JSON anahtarları ASCII kalır).
BILESEN_ADLARI = {"kalip": "kalıp", "ritim": "ritim", "ekler": "ekler", "gecis": "geçiş",
                  "noktalama": "noktalama", "yapi": "yapı"}
KATEGORI_ADLARI = {"asistan": "asistan", "sablon": "şablon", "ceviri": "çeviri", "abarti": "abartı",
                   "dolgu": "dolgu", "gecis": "geçiş", "retorik": "retorik", "burokratik": "bürokratik"}

# Cümle başında bu ifadelerden sonra virgül, İngilizce "However," alışkanlığıdır.
_ACILIS_VIRGUL = re.compile(
    r"^(ayrıca|ancak|fakat|bu nedenle|sonuç olarak|bununla birlikte|öte yandan|"
    r"dolayısıyla|özetle|kısacası|yine de|bu bağlamda|bunun yanı sıra|"
    r"buna ek olarak|son olarak|ilk olarak|nihayetinde|"
    r"bu doğrultuda|bu noktada|öncelikle|aynı zamanda|her şeyden önce)\s*,"
)

# Ses kartında sayılan söylem belirteçleri.
SOYLEM_BELIRTECLERI: Tuple[str, ...] = (
    "de", "da", "bile", "zaten", "hani", "işte", "yani", "aslında", "artık",
    "galiba", "herhalde", "sanki", "meğer", "oysa", "hâlbuki", "halbuki",
    "üstelik", "hatta", "ama", "ancak", "fakat", "çünkü", "zira", "ki",
    "belki", "hele", "bari", "nitekim", "şimdi", "ise",
)

# Gündelik sözcüklerle çakışanlar (gör, yön, tel, sok, av...) bilinçli olarak yok.
_KISALTMALAR = {
    "vb", "vs", "dr", "prof", "doç", "yrd", "örn", "bkz", "sf", "yy", "müh",
    "uzm", "çev", "sn", "bşk", "gnl", "mah", "cad", "apt", "ltd", "şti",
    "a.ş", "m.ö", "m.s", "krş",
}

# ------------------------------------------------------------------ desenler

_KELIME = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*|\d+(?:[.,]\d+)*")
_SINIR = re.compile(r"([.!?…]+)([\"'”’»)\]]*)(\s+)")
_KOD_BLOGU = re.compile(r"```.*?```|~~~.*?~~~", re.S)
_SATIR_ICI_KOD = re.compile(r"`[^`\n]+`")
_MD_BAGLANTI_HEDEF = re.compile(r"\]\([^()\[\]\n]{0,2000}\)")
_URL = re.compile(r"https?://\S+|www\.\S+")
_HTML = re.compile(r"<[^<>\n]{1,500}>")
_ALINTI_SATIRI = re.compile(r"^\s*>.*$", re.M)
# Satır içi doğrudan alıntılar başkasının sözüdür: kalıp taramasına girmez (ritim ölçümüne girer).
# Yalnızca bir söyleme fiiline ya da iki noktaya bağlı tırnaklar alıntı sayılır. Böylece metnin
# kendi cümlesini tırnağa almak kalıpları gizlemez.
_SATIR_ICI_ALINTI = re.compile(r'"[^"\n]{1,300}"|“[^”\n]{1,300}”|«[^»\n]{1,300}»')
_ALINTI_SONRASI = re.compile(
    r"\s*[,.]?\s*(diye|dedi|diyor|der\b|demiş|dediği|diyerek|söyle|sor|yaz|belirt|açıkla|ifade|"
    r"vurgula|ekle|aktar|şeklinde|sözler|ifadesi|cevab|yanıt|uyar|haykır|fısılda)")
_ALINTI_ONCESI = re.compile(r"(:|\bdedi ki|\bşöyle dedi|\bşunları söyledi)\s*$")

_BASLIK = re.compile(r"^\s{0,3}#{1,6}\s")
_TABLO = re.compile(r"^\s*\|")
_YATAY_CIZGI = re.compile(r"^\s*([-*_]\s*){3,}$")
_ETIKET_SATIRI = re.compile(r"^\s*(#[^\s#]+\s*)+$")
_EMOJI_SINIFI = "☀-➿\U0001F300-\U0001FAFF⭐⬆↔-⇿"
_EMOJI = re.compile(f"[{_EMOJI_SINIFI}]")
_LISTE_ISARETI_ZORUNLU = re.compile(r"^\s*(?:[-*+•▪◦]|\d+[.)]|[a-zçğıöşü][.)])\s+")
_EMOJI_MADDE = re.compile(rf"^\s*[{_EMOJI_SINIFI}]")
_KALIN_MADDE = re.compile(
    rf"^\s*(?:(?:[-*+•]|\d+[.)]|[{_EMOJI_SINIFI}]️?)\s*)?\*\*[^*\n]{{1,80}}\*\*\s*[:：]|"
    rf"^\s*(?:(?:[-*+•]|\d+[.)]|[{_EMOJI_SINIFI}]️?)\s*)?\*\*[^*\n]{{1,80}}[:：]\*\*"
)
_GORUNMEZ = re.compile("[​-‏‪-‮⁠-⁤﻿­]")
_SAYI = re.compile(r"%?\d+(?:[.,]\d+)*")

_MEKTEDIR = re.compile(r"(?:mekte|makta)(?:d[ıi]r(?:lar|ler)?|y[ıi]z|s[ıi]n[ıi]z|y[ıi]m|ler|lar)?$")
_KOPULA = re.compile(r"(?:d|t)[ıiuü]r(?:lar|ler)?$")
_EBILIR = re.compile(r"\w{2,}[ae]bil(?:ir|ece|iyor|mekte|meli)\w*$")
_ADFIIL = re.compile(r"\w{2,}m[ae]s[ıi](?:n[ıi]n|n[ae]|n[ıi]|nd[ae]n?|yl[ae]|d[ıi]r)?$")
_ADFIIL_ISTISNA = ("kelime", "tema", "sinema", "firma", "forma", "pijama", "drama", "panorama",
                   "dama", "lama", "prim", "kurma", "sima", "isim", "kama", "yama", "ekme")
_UCLU = re.compile(r"(?<![^\W\d_])[^\W\d_]+,\s+[^\W\d_]+\s+ve\s+[^\W\d_]+")
_TIRE_ARA_SOZ = re.compile(r"(?<=[^\W\d_])\s[-–]\s(?=[a-zçğıöşüâîû])")


# ---------------------------------------------------------------- yardımcılar

_ASCII_KATLA = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiuCGIOSUAIU")
_TR_HARF = re.compile("[çğıöşüÇĞİÖŞÜ]")


def ascii_yazilmis(metin: str) -> bool:
    """Türkçe harfler kullanılmadan yazılmış ("onemli bir rol") uzunca bir metin mi?"""
    return len(kelimeler(metin)) >= 20 and not _TR_HARF.search(metin)


def tr_kucuk(metin: str) -> str:
    """Türkçeye uygun küçük harf dönüşümü (I→ı, İ→i)."""
    return metin.replace("I", "ı").replace("İ", "i").lower()


def normallestir(metin: str) -> str:
    metin = unicodedata.normalize("NFC", metin)
    return metin.replace("\r\n", "\n").replace("\r", "\n")


def _bosalt(m: "re.Match[str]") -> str:
    return re.sub(r"[^\n]", " ", m.group(0))


def alintilari_maskele(maskeli: str) -> str:
    """Söyleme fiiline ya da iki noktaya bağlı satır içi alıntıları boşlukla örter."""
    def degistir(m: "re.Match[str]") -> str:
        once = maskeli[max(0, m.start() - 20):m.start()]
        sonra = tr_kucuk(maskeli[m.end():m.end() + 30])
        if _ALINTI_ONCESI.search(once) or _ALINTI_SONRASI.match(sonra):
            return _bosalt(m)
        return m.group(0)
    return _SATIR_ICI_ALINTI.sub(degistir, maskeli)


def maskele(metin: str) -> str:
    """Kod, bağlantı, HTML ve blok alıntıları aynı uzunlukta boşlukla örter.

    Konumlar korunduğu için eşleşmelerin satır numaraları değişmez.
    Blok alıntılar başkasının sözüdür; ölçülmez ve değiştirilmez.
    """
    for desen in (_KOD_BLOGU, _SATIR_ICI_KOD, _MD_BAGLANTI_HEDEF, _URL, _HTML, _ALINTI_SATIRI):
        metin = desen.sub(_bosalt, metin)
    return metin


def kelimeler(metin: str) -> List[str]:
    return _KELIME.findall(metin)


def _sinirla(x: float) -> float:
    return max(0.0, min(1.0, x))


def _istatistik(sayilar: Sequence[int]) -> Tuple[float, float, float]:
    if not sayilar:
        return 0.0, 0.0, 0.0
    ort = statistics.mean(sayilar)
    std = statistics.pstdev(sayilar) if len(sayilar) > 1 else 0.0
    return ort, std, (std / ort if ort else 0.0)


def cumlelere_bol(paragraf: str) -> List[str]:
    """Türkçe için cümle bölücü.

    Kısaltmalarda (vb., Prof.), Romen rakamlı sıra sayılarında (II. Mahmut),
    tek harfli adlarda (A. Yılmaz) ve cümle başındaki numaralarda (3. Bölüm)
    bölmez. "19. yüzyıl" gibi küçük harfle devam eden sıra sayıları zaten bölünmez.
    """
    cumleler: List[str] = []
    bas = 0
    for m in _SINIR.finditer(paragraf):
        devam = paragraf[m.end():].lstrip("\"'“‘«(*_")
        if not devam:
            continue
        ilk = devam[0]
        if not (ilk.isupper() or ilk.isdigit() or ilk in "—–-"):
            continue
        if m.group(1) == ".":
            i = m.start()
            while i > bas and not paragraf[i - 1].isspace():
                i -= 1
            if i < m.start():
                ham = paragraf[i:m.start()].lstrip("(\"'“‘«*_")
                ilk_sozcuk = not paragraf[bas:i].strip()
                if (tr_kucuk(ham) in _KISALTMALAR
                        or re.fullmatch(r"[IVXLCDM]{1,6}|[A-ZÇĞİÖŞÜ]", ham)
                        or (ilk_sozcuk and re.fullmatch(r"\d{1,3}", ham))):
                    continue
        cumleler.append(paragraf[bas:m.end(2)].strip())
        bas = m.end()
    kalan = paragraf[bas:].strip()
    if kalan:
        cumleler.append(kalan)
    return [c for c in cumleler if kelimeler(c)]


# ------------------------------------------------------------------- kalıplar

@dataclass
class Kalip:
    id: str
    kategori: str
    agirlik: int
    desen: "re.Pattern[str]"
    aciklama: str
    oneri: str
    ornek: str = ""
    serbest: int = 0  # metindeki ilk bu kadar eşleşme doğal sayılır, puana girmez


_KALIP_ONBELLEK: Dict[Path, List[Kalip]] = {}
_KATLI_ONBELLEK: Dict[int, "re.Pattern[str]"] = {}


def _katli_desen(k: Kalip) -> "re.Pattern[str]":
    """Kalıbın Türkçe harfleri ASCII'ye katlanmış hâli (konumları değiştirmez)."""
    anahtar = id(k)
    if anahtar not in _KATLI_ONBELLEK:
        _KATLI_ONBELLEK[anahtar] = re.compile(k.desen.pattern.translate(_ASCII_KATLA), re.M)
    return _KATLI_ONBELLEK[anahtar]


def kaliplari_yukle(yol: Path = KALIP_DOSYASI) -> List[Kalip]:
    if yol in _KALIP_ONBELLEK:
        return _KALIP_ONBELLEK[yol]
    with open(yol, encoding="utf-8") as f:
        veri = json.load(f)
    sonuc: List[Kalip] = []
    for k in veri["kaliplar"]:
        try:
            desen = re.compile(k["desen"], re.M)
        except re.error as hata:
            raise ValueError(f"Geçersiz desen ({k.get('id')}): {hata}") from hata
        sonuc.append(Kalip(k["id"], k["kategori"], int(k["agirlik"]), desen,
                           k["aciklama"], k["oneri"], k.get("ornek", ""), int(k.get("serbest", 0))))
    _KALIP_ONBELLEK[yol] = sonuc
    return sonuc


def kalip_eslesmeleri(orijinal: str, maskeli: str, kaliplar: Sequence[Kalip]) -> List[Dict]:
    """Kalıpları bulur. Çakışan eşleşmelerden ağırlığı yüksek olanı tutar."""
    kucuk = tr_kucuk(maskeli.replace("’", "'"))
    ayni_uzunluk = len(kucuk) == len(orijinal)
    katla = ascii_yazilmis(orijinal)
    if katla:
        kucuk = kucuk.translate(_ASCII_KATLA)
    adaylar = []
    for k in kaliplar:
        for m in (_katli_desen(k) if katla else k.desen).finditer(kucuk):
            if m.end() > m.start():
                adaylar.append((m.start(), m.end(), k))
    adaylar.sort(key=lambda a: (-a[2].agirlik, -(a[1] - a[0]), a[0]))
    secilen: List[Tuple[int, int, Kalip]] = []
    for bas, son, k in adaylar:
        if any(bas < s2 and b2 < son for b2, s2, _ in secilen):
            continue
        secilen.append((bas, son, k))
    secilen.sort(key=lambda a: a[0])
    sonuc = []
    goruldu: Counter = Counter()
    for bas, son, k in secilen:
        parca = (orijinal if ayni_uzunluk else kucuk)[bas:son]
        goruldu[k.id] += 1
        serbest = goruldu[k.id] <= k.serbest
        sonuc.append({
            "id": k.id, "kategori": k.kategori, "agirlik": k.agirlik,
            "etkin_agirlik": 0 if serbest else k.agirlik, "serbest": serbest,
            "satir": kucuk.count("\n", 0, bas) + 1,
            "metin": " ".join(parca.split()),
            "aciklama": k.aciklama, "oneri": k.oneri,
        })
    return sonuc


# ------------------------------------------------------------------- yapılar

@dataclass
class Yapi:
    paragraflar: List[Tuple[int, str]]
    liste_ogeleri: List[Tuple[int, str]]
    basliklar: List[Tuple[int, str]]
    duzyazi_satirlari: List[str]


def yapilari_ayir(maskeli: str) -> Yapi:
    paragraflar: List[Tuple[int, str]] = []
    liste: List[Tuple[int, str]] = []
    basliklar: List[Tuple[int, str]] = []
    duzyazi: List[str] = []
    tampon: List[str] = []
    tampon_satir = 0

    def bosalt() -> None:
        nonlocal tampon, tampon_satir
        if tampon:
            paragraflar.append((tampon_satir, " ".join(t.strip() for t in tampon)))
        tampon, tampon_satir = [], 0

    satirlar = maskeli.split("\n")
    dolu = [i for i, s in enumerate(satirlar) if s.strip()]
    emojili = {i for i in dolu if _EMOJI_MADDE.match(satirlar[i])}
    # Emojiyle başlayan satır, yalnızca komşu dolu satır da emojiliyse madde sayılır.
    emoji_madde = set()
    for j, i in enumerate(dolu):
        if i in emojili and ((j > 0 and dolu[j - 1] in emojili) or (j + 1 < len(dolu) and dolu[j + 1] in emojili)):
            emoji_madde.add(i)

    for no, satir in enumerate(satirlar, 1):
        if not satir.strip():
            bosalt()
            continue
        if _BASLIK.match(satir):
            bosalt()
            basliklar.append((no, satir.strip()))
            continue
        if _TABLO.match(satir) or _YATAY_CIZGI.match(satir) or _ETIKET_SATIRI.match(satir):
            bosalt()
            continue
        if _LISTE_ISARETI_ZORUNLU.match(satir) or (no - 1) in emoji_madde:
            bosalt()
            liste.append((no, satir.strip()))
            duzyazi.append(satir)
            continue
        if not tampon:
            tampon_satir = no
        tampon.append(satir)
        duzyazi.append(satir)
    bosalt()
    return Yapi(paragraflar, liste, basliklar, duzyazi)


def gizli_karakterler(metin: str) -> Dict:
    gorunmez = _GORUNMEZ.findall(metin)
    homoglif = []
    for kelime in re.findall(r"\w+", metin):
        latin = any("a" <= c.lower() <= "z" or c in "çğıöşüÇĞİÖŞÜ" for c in kelime)
        yabanci = any("Ѐ" <= c <= "ӿ" or "Ͱ" <= c <= "Ͽ" for c in kelime)
        if latin and yabanci:
            homoglif.append(kelime)
    return {
        "gorunmez": len(gorunmez),
        "gorunmez_turleri": sorted({f"U+{ord(c):04X}" for c in gorunmez}),
        "homoglif": len(homoglif),
        "homoglif_ornekleri": homoglif[:5],
    }


# -------------------------------------------------------------------- analiz

def analiz_et(metin: str, uslup: str = "genel", kaliplar: Optional[Sequence[Kalip]] = None) -> Dict:
    if uslup not in USLUPLAR:
        raise ValueError(f"Bilinmeyen üslup: {uslup}. Seçenekler: {', '.join(USLUPLAR)}")
    profil = USLUPLAR[uslup]
    kaliplar = kaliplar if kaliplar is not None else kaliplari_yukle()

    metin = normallestir(metin)
    maskeli = maskele(metin)
    yapi = yapilari_ayir(maskeli)

    cumleler: List[str] = []
    paragraf_uzunluklari: List[int] = []
    for _, p in yapi.paragraflar:
        pc = cumlelere_bol(p)
        cumleler.extend(pc)
        if pc:
            paragraf_uzunluklari.append(len(kelimeler(p)))

    tum_kelimeler = kelimeler(" ".join(s for s in yapi.duzyazi_satirlari)
                              + " " + " ".join(b for _, b in yapi.basliklar))
    kelime_sayisi = len(tum_kelimeler)
    duzyazi_kelimeleri = [tr_kucuk(k) for k in kelimeler(" ".join(p for _, p in yapi.paragraflar))]
    cumle_uzunluklari = [len(kelimeler(c)) for c in cumleler]
    ort, std, cv = _istatistik(cumle_uzunluklari)
    _, _, paragraf_cv = _istatistik(paragraf_uzunluklari)
    cumle_sayisi = len(cumleler)
    kisa = sum(1 for n in cumle_uzunluklari if n <= 7)
    uzun = sum(1 for n in cumle_uzunluklari if n >= 25)

    # Ek yükü
    mektedir = sum(1 for k in duzyazi_kelimeleri if len(k) > 6 and _MEKTEDIR.search(k))
    ebilir = sum(1 for k in duzyazi_kelimeleri if _EBILIR.match(k))
    adfiil = sum(1 for k in duzyazi_kelimeleri
                 if _ADFIIL.match(k) and not k.startswith(_ADFIIL_ISTISNA))
    kopula_son = 0
    for c in cumleler:
        son = kelimeler(c)
        if son:
            s = tr_kucuk(son[-1])
            if len(s) > 4 and _KOPULA.search(s) and not _MEKTEDIR.search(s):
                kopula_son += 1

    # Açılışlar ve geçişler
    acilislar: List[str] = []
    resmi_acilis = 0
    acilis_virgul = 0
    for c in cumleler:
        kc = tr_kucuk(c).lstrip("\"'“‘«(*_-—– ")
        ilk = kelimeler(kc)
        acilislar.append(ilk[0] if ilk else "")
        for g in RESMI_GECISLER:
            if kc.startswith(g) and (len(kc) == len(g) or not kc[len(g)].isalpha()):
                resmi_acilis += 1
                break
        if _ACILIS_VIRGUL.match(kc):
            acilis_virgul += 1
    ardisik_ayni = sum(1 for i in range(1, len(acilislar)) if acilislar[i] and acilislar[i] == acilislar[i - 1])
    en_sik = Counter(a for a in acilislar if a).most_common(1)
    bu_acilis = sum(1 for a in acilislar if a in ("bu", "bunun", "buna", "bunu", "bunlar"))

    # Noktalama (kod ve alıntılar hariç düz yazı ve liste satırları)
    uzun_cizgi = 0
    tire_ara = 0
    noktali_virgul = 0
    for satir in yapi.duzyazi_satirlari:
        cizgiler = satir.count("—")
        if satir.lstrip().startswith("—"):
            cizgiler -= 1  # diyalog çizgisi
        uzun_cizgi += cizgiler
        tire_ara += len(_TIRE_ARA_SOZ.findall(satir))
        noktali_virgul += satir.count(";")
    ic_iki_nokta = 0
    for c in cumleler:
        for m in re.finditer(r":", c):
            once, sonra = c[:m.start()], c[m.end():]
            if once[-1:].isdigit() and sonra[:1].isdigit():
                continue
            if kelimeler(sonra):
                ic_iki_nokta += 1
    unlem = sum(c.count("!") for c in cumleler)

    # Yapı
    ham_satirlar = metin.split("\n")
    kalin_madde = sum(1 for s in ham_satirlar if _KALIN_MADDE.match(s))
    baslik_iki_nokta = sum(1 for _, b in yapi.basliklar if ":" in b)
    soru_baslik = sum(1 for _, b in yapi.basliklar if b.rstrip(" *_#").endswith("?"))
    emoji = len(_EMOJI.findall(maskeli))
    uclu = len(_UCLU.findall(" ".join(p for _, p in yapi.paragraflar)))

    # Kalıplar
    eslesmeler = kalip_eslesmeleri(metin, alintilari_maskele(maskeli), kaliplar)
    carpan = profil["kategori_carpani"]
    agirlikli = sum(e["etkin_agirlik"] * carpan.get(e["kategori"], 1.0) for e in eslesmeler)
    yogunluk = agirlikli / kelime_sayisi * 100 if kelime_sayisi else 0.0
    # Kısa metinde tek bir eşleşme yoğunluğu tavana vurdurmasın.
    puan_yogunlugu = agirlikli / max(kelime_sayisi, KISA_METIN_TABANI) * 100

    # Tekrarlanan üçlü kelime grupları
    tekrarlar: List[Dict] = []
    if len(duzyazi_kelimeleri) >= 120:
        ucluler = Counter(tuple(duzyazi_kelimeleri[i:i + 3]) for i in range(len(duzyazi_kelimeleri) - 2))
        tekrarlar = [{"grup": " ".join(g), "adet": n} for g, n in ucluler.most_common(5) if n >= 3]

    m: Dict = {
        "surum": SURUM,
        "uslup": uslup,
        "ozet": {
            "kelime": kelime_sayisi, "cumle": cumle_sayisi,
            "paragraf": len(paragraf_uzunluklari), "baslik": len(yapi.basliklar),
            "liste_ogesi": len(yapi.liste_ogeleri),
        },
        "ritim": {
            "ortalama": round(ort, 1), "std": round(std, 1), "cv": round(cv, 2),
            "kisa_oran": round(kisa / cumle_sayisi, 2) if cumle_sayisi else 0.0,
            "uzun_oran": round(uzun / cumle_sayisi, 2) if cumle_sayisi else 0.0,
            "en_kisa": min(cumle_uzunluklari) if cumle_uzunluklari else 0,
            "en_uzun": max(cumle_uzunluklari) if cumle_uzunluklari else 0,
            "paragraf_cv": round(paragraf_cv, 2) if len(paragraf_uzunluklari) >= 4 else None,
        },
        "ekler": {
            "mektedir": mektedir,
            "mektedir_oran": round(mektedir / cumle_sayisi, 2) if cumle_sayisi else 0.0,
            "kopula_son_oran": round(kopula_son / cumle_sayisi, 2) if cumle_sayisi else 0.0,
            "ebilir_oran": round(ebilir / cumle_sayisi, 2) if cumle_sayisi else 0.0,
            "adfiil_100": round(adfiil / len(duzyazi_kelimeleri) * 100, 1) if duzyazi_kelimeleri else 0.0,
        },
        "acilis": {
            "resmi_gecis_oran": round(resmi_acilis / cumle_sayisi, 2) if cumle_sayisi else 0.0,
            "virgullu_acilis": acilis_virgul,
            "bu_ile_acilis_oran": round(bu_acilis / cumle_sayisi, 2) if cumle_sayisi else 0.0,
            "ardisik_ayni_acilis": ardisik_ayni,
            "en_sik_acilis": ({"kelime": en_sik[0][0], "oran": round(en_sik[0][1] / cumle_sayisi, 2)}
                              if en_sik and cumle_sayisi >= 5 else None),
        },
        "noktalama": {
            "uzun_cizgi": uzun_cizgi, "tire_ara_soz": tire_ara,
            "noktali_virgul": noktali_virgul, "ic_iki_nokta": ic_iki_nokta, "unlem": unlem,
        },
        "yapi": {
            "kalin_baslikli_madde": kalin_madde, "baslikta_iki_nokta": baslik_iki_nokta,
            "soru_baslik": soru_baslik,
            "emoji": emoji, "uclu_siralama": uclu,
        },
        "gizli": gizli_karakterler(metin),
        "kaliplar": eslesmeler,
        "kalip_yogunlugu": round(yogunluk, 2),
        "kalip_puan_yogunlugu": round(puan_yogunlugu, 2),
        "ascii_yazim": ascii_yazilmis(metin),
        "tekrarlar": tekrarlar,
    }
    m["puan"] = puanla(m, profil)
    m["oneriler"] = oneriler(m, profil)
    m["uyarilar"] = uyarilar(m)
    return m


KISA_SAPTAMA_YOK = ("resmi",)  # doz tablosu: bu üsluplarda kısa saptama cümlesi kullanılmaz


def puanla(m: Dict, profil: Dict) -> Dict:
    """0-100 arası imza puanı. Yüksek puan = daha çok yapay zekâ imzası."""
    oz, rt, ek, ac, nk, yp = m["ozet"], m["ritim"], m["ekler"], m["acilis"], m["noktalama"], m["yapi"]
    kelime = max(oz["kelime"], 1)
    b: Dict[str, float] = {}

    b["kalip"] = 40 * _sinirla(m["kalip_puan_yogunlugu"] / 5.0)

    ritim = 0.0
    if oz["cumle"] >= 5:
        hedef = profil["cv_hedef"]
        taban = hedef - 0.25
        ritim = 14 * _sinirla((hedef - rt["cv"]) / (hedef - taban))
        if oz["cumle"] >= 8 and rt["kisa_oran"] == 0 and m["uslup"] not in KISA_SAPTAMA_YOK:
            ritim += 3
        if rt["paragraf_cv"] is not None and rt["paragraf_cv"] < 0.25:
            ritim += 3 * _sinirla((0.25 - rt["paragraf_cv"]) / 0.15)
    b["ritim"] = min(20.0, ritim)

    b["ekler"] = (6 * _sinirla((ek["mektedir_oran"] - profil["mektedir_tolerans"]) / 0.35)
                  + 2 * _sinirla((ek["adfiil_100"] - profil["adfiil_esik"]) / 4.0)
                  + 2 * _sinirla((ek["ebilir_oran"] - 0.30) / 0.30))

    gecis = 0.0
    if oz["cumle"] >= 4:
        gecis = 8 * _sinirla((ac["resmi_gecis_oran"] * profil["gecis_carpani"] - 0.10) / 0.25)
        gecis += 2 * _sinirla(ac["virgullu_acilis"] / 3)
    b["gecis"] = gecis

    iki_nokta_payi = 1 + kelime // 200  # sıralama ve örnek için doğal kullanım payı
    tire_payi = 1 + kelime // 300  # TDK kısa çizgiyle ara söze izin verir; yalnızca yığılma imzadır
    noktalama_yuku = (nk["uzun_cizgi"] + max(0, nk["tire_ara_soz"] - tire_payi) + nk["noktali_virgul"]
                      + 0.5 * max(0, nk["ic_iki_nokta"] - iki_nokta_payi)) / kelime * 100
    b["noktalama"] = 10 * _sinirla(noktalama_yuku / 1.5)

    yapi_yuku = (yp["kalin_baslikli_madde"] + 0.5 * yp["emoji"] + yp["baslikta_iki_nokta"]
                 + yp["soru_baslik"])
    b["yapi"] = 5 * _sinirla(yapi_yuku / 4)

    toplam = round(min(100.0, sum(b.values())))
    seviye = "düşük" if toplam < 25 else ("orta" if toplam < 50 else "yüksek")
    return {"toplam": toplam, "seviye": seviye,
            "bilesenler": {k: round(v, 1) for k, v in b.items()},
            "guvenilir": oz["kelime"] >= GUVEN_KELIME and oz["cumle"] >= GUVEN_CUMLE}


def oneriler(m: Dict, profil: Dict) -> List[str]:
    b = m["puan"]["bilesenler"]
    rt, ek, ac, nk, yp = m["ritim"], m["ekler"], m["acilis"], m["noktalama"], m["yapi"]
    adaylar: List[Tuple[float, str]] = []
    if b["kalip"] > 0:
        etkin = [e for e in m["kaliplar"] if not e["serbest"]]
        kategoriler = Counter(KATEGORI_ADLARI.get(e["kategori"], e["kategori"]) for e in etkin)
        en = ", ".join(f"{k} ({n})" for k, n in kategoriler.most_common(3))
        adaylar.append((b["kalip"], f"Kalıp temizliği: {len(etkin)} eşleşme, en yoğun kategoriler: {en}. "
                                    "Kalıbı eş anlamlısıyla değiştirme, cümleyi anlamından yeniden kur."))
    if b["ritim"] > 0:
        nedenler = []
        if rt["cv"] < profil["cv_hedef"]:
            if rt["kisa_oran"] >= 0.4:
                cozum = "kısa cümleler baskın, birkaçını zarf-fiille birleştirip uzun ve akışkan bir cümle kur"
            elif rt["uzun_oran"] >= 0.4 or rt["kisa_oran"] == 0:
                cozum = "uzun cümleler baskın, birini böl ya da kısa ve kesin bir cümle çıkar"
            else:
                cozum = "orta boy cümleler baskın, bir iki cümleyi kısalt, birini uzat"
            nedenler.append(f"cümle boyları tekdüze (CV {rt['cv']}, hedef ≥ {profil['cv_hedef']}): {cozum}")
        if m["ozet"]["cumle"] >= 8 and rt["kisa_oran"] == 0 and m["uslup"] not in KISA_SAPTAMA_YOK:
            nedenler.append("hiç kısa cümle (≤7 kelime) yok")
        if rt["paragraf_cv"] is not None and rt["paragraf_cv"] < 0.25:
            nedenler.append(f"paragraf boyları birbirine çok yakın (CV {rt['paragraf_cv']}): bazı paragrafları kısalt ya da birleştir")
        metin = ". ".join(n[:1].upper() + n[1:] for n in nedenler)
        adaylar.append((b["ritim"], f"Ritim: {metin}."))
    if b["ekler"] > 0:
        parca, cozum = [], []
        if ek["mektedir_oran"] > profil["mektedir_tolerans"]:
            parca.append(f"cümle başına {ek['mektedir_oran']} '-mekte/-makta'")
            cozum.append("üsluba uygun kiplere geç")
        if ek["ebilir_oran"] > 0.30:
            parca.append(f"cümle başına {ek['ebilir_oran']} '-ebilir'")
            cozum.append("tekrarlanan '-ebilir'leri tek bir olasılık ifadesinde topla ama kaynaktaki olasılığı kesinliğe çevirme")
        if ek["adfiil_100"] > profil["adfiil_esik"]:
            parca.append(f"100 kelimede {ek['adfiil_100']} ad-fiil")
            cozum.append("ad-fiilleri çekimli fiile çevir")
        cozum_metni = ", ".join(cozum)
        adaylar.append((b["ekler"], f"Ek yükü: {', '.join(parca)}. {cozum_metni[:1].upper()}{cozum_metni[1:]}."))
    if b["gecis"] > 0:
        adaylar.append((b["gecis"], f"Resmi geçişle açılan cümle oranı %{round(ac['resmi_gecis_oran'] * 100)}"
                                    + (f", {ac['virgullu_acilis']} tanesinde İngilizce usulü virgül var" if ac["virgullu_acilis"] else "")
                                    + ". Geçişlerin çoğunu at, kalanları cümlenin içine al."))
    if b["noktalama"] > 0:
        parca, cozum = [], []
        if nk["uzun_cizgi"] or nk["tire_ara_soz"]:
            parca.append(f"{nk['uzun_cizgi'] + nk['tire_ara_soz']} ara söz çizgisi")
            cozum.append("ara sözü virgülle ya da parantezle ver")
        if nk["noktali_virgul"]:
            parca.append(f"{nk['noktali_virgul']} noktalı virgül")
            cozum.append("noktalı virgüllü cümleleri ikiye böl")
        if nk["ic_iki_nokta"]:
            parca.append(f"{nk['ic_iki_nokta']} cümle içi iki nokta")
            cozum.append("açıklama amaçlı iki noktaları düz cümleye çevir")
        cozum_metni = ", ".join(cozum)
        adaylar.append((b["noktalama"], f"Noktalama: {', '.join(parca)}. {cozum_metni[:1].upper()}{cozum_metni[1:]}."))
    if b["yapi"] > 0:
        etiketler = (("kalin_baslikli_madde", "kalın etiketli madde"), ("emoji", "emoji"),
                     ("baslikta_iki_nokta", "iki noktalı başlık"), ("soru_baslik", "soru biçimli başlık"))
        parca = [f"{yp[k]} {ad}" for k, ad in etiketler if yp[k]]
        adaylar.append((b["yapi"], f"Yapı: {', '.join(parca)}. "
                                   "Yapıya dokunma izni varsa kalın etiketli maddeleri ve süslü başlıkları sadeleştir."))
    if ac["en_sik_acilis"] and ac["en_sik_acilis"]["oran"] >= 0.25:
        adaylar.append((3.0, f"'{ac['en_sik_acilis']['kelime']}' ile başlayan cümle oranı "
                             f"%{round(ac['en_sik_acilis']['oran'] * 100)}. Açılışları çeşitlendir."))
    if yp["uclu_siralama"] >= 3 and m["ozet"]["cumle"] and yp["uclu_siralama"] / m["ozet"]["cumle"] > 0.2:
        adaylar.append((2.0, f"{yp['uclu_siralama']} adet 'X, Y ve Z' üçlüsü var. Bazılarını ikiye indir ya da tek örneğe in."))
    adaylar.sort(key=lambda a: -a[0])
    return [metin for _, metin in adaylar]


def uyarilar(m: Dict) -> List[str]:
    u = []
    if m["ozet"]["kelime"] == 0:
        return ["Metin boş ya da ölçülecek düz yazı yok."]
    if m["ozet"]["kelime"] >= GUVEN_KELIME and m["ozet"]["cumle"] < GUVEN_CUMLE:
        u.append("Cümle sınırı neredeyse hiç bulunamadı (noktalama eksik olabilir). Ritim ölçümleri geçersiz.")
    elif not m["puan"]["guvenilir"]:
        u.append(f"Metin kısa ({GUVEN_KELIME} kelimeden ya da {GUVEN_CUMLE} cümleden az): "
                 "istatistikler yön gösterir, kesin değildir.")
    if m.get("ascii_yazim"):
        u.append("Metin Türkçe harfler (ç, ğ, ı, ö, ş, ü) kullanılmadan yazılmış. Kalıplar ASCII karşılıklarıyla arandı. "
                 "Teslimde Türkçe harfleri geri koy.")
    g = m["gizli"]
    if g["gorunmez"]:
        u.append(f"{g['gorunmez']} görünmez karakter bulundu ({', '.join(g['gorunmez_turleri'])}). "
                 "Bunlar detektör atlatma hilesi olarak bilinir ve kolayca yakalanır. Temizlenmeli.")
    if g["homoglif"]:
        u.append(f"{g['homoglif']} kelimede Kiril/Yunan harfi karışmış (ör. {', '.join(g['homoglif_ornekleri'])}). "
                 "Bu bir homoglif hilesidir. Temizlenmeli.")
    return u


# ----------------------------------------------------------------- ses kartı

def ses_karti(metin: str) -> Dict:
    """Bir yazarın kendi metinlerinden ölçülebilir üslup özelliklerini çıkarır."""
    metin = normallestir(metin)
    maskeli = maskele(metin)
    yapi = yapilari_ayir(maskeli)
    cumleler = [c for _, p in yapi.paragraflar for c in cumlelere_bol(p)]
    uzunluklar = [len(kelimeler(c)) for c in cumleler]
    ort, std, cv = _istatistik(uzunluklar)
    p_uz = [len(kelimeler(p)) for _, p in yapi.paragraflar if kelimeler(p)]
    p_ort, _, _ = _istatistik(p_uz)
    ks = [tr_kucuk(k) for k in kelimeler(" ".join(p for _, p in yapi.paragraflar))]
    n = max(len(ks), 1)
    sayac = Counter(ks)
    belirtecler = {b: round(sayac[b] / n * 1000, 1) for b in SOYLEM_BELIRTECLERI if sayac[b]}
    acilis = Counter()
    for c in cumleler:
        ilk = kelimeler(tr_kucuk(c))
        if ilk:
            acilis[ilk[0]] += 1
    birinci_tekil = sum(sayac[k] for k in ("ben", "bence", "bana", "beni", "benim", "bende", "benden"))
    birinci_cogul = sum(sayac[k] for k in ("biz", "bize", "bizi", "bizim", "bizde", "bizden"))
    duz = " ".join(p for _, p in yapi.paragraflar)
    return {
        "kelime": len(ks), "cumle": len(cumleler),
        "cumle_ortalama": round(ort, 1), "cumle_std": round(std, 1), "cumle_cv": round(cv, 2),
        "kisa_cumle_oran": round(sum(1 for u in uzunluklar if u <= 7) / len(uzunluklar), 2) if uzunluklar else 0,
        "uzun_cumle_oran": round(sum(1 for u in uzunluklar if u >= 25) / len(uzunluklar), 2) if uzunluklar else 0,
        "paragraf_ortalama": round(p_ort, 1),
        "soru_oran": round(sum(1 for c in cumleler if c.rstrip("\"'”’)").endswith("?")) / len(cumleler), 2) if cumleler else 0,
        "unlem_oran": round(sum(1 for c in cumleler if c.rstrip("\"'”’)").endswith("!")) / len(cumleler), 2) if cumleler else 0,
        "parantez_100": round(duz.count("(") / n * 100, 2),
        "virgul_cumle": round(duz.count(",") / len(cumleler), 2) if cumleler else 0,
        "mektedir_oran": round(sum(1 for k in ks if len(k) > 6 and _MEKTEDIR.search(k)) / max(len(cumleler), 1), 2),
        "birinci_tekil_1000": round(birinci_tekil / n * 1000, 1),
        "birinci_cogul_1000": round(birinci_cogul / n * 1000, 1),
        "soylem_belirtecleri_1000": dict(sorted(belirtecler.items(), key=lambda x: -x[1])),
        "sik_acilislar": [k for k, _ in acilis.most_common(5)],
        "uzun_cizgi": duz.count("—"), "noktali_virgul": duz.count(";"),
    }


def ses_karti_metni(k: Dict) -> str:
    b = ", ".join(f"{s} ({v})" for s, v in list(k["soylem_belirtecleri_1000"].items())[:10]) or "belirgin değil"
    satirlar = [
        "SES KARTI",
        f"Örneklem: {k['kelime']} kelime, {k['cumle']} cümle"
        + ("  (uyarı: 300 kelimenin altında, kart kaba bir tahmindir)" if k["kelime"] < 300 else ""),
        "",
        f"Cümle boyu      : ortalama {k['cumle_ortalama']} kelime, std {k['cumle_std']}, CV {k['cumle_cv']}",
        f"Kısa/uzun cümle : %{round(k['kisa_cumle_oran'] * 100)} kısa (≤7), %{round(k['uzun_cumle_oran'] * 100)} uzun (≥25)",
        f"Paragraf boyu   : ortalama {k['paragraf_ortalama']} kelime",
        f"Virgül/cümle    : {k['virgul_cumle']}  ·  parantez/100 kelime: {k['parantez_100']}",
        f"Soru / ünlem    : %{round(k['soru_oran'] * 100)} / %{round(k['unlem_oran'] * 100)}",
        f"Kişi            : 1. tekil {k['birinci_tekil_1000']}‰, 1. çoğul {k['birinci_cogul_1000']}‰",
        f"-mekte/-makta   : cümle başına {k['mektedir_oran']}",
        f"Söylem belirteçleri (‰): {b}",
        f"Sık açılışlar   : {', '.join(k['sik_acilislar']) or '-'}",
        f"Uzun çizgi / noktalı virgül: {k['uzun_cizgi']} / {k['noktali_virgul']}",
        "",
        "Yeniden yazarken: cümle ortalamasını ±3 kelime, CV'yi ±0,1 içinde tut, belirteçleri bu sıklıkla kullan,",
        "yazarın hiç kullanmadığı noktalama ve bağlaçları ekleme.",
    ]
    return "\n".join(satirlar)


# ------------------------------------------------------------- karşılaştırma

_SAYI_SOZCUKLERI = {
    "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9,
    "on": 10, "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50, "altmış": 60, "yetmiş": 70,
    "seksen": 80, "doksan": 90,
}
_OLCEKLER = {"yüz": 100, "bin": 1000, "milyon": 10 ** 6, "milyar": 10 ** 9, "trilyon": 10 ** 12}
_SAYI_OGESI = re.compile(
    r"(?P<yuzde>%\s?|\byüzde\s+)?(?P<sayi>\d+(?:[.,]\d+)*)(?:\s+(?P<olcek>bin|milyon|milyar|trilyon)\b)?"
    r"|(?P<soz>\b(?:(?:bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|kırk|elli|altmış|yetmiş|"
    r"seksen|doksan|yüz|bin|milyon|milyar)\s+)*(?:iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|kırk|"
    r"elli|altmış|yetmiş|seksen|doksan|yüz|bin|milyon|milyar)\b"
    # Sayı sözcüğü bir adın önünde durur ("üç kişi"). Cümle sonundaki ya da bağlaçtan önceki
    # "yedi", "altı" gibi sözcükler çoğunlukla fiil ya da addır ("yemeği yedi", "masanın altı").
    r"(?=\s+(?!(?:ve|ama|fakat|ancak|çünkü|ki|diye|mi|mı|mu|mü|de|da)\b)[^\W\d_]))")
_BINLIK = re.compile(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?")


def _sozcuk_sayi(ifade: str) -> Optional[int]:
    """"iki yüz elli" → 250. Tek başına "bir" sayı sayılmaz (belirsiz tanımlık)."""
    toplam, ara = 0, 0
    for s in ifade.split():
        if s == "bir":
            ara += 1
        elif s in _SAYI_SOZCUKLERI:
            ara += _SAYI_SOZCUKLERI[s]
        elif s == "yüz":
            ara = (ara or 1) * 100
        else:
            toplam += (ara or 1) * _OLCEKLER[s]
            ara = 0
    deger = toplam + ara
    return deger if deger and ifade.strip() != "bir" else None


def _sayi_degeri(ham: str) -> str:
    """Biçimi değil değeri karşılaştırmak için kanonik yazım: "1.250,50" ve "1250,50" aynıdır."""
    if _BINLIK.fullmatch(ham):
        ham = ham.replace(".", "")
    if re.fullmatch(r"\d+,\d+", ham):
        tam, ondalik = ham.split(",")
        tam, ondalik = tam.lstrip("0") or "0", ondalik.rstrip("0")
        return f"{tam},{ondalik}" if ondalik else tam
    if re.fullmatch(r"\d+", ham):
        return ham.lstrip("0") or "0"
    return ham  # sürüm numarası, saat gibi biçimler olduğu gibi karşılaştırılır


def sayilari_cikar(metin: str) -> List[Tuple[str, str]]:
    """Metindeki sayıları (kanonik değer, metindeki yazımı) çiftleri olarak döndürür.

    Rakamla ve yazıyla yazılmış sayılar, yüzdeler ("%15", "yüzde 15") ve ölçekler
    ("2 milyon") tanınır. Kod, bağlantı ve HTML dışarıda kalır.
    """
    kucuk = tr_kucuk(maskele(normallestir(metin)))
    sonuc: List[Tuple[str, str]] = []
    for m in _SAYI_OGESI.finditer(kucuk):
        if m.group("sayi"):
            deger = _sayi_degeri(m.group("sayi"))
            if m.group("olcek") and re.fullmatch(r"\d+(,\d+)?", deger):
                tam, _, ondalik = deger.partition(",")
                carpan = _OLCEKLER[m.group("olcek")]
                deger = str(int(tam) * carpan + (int(ondalik) * carpan // 10 ** len(ondalik) if ondalik else 0))
            if m.group("yuzde"):
                deger = "%" + deger
        else:
            sayi = _sozcuk_sayi(m.group("soz"))
            if sayi is None:
                continue
            deger = str(sayi)
            onceki = kucuk[max(0, m.start() - 6):m.start()]
            if onceki.endswith("yüzde "):
                deger = "%" + deger
        sonuc.append((deger, " ".join(m.group(0).split())))
    return sonuc


def _ozel_adlar(metin: str) -> List[str]:
    """Özel ad adayları: cümle içinde büyük harfle başlayanlar, kesme işaretli adlar ve kısaltmalar.

    Başlıklar dışarıda kalır. Cümle başındaki sözcük yalnızca kesme işareti alıyorsa
    ("Google'ın") ya da metinde başka bir yerde de ad olarak geçiyorsa ad sayılır.
    Kalın etiketlerin (**Veri Okuryazarlığı:**) içinden yalnızca kısaltmalar ve kesme
    işaretli adlar alınır, çünkü derin yeniden yazımda etiketler kalkabilir.
    """
    yapi = yapilari_ayir(maskele(normallestir(metin)))
    ic_adlar: List[str] = []
    bas_adaylari: List[str] = []

    def kisaltma_mi(k: str) -> bool:
        return (2 <= len(k) <= 6 and k.isupper() and k.isalpha()
                and not re.fullmatch(r"[IVXLCDM]+", k))

    bloklar = []
    for _, p in yapi.paragraflar + yapi.liste_ogeleri:
        for etiket in re.findall(r"\*\*([^*\n]+)\*\*", p):
            for k in kelimeler(etiket):
                if kisaltma_mi(k) or re.search(r"['’]", k):
                    ic_adlar.append(re.split(r"['’]", k)[0])
        bloklar.append(re.sub(r"\*\*[^*\n]+\*\*", " ", p))
    bloklar = [parca for b in bloklar for parca in re.split(r":\s+", b)]
    for blok in bloklar:
        for c in cumlelere_bol(" ".join(blok.split())):
            ks = kelimeler(c)
            if not ks:
                continue
            ilk = ks[0]
            if kisaltma_mi(re.split(r"['’]", ilk)[0]):
                ic_adlar.append(re.split(r"['’]", ilk)[0])
            elif ilk[:1].isupper() and re.search(r"['’]", ilk):
                ic_adlar.append(re.split(r"['’]", ilk)[0])  # "Elif'in", "Ankara'da"
            elif ilk[:1].isupper():
                bas_adaylari.append(ilk)
            for k in ks[1:]:
                kok = re.split(r"['’]", k)[0]
                if kisaltma_mi(kok) or (k[:1].isupper() and not k.isupper()):
                    ic_adlar.append(kok)
    bilinen = {tr_kucuk(a) for a in ic_adlar}
    adlar = ic_adlar + [a for a in bas_adaylari if tr_kucuk(a) in bilinen]
    return [a for a in adlar if tr_kucuk(a).rstrip(".") not in _KISALTMALAR and len(a) > 1]


def _ad_geciyor_mu(ad: str, metin_kucuk: str) -> bool:
    """Adın kökü metinde bir sözcüğün başında geçiyor mu? ("Ankara" → "Ankara'ya", "Bankası" → "Bankasının")"""
    kucuk = tr_kucuk(ad)
    kok = kucuk[:min(len(kucuk), max(5, len(kucuk) - 3))]
    return re.search(r"(?<![^\W\d_])" + re.escape(kok), metin_kucuk) is not None


def koruma_kontrolu(once: str, sonra: str) -> Dict:
    """Sayıların ve özel adların yeniden yazımda kaybolup kaybolmadığını kontrol eder.

    Sayılar değerleriyle ve adetleriyle karşılaştırılır. "%15" ile "yüzde 15", "3" ile
    "üç", "1.250" ile "1250" aynı sayılır. "2 milyon" ile "2 milyar" farklıdır.
    """
    s_once, s_sonra = sayilari_cikar(once), sayilari_cikar(sonra)
    c_once, c_sonra = Counter(d for d, _ in s_once), Counter(d for d, _ in s_sonra)
    yazim = {}
    for d, y in s_once + s_sonra:
        yazim.setdefault(d, y)
    kayip = [yazim[d] for d in c_once if d not in c_sonra]
    azalan = [f"{yazim[d]} ({c_once[d]} → {c_sonra[d]})" for d in c_once if 0 < c_sonra[d] < c_once[d]]
    yeni = [yazim[d] for d in c_sonra if d not in c_once]
    sonra_kucuk = tr_kucuk(normallestir(sonra))
    kayip_ad = [ad for ad in dict.fromkeys(_ozel_adlar(once)) if not _ad_geciyor_mu(ad, sonra_kucuk)]
    return {"kayip_sayilar": kayip, "azalan_sayilar": azalan, "kayip_ozel_adlar": kayip_ad,
            "yeni_sayilar": yeni}


def etkin_kaliplar(m: Dict) -> List[Dict]:
    """Puana giren eşleşmeler ("tek kullanım doğal" sayılanlar hariç)."""
    return [e for e in m["kaliplar"] if not e.get("serbest")]


def karsilastir(once: str, sonra: str, uslup: str = "genel") -> Dict:
    a, b = analiz_et(once, uslup), analiz_et(sonra, uslup)
    satirlar = [
        ("İmza puanı", a["puan"]["toplam"], b["puan"]["toplam"]),
        ("Kalıp eşleşmesi", len(etkin_kaliplar(a)), len(etkin_kaliplar(b))),
        ("Kalıp yoğunluğu /100", a["kalip_yogunlugu"], b["kalip_yogunlugu"]),
        ("Cümle CV", a["ritim"]["cv"], b["ritim"]["cv"]),
        ("Ortalama cümle", a["ritim"]["ortalama"], b["ritim"]["ortalama"]),
        ("-mekte/-makta oranı", a["ekler"]["mektedir_oran"], b["ekler"]["mektedir_oran"]),
        ("Resmi geçiş açılışı", a["acilis"]["resmi_gecis_oran"], b["acilis"]["resmi_gecis_oran"]),
        ("Uzun çizgi", a["noktalama"]["uzun_cizgi"], b["noktalama"]["uzun_cizgi"]),
        ("Noktalı virgül", a["noktalama"]["noktali_virgul"], b["noktalama"]["noktali_virgul"]),
        ("Kelime", a["ozet"]["kelime"], b["ozet"]["kelime"]),
    ]
    koruma = koruma_kontrolu(once, sonra)
    uyar = []
    ka, kb = a["ozet"]["kelime"], b["ozet"]["kelime"]
    if ka and abs(kb - ka) / ka > UZUNLUK_TOLERANSI:
        yon = "azaldı" if kb < ka else "arttı"
        uyar.append(f"Kelime sayısı %{abs(round((kb - ka) / ka * 100))} {yon} ({ka} → {kb}). "
                    "Silinen ya da eklenen içeriğin bilinçli olduğunu kontrol et.")
    def liste(ogeler: Sequence[str]) -> str:
        return ", ".join(f"«{o}»" for o in ogeler)
    if koruma["kayip_sayilar"]:
        uyar.append(f"Taslakta bulunmayan sayılar: {liste(koruma['kayip_sayilar'])}. Kasıtlı değilse geri ekle.")
    if koruma["azalan_sayilar"]:
        uyar.append(f"Taslakta daha az geçen sayılar: {liste(koruma['azalan_sayilar'])}. "
                    "Tekrar eden bir anma silindiyse sorun yok. Farklı bir olguya aitse geri ekle.")
    if koruma["kayip_ozel_adlar"]:
        uyar.append(f"Taslakta bulunmayan olası özel adlar (yaklaşık): {liste(koruma['kayip_ozel_adlar'][:10])}.")
    if koruma["yeni_sayilar"]:
        uyar.append(f"Kaynakta olmayan yeni sayılar: {liste(koruma['yeni_sayilar'])}. Uydurma bilgi olmadığından emin ol.")
    return {"once": a, "sonra": b, "tablo": satirlar, "koruma": koruma, "uyarilar": uyar,
            "kalan_kaliplar": b["kaliplar"]}


# ------------------------------------------------------------------- çıktılar

def rapor_metni(m: Dict, ayrinti: bool = False) -> str:
    oz, rt, ek, ac, nk, yp, p = m["ozet"], m["ritim"], m["ekler"], m["acilis"], m["noktalama"], m["yapi"], m["puan"]
    s = [
        "TÜRKÇE İMZA ANALİZİ  (yol gösterici bir ölçümdür, AI detektörü değildir)",
        f"Üslup: {m['uslup']} · Kelime: {oz['kelime']} · Cümle: {oz['cumle']} · Paragraf: {oz['paragraf']}"
        + (f" · Başlık: {oz['baslik']}" if oz["baslik"] else "")
        + (f" · Liste öğesi: {oz['liste_ogesi']}" if oz["liste_ogesi"] else ""),
        "",
        f"İMZA PUANI: {p['toplam']}/100 ({p['seviye']})"
        + ("" if p["guvenilir"] else "  [kısa metin, düşük güven]"),
        "  " + " · ".join(f"{BILESEN_ADLARI.get(k, k)} {v}" for k, v in p["bilesenler"].items()),
        "",
        "Ritim",
        f"  Cümle boyu: ortalama {rt['ortalama']}, std {rt['std']}, CV {rt['cv']} "
        f"(en kısa {rt['en_kisa']}, en uzun {rt['en_uzun']})",
        f"  Kısa cümle (≤7): %{round(rt['kisa_oran'] * 100)} · Uzun cümle (≥25): %{round(rt['uzun_oran'] * 100)}"
        + (f" · Paragraf CV: {rt['paragraf_cv']}" if rt["paragraf_cv"] is not None else ""),
        "Ekler",
        f"  -mekte/-makta: {ek['mektedir']} (cümle başına {ek['mektedir_oran']}) · "
        f"-dır ile biten cümle: %{round(ek['kopula_son_oran'] * 100)} · "
        f"-ebilir: cümle başına {ek['ebilir_oran']} · ad-fiil/100: {ek['adfiil_100']}",
        "Açılışlar",
        f"  Resmi geçişle açılan cümle: %{round(ac['resmi_gecis_oran'] * 100)} · virgüllü açılış: {ac['virgullu_acilis']} · "
        f"'Bu' ile açılış: %{round(ac['bu_ile_acilis_oran'] * 100)} · ardışık aynı açılış: {ac['ardisik_ayni_acilis']}",
        "Noktalama ve yapı",
        f"  Uzun çizgi: {nk['uzun_cizgi']} · ara söz tiresi: {nk['tire_ara_soz']} · noktalı virgül: {nk['noktali_virgul']} · "
        f"cümle içi iki nokta: {nk['ic_iki_nokta']} · ünlem: {nk['unlem']}",
        f"  Kalın başlıklı madde: {yp['kalin_baslikli_madde']} · emoji: {yp['emoji']} · "
        f"iki noktalı başlık: {yp['baslikta_iki_nokta']} · soru başlık: {yp['soru_baslik']} · "
        f"'X, Y ve Z' üçlüsü: {yp['uclu_siralama']}",
    ]
    es = m["kaliplar"]
    s += ["", f"Kalıp eşleşmeleri: {len(es)} (ağırlıklı yoğunluk {m['kalip_yogunlugu']}/100 kelime)"]
    gosterilecek = es if ayrinti else sorted(es, key=lambda e: -e["agirlik"])[:15]
    for e in sorted(gosterilecek, key=lambda e: e["satir"]):
        s.append(f"  {_agirlik_etiketi(e)} s.{e['satir']} \"{e['metin']}\" "
                 f"({KATEGORI_ADLARI.get(e['kategori'], e['kategori'])}) → {e['oneri']}")
    if not ayrinti and len(es) > 15:
        s.append(f"  ... {len(es) - 15} eşleşme daha (--ayrinti ile tümü)")
    if m["tekrarlar"]:
        s += ["", "Tekrarlanan kelime grupları: " + ", ".join(f"\"{t['grup']}\" ×{t['adet']}" for t in m["tekrarlar"])]
    if m["oneriler"]:
        s += ["", "Öncelikli düzeltmeler"]
        s += [f"  {i}. {o}" for i, o in enumerate(m["oneriler"], 1)]
    if m["uyarilar"]:
        s += ["", "Uyarılar"] + [f"  ! {u}" for u in m["uyarilar"]]
    return "\n".join(s)


def _agirlik_etiketi(e: Dict) -> str:
    return "[0, tek kullanım doğal]" if e.get("serbest") else f"[{e['agirlik']}]"


def karsilastirma_metni(k: Dict) -> str:
    s = ["ÖNCE / SONRA KARŞILAŞTIRMASI", "", f"  {'Ölçüt':<24}{'Önce':>10}{'Sonra':>10}"]
    for ad, a, b in k["tablo"]:
        s.append(f"  {ad:<24}{a!s:>10}{b!s:>10}")
    if k["kalan_kaliplar"]:
        s += ["", "Taslakta kalan kalıplar:"]
        s += [f"  {_agirlik_etiketi(e)} s.{e['satir']} \"{e['metin']}\" → {e['oneri']}" for e in k["kalan_kaliplar"]]
    else:
        s += ["", "Taslakta kalıp eşleşmesi yok."]
    if k["sonra"]["oneriler"]:
        s += ["", "Taslak için kalan öneriler:"] + [f"  - {o}" for o in k["sonra"]["oneriler"]]
    if k["uyarilar"]:
        s += ["", "Anlam koruma uyarıları"] + [f"  ! {u}" for u in k["uyarilar"]]
    else:
        s += ["", "Anlam koruma: sayılar ve özel adlar korunmuş görünüyor."]
    return "\n".join(s)


def kalip_listesi_metni(kaliplar: Sequence[Kalip]) -> str:
    s = []
    for kategori in dict.fromkeys(k.kategori for k in kaliplar):
        s.append(f"\n[{kategori}]")
        for k in kaliplar:
            if k.kategori == kategori:
                s.append(f"  {k.id:<30} ağırlık {k.agirlik}  {k.aciklama}")
    return "\n".join(s).lstrip("\n")


def _tr_ondalik(metin: str) -> str:
    """Rapor satırlarında ondalık ayracını Türkçe virgüle çevirir.

    Kullanıcı metninden alıntı içeren ("..." ya da «...») satırlara dokunmaz. Böylece
    koruma uyarılarındaki "1.250,50" gibi sayılar metindeki yazımıyla kalır.
    """
    return "\n".join(s if ('"' in s or "«" in s) else re.sub(r"(?<=\d)\.(?=\d)", ",", s)
                     for s in metin.split("\n"))


def _uzunluk_hatasi(n: int) -> str:
    return (f"Metin çok uzun ({n} karakter, sınır {AZAMI_KARAKTER}). "
            "Belgeyi bölümlere ayırıp her bölümü ayrı ölçün.")


def _oku(yol: str) -> str:
    if yol == "-":
        veri = sys.stdin.buffer.read()
    else:
        veri = Path(yol).read_bytes()
    return veri.decode("utf-8-sig")


def main(argv: Optional[Sequence[str]] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        prog="analiz.py",
        description="Türkçe metinlerde yapay zekâ yazım imzalarını ölçer. Bir AI detektörü değildir.",
    )
    ap.add_argument("dosya", nargs="?", help="Metin dosyası ya da standart girdi için '-'")
    ap.add_argument("--uslup", default="genel", choices=sorted(USLUPLAR), help="Eşikleri üsluba göre ayarlar")
    ap.add_argument("--karsilastir", metavar="SONRA",
                    help=f"Yeniden yazılmış metinle karşılaştır. '-' verilirse kaynak ve taslak standart "
                         f"girdiden okunur ve '{AYRAC}' satırıyla ayrılır (geçici dosya gerekmez)")
    ap.add_argument("--ayrac", default=AYRAC, metavar="SATIR",
                    help=f"'--karsilastir -' kipinde kaynak ile taslağı ayıran satır (varsayılan: {AYRAC}). "
                         "Metnin kendisi bu satırı içeriyorsa başka bir ayraç verin")
    ap.add_argument("--profil", action="store_true", help="Yazarın kendi metninden ses kartı çıkar")
    ap.add_argument("--json", action="store_true", help="JSON çıktı")
    ap.add_argument("--ayrinti", action="store_true", help="Tüm kalıp eşleşmelerini göster")
    ap.add_argument("--esik", type=int, help="Puan bu değeri aşarsa 1 koduyla çık (CI için)")
    ap.add_argument("--kaliplar", action="store_true", help="Kalıp sözlüğünü listele")
    ap.add_argument("--surum", action="version", version=f"%(prog)s {SURUM}")
    args = ap.parse_args(argv)

    if args.kaliplar:
        print(kalip_listesi_metni(kaliplari_yukle()))
        return 0
    if args.karsilastir == "-" and args.dosya in (None, "-"):
        try:
            veri = _oku("-")
        except UnicodeDecodeError as hata:
            print(f"Girdi okunamadı: {hata}", file=sys.stderr)
            return 2
        if len(veri) > AZAMI_KARAKTER * 2:
            print(_uzunluk_hatasi(len(veri)), file=sys.stderr)
            return 2
        veri = normallestir(veri)
        parcalar = re.split(rf"^[ \t]*{re.escape(args.ayrac)}[ \t]*$", veri, flags=re.M)
        if len(parcalar) > 2:
            print(f"'{args.ayrac}' satırı birden fazla kez geçiyor. Kaynak ya da taslak bu satırı içeriyorsa "
                  "--ayrac ile metinde geçmeyen başka bir ayraç verin.", file=sys.stderr)
            return 2
        if len(parcalar) != 2 or not parcalar[0].strip() or not parcalar[1].strip():
            print(f"Standart girdide kaynak ile taslağı ayıran '{args.ayrac}' satırı bulunamadı "
                  "ya da iki taraftan biri boş.", file=sys.stderr)
            return 2
        k = karsilastir(parcalar[0].strip("\n"), parcalar[1].strip("\n"), args.uslup)
        print(json.dumps(k, ensure_ascii=False, indent=2) if args.json else _tr_ondalik(karsilastirma_metni(k)))
        return 1 if args.esik is not None and k["sonra"]["puan"]["toplam"] > args.esik else 0

    if not args.dosya:
        ap.error("bir dosya yolu ya da '-' verin")

    try:
        metin = _oku(args.dosya)
    except (OSError, UnicodeDecodeError) as hata:
        print(f"Dosya okunamadı: {hata}", file=sys.stderr)
        return 2
    if len(metin) > AZAMI_KARAKTER:
        print(_uzunluk_hatasi(len(metin)), file=sys.stderr)
        return 2

    if args.profil:
        kart = ses_karti(metin)
        print(json.dumps(kart, ensure_ascii=False, indent=2) if args.json else _tr_ondalik(ses_karti_metni(kart)))
        return 0

    if args.karsilastir:
        try:
            sonra = _oku(args.karsilastir)
        except (OSError, UnicodeDecodeError) as hata:
            print(f"Dosya okunamadı: {hata}", file=sys.stderr)
            return 2
        if len(sonra) > AZAMI_KARAKTER:
            print(_uzunluk_hatasi(len(sonra)), file=sys.stderr)
            return 2
        k = karsilastir(metin, sonra, args.uslup)
        print(json.dumps(k, ensure_ascii=False, indent=2) if args.json else _tr_ondalik(karsilastirma_metni(k)))
        puan = k["sonra"]["puan"]["toplam"]
    else:
        m = analiz_et(metin, args.uslup)
        print(json.dumps(m, ensure_ascii=False, indent=2) if args.json else _tr_ondalik(rapor_metni(m, args.ayrinti)))
        puan = m["puan"]["toplam"]

    if args.esik is not None and puan > args.esik:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""analiz.py ve kaliplar.json için testler.

Çalıştırma:  python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import contextlib
import io
import json
import re
import sys
import tempfile
import time
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "scripts"))

import analiz  # noqa: E402

FIKSTUR = KOK / "tests" / "fixtures"
CIFTLER = ("blog", "linkedin", "akademik", "eposta", "haber", "edebi", "resmi")
USLUP = {"blog": "deneme", "linkedin": "profesyonel", "akademik": "akademik",
         "eposta": "profesyonel", "haber": "gazetecilik", "edebi": "edebi", "resmi": "resmi"}


def oku(ad: str) -> str:
    return (FIKSTUR / ad).read_text(encoding="utf-8")


class TurkceKucukHarf(unittest.TestCase):
    def test_noktali_noktasiz_i(self):
        self.assertEqual(analiz.tr_kucuk("IŞIK İZMİR"), "ışık izmir")

    def test_uzunluk_korunur(self):
        metin = "İstanbul'da IRMAK kıyısında Çağrı"
        self.assertEqual(len(analiz.tr_kucuk(metin)), len(metin))


class CumleBolucu(unittest.TestCase):
    def test_sira_sayisi_ve_kisaltma(self):
        metin = ("19. yüzyılda Prof. Dr. Ahmet Yılmaz vb. konular yazdı. "
                 "II. Mahmut dönemi başka. Sonra herkes gitti.")
        cumleler = analiz.cumlelere_bol(metin)
        self.assertEqual(len(cumleler), 3, cumleler)
        self.assertTrue(cumleler[1].startswith("II. Mahmut"))

    def test_sayiyla_biten_cumle(self):
        self.assertEqual(len(analiz.cumlelere_bol("Katılımcı sayısı 45. Bunların çoğu öğrenciydi.")), 2)
        self.assertEqual(len(analiz.cumlelere_bol("3. Bölüm burada başlıyor. Sonra devam ediyor.")), 2)

    def test_gundelik_sozcuk_kisaltma_sanilmaz(self):
        self.assertEqual(len(analiz.cumlelere_bol("Gözlerini kapattı, sonra gör. Herkes güldü.")), 2)

    def test_bas_harf(self):
        self.assertEqual(len(analiz.cumlelere_bol("A. Yılmaz geldi. Herkes sustu.")), 2)

    def test_soru_ve_unlem(self):
        self.assertEqual(len(analiz.cumlelere_bol("Neden mi? Çünkü öyle! Bitti.")), 3)

    def test_kucuk_harfle_devam_bolunmez(self):
        self.assertEqual(len(analiz.cumlelere_bol("Saat 3.30 gibi geldi. Sonra gitti.")), 2)

    def test_tirnak_icinde_bitis(self):
        # '"Gel." dedi' bölünmez (küçük harfle devam), '"Git!" Ve' bölünür.
        self.assertEqual(len(analiz.cumlelere_bol('"Gel." dedi. Sonra "Git!" Ve gitti.')), 3)


class KalipSozlugu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.veri = json.loads((KOK / "scripts" / "kaliplar.json").read_text(encoding="utf-8"))
        cls.kaliplar = analiz.kaliplari_yukle()

    def test_alanlar_ve_benzersiz_kimlik(self):
        kimlikler = [k["id"] for k in self.veri["kaliplar"]]
        self.assertEqual(len(kimlikler), len(set(kimlikler)), "yinelenen id")
        for k in self.veri["kaliplar"]:
            for alan in ("id", "kategori", "agirlik", "desen", "aciklama", "oneri", "ornek"):
                self.assertTrue(k.get(alan), f"{k.get('id')}: '{alan}' boş")
            self.assertIn(k["kategori"], self.veri["kategoriler"], k["id"])
            self.assertIn(k["agirlik"], (1, 2, 3), k["id"])
            self.assertRegex(k["id"], r"^[a-z_]+$")

    def test_her_desen_kendi_ornegini_yakalar(self):
        for k in self.kaliplar:
            with self.subTest(kalip=k.id):
                self.assertIsNotNone(k.desen.search(analiz.tr_kucuk(k.ornek)),
                                     f"{k.id} kendi örneğini yakalamıyor: {k.ornek!r}")

    def test_cekimli_bicimler(self):
        """Ünlü daralması (arala→aralıyor) ve ünsüz yumuşaması (güç→gücü, et→ediyor)."""
        ornekler = {
            "ceviri_rol_oyna": "Eğitim burada kilit bir rol oynuyor.",
            "ceviri_kapilari_arala": "Kitap yeni dünyaların kapılarını aralıyor.",
            "ceviri_itici_guc": "Büyümenin itici gücü ihracat.",
            "ceviri_onem_tasi": "Bu konu büyük önem arz ediyor.",
            "sablon_veda": "Keyifli demlemeler!",
            "ceviri_kucakla": "Şirketler değişimi kucaklıyor.",
            "burokratik_sagla": "Bu yöntem avantaj sağlıyor.",
            "ceviri_potansiyel": "Potansiyelinizi keşfedin.",
            "ceviri_deneyimle": "Bu lezzeti burada deneyimliyorsunuz.",
            "ceviri_bir_sekilde": "Kaynakları etkili bir biçimde kullandık.",
            "ceviri_kapilari_arala": "Bu adım yeni bir döneme kapı aralıyor.",
            "ceviri_oneme_sahip": "Bu eser edebiyatımızda önemli bir yere sahiptir.",
            "retorik_x_degil_y": "Bu bir tercih meselesi değil, bir zorunluluk.",
        }
        kimlige_gore = {k.id: k for k in self.kaliplar}
        for kimlik, cumle in ornekler.items():
            with self.subTest(kalip=kimlik):
                self.assertIsNotNone(kimlige_gore[kimlik].desen.search(analiz.tr_kucuk(cumle)), cumle)

    def test_desenler_kucuk_harf(self):
        for k in self.veri["kaliplar"]:
            harfler = re.sub(r"\\[A-Za-z]|\[[^\]]*\]|\(\?[^)]*\)", "", k["desen"])
            self.assertEqual(harfler, analiz.tr_kucuk(harfler), f"{k['id']} büyük harf içeriyor")

    def test_dogal_cumlelerde_yanlis_alarm_yok(self):
        temiz = [
            "Kapıyı açtı ve içeri girdi.",
            "Uzay yolculuğu pahalı bir iş.",
            "Günün sonunda yorgun düştük.",
            "Kapının kilidini açtı.",
            "Deneyimleri bize çok şey öğretti.",
            "Model olarak bu arabayı seçtik.",
            "Kullanıcı deneyimi tasarımı üzerine çalışıyor.",
            "Elbette, her şey yolunda.",
            "Olağanüstü hal ilan edildi.",
            "Ankara yolculuğumuz üç saat sürdü.",
            "Hadi gidelim, geç kaldık.",
            "Yoruldun mu? diye sordu.",
            "Yolculuğunuz keyifli geçsin.",
            "On yıllık iş deneyimi var.",
            "Bu sabah erkenden çıktım, ama trafik yine de vardı.",
            "Mum ışığında yemek yedik.",
            "Köprüden geçip sola döndük.",
            "Kapının anahtarı kayboldu.",
            "Su donunca buz hâline gelir.",
            "Son yıllarda büyüyen kentlerde kira arttı.",
            "Çok çeşitli kuşlar gördük.",
            "Kayda değer bir şey olmadı.",
            "Yolculuğa çıkmadan önce lastikleri kontrol ettik.",
            "Bu yolculukta çok yorulduk.",
            "Yemeği yedi ve kalktı.",
        ]
        for cumle in temiz:
            with self.subTest(cumle=cumle):
                es = analiz.kalip_eslesmeleri(cumle, cumle, self.kaliplar)
                self.assertEqual(es, [], es)


    def test_serbest_kalibin_ilk_kullanimi_puana_girmez(self):
        m = analiz.analiz_et("Sizin için uygun mu? Perşembe saat üçte görüşebiliriz.")
        self.assertEqual([e["id"] for e in m["kaliplar"]], ["retorik_soru_cevap"])
        self.assertEqual(m["kaliplar"][0]["etkin_agirlik"], 0)
        self.assertEqual(m["puan"]["bilesenler"]["kalip"], 0)
        iki = analiz.analiz_et("Zor mu? Hayır. Pahalı mı? Biraz. Gerekli mi? Evet.")
        self.assertEqual(sum(1 for e in iki["kaliplar"] if e["etkin_agirlik"]), 2)

    def test_ascii_yazilmis_metin(self):
        metin = ("Gunumuzde yapay zeka onemli bir rol oynamaktadir. Bu baglamda sirketler yeni "
                 "araclar kullaniyor ve sonuc olarak verimlilik artiyor, calisanlar da memnun.")
        m = analiz.analiz_et(metin)
        kimlikler = {e["id"] for e in m["kaliplar"]}
        self.assertTrue({"ceviri_rol_oyna", "gecis_baglam", "sablon_gunumuzde"} <= kimlikler, kimlikler)
        self.assertTrue(any("Türkçe harfler" in u for u in m["uyarilar"]))

    def test_kotu_niyetli_girdiler_hizli(self):
        """Doğrusal olmayan regex geri izlemesi olmamalı (ReDoS)."""
        n = 40000
        girdiler = ["a" * n, " " * n, "<" * n, "](" * (n // 2), "vb. Vb. " * (n // 8),
                    "a, " * (n // 3), "a mı? " * (n // 6), '"' * n, ("a" * 200 + "\n") * (n // 200)]
        for g in girdiler:
            with self.subTest(girdi=g[:12]):
                bas = time.perf_counter()
                analiz.analiz_et(g)
                self.assertLess(time.perf_counter() - bas, 3.0)


class Olcumler(unittest.TestCase):
    def test_mektedir_sayimi(self):
        m = analiz.analiz_et("Sistem çalışmaktadır. Veriler işlenmektedir. Kullanıcılar beklemekte.")
        self.assertEqual(m["ekler"]["mektedir"], 3)

    def test_uzun_cizgi_diyalog_sayilmaz(self):
        m = analiz.analiz_et("— Geldin mi?\n— Geldim.\n\nYol uzundu — çok uzundu.")
        self.assertEqual(m["noktalama"]["uzun_cizgi"], 1)

    def test_aralik_tiresi_ara_soz_sayilmaz(self):
        m = analiz.analiz_et("Ankara - İstanbul seferi var. Pazartesi - Cuma açığız. Yol uzun - çok uzun.")
        self.assertEqual(m["noktalama"]["tire_ara_soz"], 1)

    def test_rapor_ondalik_virgul(self):
        cikti = analiz._tr_ondalik("CV 0.26 · ortalama 10.7\n  [3] s.1 \"3.5 kat\" (ceviri)")
        self.assertIn("CV 0,26", cikti)
        self.assertIn('"3.5 kat"', cikti)

    def test_noktali_virgul_ve_ic_iki_nokta(self):
        m = analiz.analiz_et("Hava güzeldi; dışarı çıktık. Asıl sorun: kimse gelmedi. Saat 14:30 idi.")
        self.assertEqual(m["noktalama"]["noktali_virgul"], 1)
        self.assertEqual(m["noktalama"]["ic_iki_nokta"], 1)

    def test_kod_ve_baglanti_maskelenir(self):
        metin = ("Bu metin temiz.\n\n```\nkritik bir rol oynamaktadır\n```\n\n"
                 "`önemli bir rol oynar` ve https://ornek.com/onemli-bir-rol-oynar")
        self.assertEqual(analiz.analiz_et(metin)["kaliplar"], [])

    def test_blok_alinti_olculmez(self):
        m = analiz.analiz_et("> Eğitim kritik bir rol oynamaktadır.\n\nBen buna katılmıyorum.")
        self.assertEqual(m["kaliplar"], [])

    def test_satir_ici_alinti_kalip_taramasina_girmez(self):
        metin = 'Bakan "Eğitim kritik bir rol oynamaktadır" dedi. Biz de katıldık.'
        m = analiz.analiz_et(metin)
        self.assertEqual(m["kaliplar"], [])
        self.assertEqual(m["ozet"]["cumle"], 2)

    def test_kendi_cumlesini_tirnaklamak_kalibi_gizlemez(self):
        metin = "Yazar bu yaklaşımı “oyunun kurallarını değiştiren, kritik bir rol oynayan” bir adım olarak görüyor."
        kimlikler = {e["id"] for e in analiz.analiz_et(metin)["kaliplar"]}
        self.assertIn("ceviri_rol_oyna", kimlikler)
        alinti = 'Bakan şunları söyledi: "Eğitim kritik bir rol oynamaktadır." Biz de katıldık.'
        self.assertEqual(analiz.analiz_et(alinti)["kaliplar"], [])

    def test_bos_ve_noktalamasiz_metin_uyarisi(self):
        self.assertIn("boş", analiz.analiz_et("")["uyarilar"][0])
        noktasiz = analiz.analiz_et("bu metinde hiç nokta yok " * 40)
        self.assertTrue(any("Cümle sınırı" in u for u in noktasiz["uyarilar"]))

    def test_kisa_dogal_metin_dusuk_puan(self):
        m = analiz.analiz_et("Ahmet Bey merhaba, yarınki toplantıyı perşembeye alabilir miyiz? Sizin için uygun mu? "
                             "Haber verirseniz takvimi güncellerim.", "profesyonel")
        self.assertLess(m["puan"]["toplam"], 25)

    def test_ritim_onerisi_yonu(self):
        kisa = analiz.analiz_et(" ".join(["Geldim. Gördüm. Yazdım. Çıktım. Döndüm."] * 3), "deneme")
        ritim = next((o for o in kisa["oneriler"] if o.startswith("Ritim")), "")
        self.assertIn("kısa cümleler baskın", ritim)

    def test_resmi_metinde_kisa_cumle_cezasi_yok(self):
        cumle = "İlgili birim talebi on beş gün içinde değerlendirerek başvuru sahibine yazılı olarak bildirir. "
        m = analiz.analiz_et(cumle * 9, "resmi")
        self.assertFalse(any("kısa cümle" in o for o in m["oneriler"]))

    def test_kalin_baslikli_madde_ve_emoji(self):
        metin = "Konular:\n\n✅ **Bir:** açıklama\n✅ **İki:** açıklama\n- **Üç:** açıklama"
        m = analiz.analiz_et(metin)
        self.assertEqual(m["yapi"]["kalin_baslikli_madde"], 3)
        self.assertEqual(m["ozet"]["liste_ogesi"], 3)

    def test_soru_basligi(self):
        m = analiz.analiz_et("## Peki, Kahve Nasıl Seçilir?\n\nÇekirdek taze olmalı.\n\n## Öğütme\n\nİnce öğüt.")
        self.assertEqual(m["yapi"]["soru_baslik"], 1)

    def test_tek_emojili_satir_paragraftir(self):
        m = analiz.analiz_et("🚀 Yeni kitabım çıktı ve çok mutluyum.\n\nHerkese teşekkürler.")
        self.assertEqual(m["ozet"]["liste_ogesi"], 0)
        self.assertEqual(m["ozet"]["paragraf"], 2)

    def test_gizli_karakter_ve_homoglif(self):
        metin = "Bu me\u200btin ins\u0430n yazmış gibi."  # U+0430 Kiril 'а'
        g = analiz.analiz_et(metin)["gizli"]
        self.assertEqual(g["gorunmez"], 1)
        self.assertEqual(g["homoglif"], 1)
        self.assertTrue(analiz.analiz_et(metin)["uyarilar"])

    def test_cakisan_eslesmede_agir_olan_kalir(self):
        metin = "Gelin birlikte bakalım."
        es = analiz.analiz_et(metin)["kaliplar"]
        self.assertEqual([e["id"] for e in es], ["asistan_gelin_bakalim"])

    def test_bilinmeyen_uslup(self):
        with self.assertRaises(ValueError):
            analiz.analiz_et("metin", "yok-boyle-uslup")


class AyirtEdicilik(unittest.TestCase):
    """Yapay zekâ çıktısı ile doğal yeniden yazımı her üslupta ayırabilmeli."""

    def test_ciftler(self):
        for ad in CIFTLER:
            with self.subTest(cift=ad):
                uslup = USLUP[ad]
                ai = analiz.analiz_et(oku(f"ai_{ad}.md"), uslup)["puan"]["toplam"]
                dogal = analiz.analiz_et(oku(f"dogal_{ad}.md"), uslup)["puan"]["toplam"]
                self.assertGreaterEqual(ai, 35, f"ai_{ad} puanı düşük: {ai}")
                self.assertLess(dogal, 20, f"dogal_{ad} puanı yüksek: {dogal}")
                self.assertGreater(ai - dogal, 25, f"{ad}: fark yetersiz ({ai} / {dogal})")

    def test_dogal_ornekler_kalip_icermez(self):
        """Üslubun hafiflettiği kategoriler (ör. resmi metinde 'gerekmektedir') hariç."""
        for ad in CIFTLER:
            with self.subTest(cift=ad):
                hafif = analiz.USLUPLAR[USLUP[ad]]["kategori_carpani"]
                es = [e for e in analiz.analiz_et(oku(f"dogal_{ad}.md"), USLUP[ad])["kaliplar"]
                      if e["kategori"] not in hafif and not e["serbest"]]
                self.assertEqual(es, [], es)


class BelgeTutarliligi(unittest.TestCase):
    """references/ornekler.md, fikstürlerle ve gerçek ölçümlerle aynı kalmalı."""

    @classmethod
    def setUpClass(cls):
        cls.belge = (KOK / "references" / "ornekler.md").read_text(encoding="utf-8")

    def test_ornek_metinler_fiksturlerle_ayni(self):
        for ad in CIFTLER:
            for onek in ("ai", "dogal"):
                with self.subTest(dosya=f"{onek}_{ad}"):
                    self.assertIn(oku(f"{onek}_{ad}.md").strip(), self.belge)

    def test_olcum_satirlari_guncel(self):
        for ad in CIFTLER:
            with self.subTest(cift=ad):
                k = analiz.karsilastir(oku(f"ai_{ad}.md"), oku(f"dogal_{ad}.md"), USLUP[ad])
                a, b = k["once"], k["sonra"]
                beklenen = (f"İmza puanı {a['puan']['toplam']} → {b['puan']['toplam']} · "
                            f"kalıp {len(analiz.etkin_kaliplar(a))} → {len(analiz.etkin_kaliplar(b))} · "
                            f"-mekte/-makta {a['ekler']['mektedir']} → {b['ekler']['mektedir']}")
                self.assertIn(f"*Ölçüm: {beklenen}", self.belge,
                              "ornekler.md içindeki ölçüm satırı güncel değil")


class SkillMeta(unittest.TestCase):
    """SKILL.md ön bilgisi ve sürüm/sayı tutarlılığı."""

    @classmethod
    def setUpClass(cls):
        metin = (KOK / "SKILL.md").read_text(encoding="utf-8")
        cls.on = re.match(r"^---\n(.*?)\n---\n", metin, re.S).group(1)
        cls.govde_satir = metin.count("\n")

    def test_on_bilgi(self):
        ad = re.search(r"^name:\s*(.+)$", self.on, re.M).group(1).strip()
        aciklama = re.search(r"^description:\s*(.+)$", self.on, re.M).group(1).strip()
        self.assertRegex(ad, r"^[a-z0-9-]{1,64}$")
        self.assertLessEqual(len(aciklama.encode("utf-8")), 1024, "bayt olarak da 1024 sınırı")
        self.assertNotRegex(aciklama, r"<[^>]+>")
        self.assertLess(self.govde_satir, 500, "SKILL.md 500 satırı aşmamalı")

    def test_surumler_ayni(self):
        skill = re.search(r'version:\s*"([^"]+)"', self.on).group(1)
        veri = json.loads((KOK / "scripts" / "kaliplar.json").read_text(encoding="utf-8"))
        self.assertEqual(skill, analiz.SURUM)
        self.assertEqual(veri["surum"], analiz.SURUM)
        self.assertIn(f"## [{analiz.SURUM}]", (KOK / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_kalip_sayisi_belgelerle_ayni(self):
        n = len(analiz.kaliplari_yukle())
        beklenen = {"README.md": rf"\b{n} kalı[pb]", "README.en.md": rf"\b{n} known patterns",
                    "CHANGELOG.md": rf"\b{n} kalıp"}
        for dosya, desen in beklenen.items():
            with self.subTest(dosya=dosya):
                self.assertRegex((KOK / dosya).read_text(encoding="utf-8"), desen)

    def test_eklenti_manifestleri(self):
        eklenti = json.loads((KOK / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        pazar = json.loads((KOK / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        ad = re.search(r"^name:\s*(.+)$", self.on, re.M).group(1).strip()
        self.assertEqual(eklenti["name"], ad)
        self.assertEqual(eklenti["version"], analiz.SURUM)
        self.assertEqual([p["name"] for p in pazar["plugins"]], [ad])
        self.assertEqual(pazar["plugins"][0]["source"], "./")
        self.assertTrue(pazar["owner"]["name"])

    def test_claude_ai_yalnizca_izinli_alanlar(self):
        """claude.ai yüklemesi bu alanlar dışındaki ön bilgi anahtarlarını reddeder."""
        anahtarlar = set(re.findall(r"^([a-z-]+):", self.on, re.M))
        self.assertLessEqual(anahtarlar, {"name", "description", "license", "compatibility",
                                          "metadata", "allowed-tools"})

    def test_readme_baglantilari(self):
        for dosya in ("README.md", "README.en.md"):
            metin = (KOK / dosya).read_text(encoding="utf-8")
            for yol in set(re.findall(r'(?:\]\(|src(?:set)?=")((?!https?:|#)[^)"#]+)', metin)):
                with self.subTest(dosya=dosya, yol=yol):
                    self.assertTrue((KOK / yol).exists(), yol)

    def test_baglantilar_var(self):
        metin = (KOK / "SKILL.md").read_text(encoding="utf-8")
        for yol in set(re.findall(r"\]\((references/[^)]+)\)", metin)):
            with self.subTest(yol=yol):
                self.assertTrue((KOK / yol).is_file(), yol)


class Karsilastirma(unittest.TestCase):
    def test_kayip_sayi_ve_ad(self):
        k = analiz.karsilastir("Satışlar 2023'te %40 arttı. Açıklamayı Ayşe Demir yaptı.",
                               "Satışlar geçen yıl arttı. Yönetim açıkladı.")
        self.assertIn("2023", k["koruma"]["kayip_sayilar"])
        self.assertIn("%40", k["koruma"]["kayip_sayilar"])
        self.assertIn("Ayşe", k["koruma"]["kayip_ozel_adlar"])

    def test_cumle_basindaki_ad(self):
        k = analiz.karsilastir("Elif eve döndü. Annesi Elif'i bekliyordu.", "Kız eve döndü. Annesi onu bekliyordu.")
        self.assertIn("Elif", k["koruma"]["kayip_ozel_adlar"])

    def test_hitap_sonrasi_ad_sanilmaz(self):
        k = analiz.karsilastir("Sayın Ahmet Bey,\n\nUmarım iyisinizdir.", "Ahmet Bey merhaba,\n\nİyi günler.")
        self.assertNotIn("Umarım", k["koruma"]["kayip_ozel_adlar"])

    def test_uydurma_sayi(self):
        k = analiz.karsilastir("Satışlar arttı.", "Satışlar %12 arttı.")
        self.assertIn("%12", k["koruma"]["yeni_sayilar"])

    def test_sayi_degeri_ve_bicimi(self):
        k = analiz.koruma_kontrolu("Oran %15, tutar 1.250,50 TL, bütçe 2 milyon lira, üç kişi.",
                                   "Oran yüzde 15, tutar 1250,50 TL, bütçe 2.000.000 lira, 3 kişi.")
        self.assertEqual((k["kayip_sayilar"], k["yeni_sayilar"]), ([], []))

    def test_sayi_degisimi_yakalanir(self):
        k = analiz.koruma_kontrolu("Toplantıya üç kişi katıldı, bütçe 2 milyon.",
                                   "Toplantıya beş kişi katıldı, bütçe 2 milyar.")
        self.assertEqual(set(k["kayip_sayilar"]), {"üç", "2 milyon"})
        self.assertEqual(set(k["yeni_sayilar"]), {"beş", "2 milyar"})

    def test_tekrar_eden_sayinin_kaybi(self):
        k = analiz.koruma_kontrolu("Süre 3 gün, ardından 3 hafta.", "Süre 3 gün, ardından bir süre.")
        self.assertEqual(k["azalan_sayilar"], ["3 (2 → 1)"])

    def test_kisaltma_ve_sozcuk_siniri(self):
        k = analiz.koruma_kontrolu("Verileri TÜİK açıkladı, yorumu Ece Kaya yaptı.",
                                   "Verileri kurum açıkladı, yorumu bir mece yaptı.")
        self.assertIn("TÜİK", k["kayip_ozel_adlar"])
        self.assertIn("Ece", k["kayip_ozel_adlar"])
        self.assertNotIn("II", analiz._ozel_adlar("Bu II. Mahmut dönemidir."))

    def test_unvan_kisaltmasi_ad_sayilmaz(self):
        k = analiz.koruma_kontrolu("Toplantıda Dr. Ayşe Kaya konuştu.", "Toplantıda Ayşe Kaya konuştu.")
        self.assertEqual(k["kayip_ozel_adlar"], [])

    def test_uyarida_sayi_yazimi_bozulmaz(self):
        k = analiz.karsilastir("Fiyat 1.250,50 TL, sürüm 3.2.1 oldu.", "Fiyat uygun.")
        metin = analiz._tr_ondalik(analiz.karsilastirma_metni(k))
        self.assertIn("«1.250,50»", metin)
        self.assertIn("«3.2.1»", metin)

    def test_ekli_ozel_ad_korunmus_sayilir(self):
        k = analiz.karsilastir("Toplantı Ankara'da yapıldı.", "Toplantıyı Ankara'daki ofiste yaptık.")
        self.assertEqual(k["koruma"]["kayip_ozel_adlar"], [])


class SesKarti(unittest.TestCase):
    def test_alanlar(self):
        kart = analiz.ses_karti(oku("dogal_blog.md"))
        for alan in ("cumle_ortalama", "cumle_cv", "soylem_belirtecleri_1000", "sik_acilislar"):
            self.assertIn(alan, kart)
        self.assertGreater(kart["cumle"], 5)
        self.assertIn("SES KARTI", analiz.ses_karti_metni(kart))


class KomutSatiri(unittest.TestCase):
    def calistir(self, *argv):
        cikti = io.StringIO()
        with contextlib.redirect_stdout(cikti):
            kod = analiz.main(list(argv))
        return kod, cikti.getvalue()

    def test_json(self):
        kod, cikti = self.calistir(str(FIKSTUR / "ai_blog.md"), "--json")
        self.assertEqual(kod, 0)
        self.assertIn("puan", json.loads(cikti))

    def test_esik(self):
        kod, _ = self.calistir(str(FIKSTUR / "ai_blog.md"), "--esik", "30")
        self.assertEqual(kod, 1)
        kod, _ = self.calistir(str(FIKSTUR / "dogal_blog.md"), "--esik", "30")
        self.assertEqual(kod, 0)

    def test_karsilastirma_ve_profil(self):
        kod, cikti = self.calistir(str(FIKSTUR / "ai_blog.md"), "--karsilastir", str(FIKSTUR / "dogal_blog.md"))
        self.assertEqual(kod, 0)
        self.assertIn("KARŞILAŞTIRMA", cikti)
        kod, cikti = self.calistir(str(FIKSTUR / "dogal_blog.md"), "--profil")
        self.assertIn("SES KARTI", cikti)

    def calistir_girdiyle(self, girdi, *argv):
        cikti, hata = io.StringIO(), io.StringIO()
        eski = sys.stdin
        sys.stdin = io.TextIOWrapper(io.BytesIO(girdi.encode("utf-8")), encoding="utf-8")
        try:
            with contextlib.redirect_stdout(cikti), contextlib.redirect_stderr(hata):
                kod = analiz.main(list(argv))
        finally:
            sys.stdin = eski
        return kod, cikti.getvalue(), hata.getvalue()

    def test_tek_akista_karsilastirma(self):
        girdi = oku("ai_blog.md") + "\n===TASLAK===\n" + oku("dogal_blog.md")
        kod, cikti, _ = self.calistir_girdiyle(girdi, "--karsilastir", "-", "--json")
        self.assertEqual(kod, 0)
        k = json.loads(cikti)
        self.assertGreater(k["once"]["puan"]["toplam"], k["sonra"]["puan"]["toplam"])
        self.assertEqual(k["kalan_kaliplar"], [])

    def test_tek_akista_ayrac_yoksa_hata(self):
        kod, _, hata = self.calistir_girdiyle("Ayraçsız bir metin.", "--karsilastir", "-")
        self.assertEqual(kod, 2)
        self.assertIn("===TASLAK===", hata)

    def test_ayrac_iki_kez_gecerse_hata(self):
        girdi = "Kaynak.\n===TASLAK===\nAra.\n===TASLAK===\nTaslak."
        kod, _, hata = self.calistir_girdiyle(girdi, "--karsilastir", "-")
        self.assertEqual(kod, 2)
        self.assertIn("--ayrac", hata)

    def test_ozel_ayrac_ve_crlf(self):
        girdi = "Kaynakta ===TASLAK=== yazıyor.\r\n@@AYRAC_7Q@@\r\nTaslakta da yazıyor.\r\n"
        kod, cikti, _ = self.calistir_girdiyle(girdi, "--karsilastir", "-", "--ayrac", "@@AYRAC_7Q@@", "--json")
        self.assertEqual(kod, 0)
        self.assertIn("KARŞILAŞTIRMA", analiz.karsilastirma_metni(json.loads(cikti)))
        kod, _, _ = self.calistir_girdiyle("Kaynak.\r\n===TASLAK===\r\nTaslak.\r\n", "--karsilastir", "-")
        self.assertEqual(kod, 0)

    def test_profil_standart_girdiden(self):
        kod, cikti, _ = self.calistir_girdiyle(oku("dogal_blog.md"), "-", "--profil")
        self.assertEqual(kod, 0)
        self.assertIn("SES KARTI", cikti)

    def test_cok_uzun_girdi_reddedilir(self):
        kod, _, hata = self.calistir_girdiyle("a " * (analiz.AZAMI_KARAKTER // 2 + 10), "-")
        self.assertEqual(kod, 2)
        self.assertIn("bölüm", hata)

    def test_skill_md_komutlari_gecerli(self):
        """SKILL.md'deki her analiz.py komutu betiğin gerçek seçenekleriyle uyumlu olmalı."""
        skill = (KOK / "SKILL.md").read_text(encoding="utf-8")
        komutlar = re.findall(r"analiz\.py[^\n`]*", skill)
        self.assertTrue(komutlar)
        yardim = io.StringIO()
        with contextlib.redirect_stdout(yardim), self.assertRaises(SystemExit):
            analiz.main(["--help"])
        for komut in komutlar:
            for secenek in re.findall(r"(?<!\S)--[a-z]+", komut):
                with self.subTest(komut=komut, secenek=secenek):
                    self.assertIn(secenek, yardim.getvalue())
            for uslup in re.findall(r"--uslup\s+([a-z]+)", komut):
                self.assertIn(uslup, analiz.USLUPLAR)

    def test_skill_md_heredoc_guvenli(self):
        """Sabit bir heredoc sınırlayıcısı, metindeki bir satırın komut olarak çalışmasına yol açar."""
        skill = (KOK / "SKILL.md").read_text(encoding="utf-8")
        kod = "\n".join(re.findall(r"```bash\n(.*?)```", skill, re.S))
        sinirlayicilar = re.findall(r"<<-?\s*(\S+)", kod)
        self.assertTrue(sinirlayicilar)
        for s in sinirlayicilar:
            with self.subTest(sinirlayici=s):
                self.assertRegex(s, r"^'METIN_[A-Za-z0-9]{8}'$", "tırnaklı ve rastgele görünümlü olmalı")
        self.assertEqual(len(set(sinirlayicilar)), len(sinirlayicilar), "örnekler aynı sınırlayıcıyı tekrarlamamalı")
        self.assertIn("${CLAUDE_SKILL_DIR}/scripts/analiz.py", skill)
        self.assertRegex(skill, r"(?m)^allowed-tools: Bash\(python3 \$\{CLAUDE_SKILL_DIR\}/scripts/analiz\.py \*\)$")

    def test_kalip_listesi(self):
        kod, cikti = self.calistir("--kaliplar")
        self.assertEqual(kod, 0)
        self.assertIn("ceviri_rol_oyna", cikti)

    def test_bom_ve_crlf(self):
        with tempfile.NamedTemporaryFile("wb", suffix=".txt", delete=False) as f:
            f.write("\ufeffBirinci cümle.\r\nİkinci cümle.\r\n".encode("utf-8"))
        try:
            kod, cikti = self.calistir(f.name, "--json")
            self.assertEqual(json.loads(cikti)["ozet"]["cumle"], 2)
            self.assertEqual(json.loads(cikti)["gizli"]["gorunmez"], 0)
        finally:
            Path(f.name).unlink()

    def test_olmayan_dosya(self):
        with contextlib.redirect_stderr(io.StringIO()):
            kod, _ = self.calistir("/yok/boyle/bir/dosya.txt")
        self.assertEqual(kod, 2)


if __name__ == "__main__":
    unittest.main()

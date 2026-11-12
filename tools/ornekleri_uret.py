#!/usr/bin/env python3
"""references/ornekler.md dosyasını test metinlerinden ve gerçek ölçümlerden üretir.

Örnek metinler tests/fixtures/ altındaki ai_*.md ve dogal_*.md dosyalarıdır.
"Ne değişti" açıklamaları aşağıdadır. Ölçüm satırları her çalıştırmada
analiz.py ile yeniden hesaplanır, böylece belge ile kod arasında kayma olmaz.

Kullanım:  python3 tools/ornekleri_uret.py
"""
from __future__ import annotations

import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "scripts"))

import analiz  # noqa: E402

FIKSTUR = KOK / "tests" / "fixtures"

# (ad, üslup, yoğunluk, başlık, ne değişti, sana kalan)
ORNEKLER = [
    ("blog", "deneme", "orta", "Uzaktan çalışma üzerine blog yazısı", [
        "\"Günümüzde ... ayrılmaz bir parçası haline gelmiştir\" şablon girişi düz bir saptamaya indi: \"artık gündelik hayatın parçası\".",
        "\"Sadece avantajları değil, aynı zamanda bazı zorlukları\" kalıbı \"avantajlarının yanında bazı zorlukları da var\" oldu. \"Bazı\" korundu.",
        "Sekiz \"-mekte/-makta\" yüklemi \"-iyor\" ve geniş zamana çevrildi. Olasılık ifadeleri korundu: "
        "\"etkileyebilmektedir\" → \"zarar görebiliyor\", \"yol açabilmektedir\" → \"yol açabilir\", \"neden olabilmektedir\" → \"zayıflatabiliyor\".",
        "\"Öncelikle / Bunun yanı sıra / Bu bağlamda / Sonuç olarak\" iskeleti kaldırıldı. \"Bu bağlamda\" gerçek bir bağa (\"bu yüzden\") dönüştü.",
        "\"Kritik bir rol oynamaktadır\" → \"çok önemli\", \"etkili bir şekilde\" → \"etkili\". \"Büyük fırsatlar sunmaktadır\" fırsat olarak kaldı (\"büyük fırsatlar barındırıyor\"), kesin bir kazanca çevrilmedi.",
        "Cümle boyları açıldı (CV 0,26 → 0,48). Kısalma silinen kalıplardan geliyor. Yeni bilgi eklenmedi.",
    ], ["Kendi ekibinden ya da deneyiminden tek bir somut örnek verirsen ikinci paragrafa işlerim. Yazıyı en çok bu kişiselleştirir."]),
    ("linkedin", "profesyonel", "derin (yapıya dokunuldu)", "Kitap duyurusu, LinkedIn gönderisi", [
        "\"Paylaşmaktan mutluluk duyuyorum\" açılışı atıldı. Gönderi doğrudan haberle başlıyor.",
        "\"Uzun soluklu bir yolculuğun ardından\" yerine \"uzun süredir üzerinde çalıştığım\".",
        "\"Sadece bir rehber değil, aynı zamanda ... kapılarını aralayan kapsamlı bir kaynak\" iddiası iki parçasıyla korundu: "
        "\"Bir rehber olarak yazdım ama veri odaklı düşünmeye kapsamlı bir giriş olarak da okunabilir.\"",
        "✅ ve kalın etiketli maddeler sade maddelere dönüştü (derin yoğunlukta yapısal değişiklik). Madde içerikleri korundu, \"ilham verici\" sıfatı atıldı.",
        "\"Kariyer yolculuğunuzda size değerli içgörüler sunacağına\" → \"kariyerinizde işinize yarayacak fikirler vereceğine\". Okura söz verilen şey aynı.",
        "Altı emoji ve üç ünlem kaldırıldı, etiketler korundu. Kelime sayısındaki düşüş silinen kalıplardan ve emojilerden geliyor.",
    ], []),
    ("akademik", "akademik", "orta", "Literatür değerlendirmesi paragrafı", [
        "\"Bu bağlamda / Söz konusu / Öte yandan / Dolayısıyla\" zinciri kaldırıldı. Tek bağ olarak \"Bu nedenle\" kaldı.",
        "Dört \"-mektedir\" yükleminden biri kaldı, diğerleri \"-mıştır\" ve ad cümlesine döndü. Akademik üslupta ölçülü kullanım doğaldır.",
        "\"Giderek artan bir ilgi görmektedir\" → \"giderek daha çok ilgi görmektedir\". Literatür özne olmaktan çıktı, ilgi gören konu oldu.",
        "\"Potansiyeline sahip olduğu da göz ardı edilmemelidir\" → \"kaynağı olabileceği de dikkate alınmalıdır\". Olasılık ve uyarı tonu korundu.",
        "Terimler (psikolojik iyi oluş, boylamsal) ve iddiaların kapsamı korundu. Atıf ya da bulgu eklenmedi.",
    ], []),
    ("eposta", "profesyonel", "orta", "Bütçe onayı e-postası", [
        "\"Umarım bu e-posta sizi iyi bulur\" ve \"iletişime geçmekten çekinmeyiniz\" çeviri kalıpları atıldı. Kapanışta tek ve sade bir cümle kaldı.",
        "\"Sayın Ahmet Bey\" yerine iş yazışmasında yaygın olan \"Ahmet Bey merhaba\". Kurum kültürü daha resmiyse eski hitap korunur.",
        "\"Toplantıda belirtildiği üzere\" → \"Toplantıda da belirtildiği gibi\". Atıf edilgen kaldı, \"biz\"e çevrilmedi.",
        "\"Başarılı bir şekilde tamamlanabilmesi için ... en kısa sürede sağlanması büyük önem arz etmektedir\" → "
        "\"başarıyla tamamlayabilmemiz için bütçe onayının bir an önce çıkması çok önemli\". Önem derecesi ve aciliyet aynı.",
        "Tarihler (15 Kasım, 20 Kasım) ve talep aynı. Kelime sayısındaki düşüş silinen kalıplardan geliyor, içerik kaybı yok.",
    ], []),
    ("haber", "gazetecilik", "orta", "Faiz kararı haberi", [
        "\"Büyük bir yankı uyandırdı\" neredeyse aynen kaldı (yalnızca virgül ve \"bir\" atıldı). Kalıp olmayan bir ifadeyi eş anlamlısıyla değiştirmeye gerek yok.",
        "\"Kritik bir rol oynayacağını ifade ederken\" → \"belirleyici olacağını söyledi\". Nötr söyleme fiili nötr kaldı, atıf (ekonomistlerin tümü) korundu.",
        "\"Konusunda uyarılarda bulundu\" → \"konusunda uyardı\". Uzun cümle ikiye bölündü, geçmiş zaman korundu.",
        "\"Önemli ölçüde şekillendirecek gibi görünmektedir\" → \"büyük ölçüde belirleyecek gibi görünüyor\". Etkinin derecesi ve belirsizlik korundu.",
        "\"Merkez Bankası'nın\" TDK kuralına göre \"Merkez Bankasının\" yazıldı: kurum adlarına gelen ekler kesmeyle ayrılmaz. Yayın kuralın farklıysa kaynaktaki gibi bırakılır.",
    ], ["Faiz oranı, karar tarihi ve yorum yapan ekonomistlerin adları metni hem güçlendirir hem de şablon hissini kırar. Bunları verirsen eklerim."]),
    ("edebi", "edebi", "orta", "Öyküden bir paragraf", [
        "\"Adeta bir örtü gibi\" klişe benzetmesi ve \"o eşsiz anlar\"daki abartı çıkarıldı. \"O anlar\"daki gösterme sözcüğü duyguyu taşıyor.",
        "\"Geçmişin hatıralarıyla dolu zihninde kaybolmuştu\" → \"geçmişin anıları arasında kaybolup gitmişti\".",
        "\"Kalbinde tarif edilemez bir hüzün vardı\" duygu bildirimi beden duyumuna çevrildi: \"İçi burkuluyordu.\" Anlatı zamanı korundu.",
        "Noktalı virgül ve \"ama aynı zamanda\" yerine iki cümle. \"Umudun ışığı\" klişesi sade bir cümleye indi, \"hâlâ\" korundu.",
        "Karakter, mekân, zaman ve olay aynı kaldı. Kısalma silinen klişelerden geliyor. Yeni sahne, ayrıntı ya da anı eklenmedi.",
    ], ["Yağmurun sesi, odadaki bir koku ya da annesine dair tek bir somut nesne sahneyi çok daha canlı kılar. Bunu senin kurgundan alalım."]),
    ("resmi", "resmi", "hafif", "Kurum içi bilgi güvenliği duyurusu", [
        "\"Büyük önem arz etmektedir\" → \"çok önemlidir\". Önem derecesi korundu, zorunluluğa çevrilmedi.",
        "\"Bu bağlamda\" ve \"Bunun yanı sıra\" kaldırıldı, \"Söz konusu kurallara\" → \"Bu kurallara\".",
        "\"Gerekmektedir\" ve resmi hitap üslubun gereği olarak korundu. Sayılar, tarih ve birim adı aynı.",
        "\"İletişime geçmekten çekinmeyiniz\" → \"Sorularınızı Bilgi İşlem birimine iletebilirsiniz.\" TDK'ya göre \"halinde\" → \"hâlinde\", \"işbirliği\" → \"iş birliği\".",
        "Hafif yoğunlukta cümle yapısı büyük ölçüde korundu. Metnin hukuk ya da İK onayından geçmesi gerekiyorsa bu adım atlanmamalı.",
    ], []),
]

KOTU_ORNEK = (
    "Merkez Bankasının faiz kararı piyasada adeta deprem etkisi yarattı, yani ortalık bir anda karıştı işte. "
    "Zaten ekonomistlerin bir kısmı bu işin suyunun çıktığını, enflasyonun artık köşeye sıkıştığını düşünüyor. "
    "Bazı uzmanlarsa hani şu meşhur büyüme var ya, onun bundan pek hoşlanmayacağını söylüyor! "
    "Yatırımcılar mı? Onlar da diken üstünde, ne olacak diye bekleşip duruyorlar."
)


def oku(ad: str) -> str:
    return (FIKSTUR / ad).read_text(encoding="utf-8").strip()


def olcum_satiri(ad: str, uslup: str) -> str:
    k = analiz.karsilastir(oku(f"ai_{ad}.md"), oku(f"dogal_{ad}.md"), uslup)
    a, b = k["once"], k["sonra"]
    s = (f"İmza puanı {a['puan']['toplam']} → {b['puan']['toplam']} · "
         f"kalıp {len(analiz.etkin_kaliplar(a))} → {len(analiz.etkin_kaliplar(b))} · "
         f"-mekte/-makta {a['ekler']['mektedir']} → {b['ekler']['mektedir']}")
    if a["ozet"]["cumle"] >= 5 and b["ozet"]["cumle"] >= 5:
        hedef = analiz.USLUPLAR[uslup]["cv_hedef"]
        s += f" · cümle CV {a['ritim']['cv']} → {b['ritim']['cv']} (hedef ≥ {hedef:.2f})".replace(".", ",")
    s += f" · kelime {a['ozet']['kelime']} → {b['ozet']['kelime']}"
    if not (a["puan"]["guvenilir"] and b["puan"]["guvenilir"]):
        s += " · kısa metin, puanlar yalnızca yön gösterir"
    return s


def uret() -> str:
    s = [
        "# Örnekler", "",
        "Her örnek, tipik bir yapay zekâ çıktısının önce ve sonra hâlidir. \"Sonra\" metinleri skill'in kurallarına göre "
        "elle hazırlanmış başvuru yeniden yazımlarıdır ve `tests/fixtures/` klasöründeki test metinleriyle birebir aynıdır. Ölçüm satırları `analiz.py --karsilastir` ile hesaplanır. Bu dosya "
        "`tools/ornekleri_uret.py` ile üretilir, elle düzenlenmez.", "",
        "Örneklerde dikkat edilecek ilke: kaynaktaki her iddia, nicelik (\"birçok\", \"bazı\"), olasılık ifadesi "
        "(\"-ebilir\", \"gibi görünüyor\") ve zaman kipi korunur. Yeniden yazım üslubu değiştirir, iddiayı değiştirmez.", "",
        "Örnekler aynı zamanda varsayılan teslim biçimini gösterir: kısa bir üslup satırı, metin, \"Ne değişti\" ve "
        "yalnızca gerçekten işe yarayacaksa \"Sana kalan\".", "",
        "## İçindekiler", "",
    ]
    s += [f"{i}. {o[3]} ({o[1]})" for i, o in enumerate(ORNEKLER, 1)]
    s += [f"{len(ORNEKLER) + 1}. Aşırı düzeltme: nasıl yapılmaz", ""]
    for i, (ad, uslup, yog, baslik, degisti, kalan) in enumerate(ORNEKLER, 1):
        s += [f"## {i}. {baslik}", "", "### Önce", "", "````markdown", oku(f"ai_{ad}.md"), "````", "",
              "### Sonra", "", f"**Üslup:** {uslup} · **Yoğunluk:** {yog}", "",
              "````markdown", oku(f"dogal_{ad}.md"), "````", "", "**Ne değişti**", ""]
        s += [f"- {d}" for d in degisti] + [""]
        if kalan:
            s += ["**Sana kalan**", ""] + [f"- {x}" for x in kalan] + [""]
        s += [f"*Ölçüm: {olcum_satiri(ad, uslup)}*", ""]
    s += [
        f"## {len(ORNEKLER) + 1}. Aşırı düzeltme: nasıl yapılmaz", "",
        "Aynı haber metninin kötü bir \"insanlaştırılmış\" hâli:", "",
        "````markdown", KOTU_ORNEK, "````", "",
        "**Neden yanlış**", "",
        "- Gazetecilik üslubuna konuşma dili ve belirteç yağmuru (yani, işte, zaten, hani) sokulmuş.",
        "- Üç deyim üst üste (suyunun çıkması, köşeye sıkışmak, diken üstünde). İnsanlaştırıcı imzası.",
        "- Kaynakta olmayan iddialar eklenmiş: \"deprem etkisi\", \"enflasyon köşeye sıkıştı\", yatırımcıların \"diken üstünde\" olduğu.",
        "- Nicelik değişmiş: kaynakta \"ekonomistler\" var, burada \"ekonomistlerin bir kısmı\".",
        "- \"Yatırımcılar mı? Onlar da...\" soru-cevap kalıbı ve ünlem haberin ciddiyetini bozuyor.",
        "- \"Adeta\" kalmış. Kalıp temizlenmeden üstüne süs eklenmiş.",
        "",
        "Doğru hâli 5. örnektedir. İnsan sesi araçları üsluba göre dozlanır. Gazetecilikte olgu önce gelir, süs hiç gelmez.",
        "",
    ]
    return "\n".join(s)


def main() -> int:
    hedef = KOK / "references" / "ornekler.md"
    hedef.write_text(uret(), encoding="utf-8")
    print(f"{hedef.relative_to(KOK)} güncellendi")
    for ad, uslup, *_ in ORNEKLER:
        print(f"  {ad:10} {olcum_satiri(ad, uslup)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

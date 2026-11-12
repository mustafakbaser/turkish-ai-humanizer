# Katkı Rehberi

Katkılarınızı bekliyoruz. En değerli katkılar şunlar:

- Türkçe yapay zekâ metinlerinde fark ettiğiniz yeni bir kalıp
- Doğal bir cümlede yanlış alarm veren bir desen
- Yeni bir üslupta önce/sonra örneği
- Eşik kalibrasyonu için lisansı açık insan metinleri

## Yeni kalıp eklemek

Kalıplar `scripts/kaliplar.json` dosyasındadır. Her kalıp şu alanları taşır:

```json
{
  "id": "ceviri_deger_kat",
  "kategori": "ceviri",
  "agirlik": 2,
  "desen": "değer kat\\w*",
  "aciklama": "'Add value' çevirisi.",
  "oneri": "Ne kazandırdığını söyle: 'işe hız katar', 'müşteri getirir'.",
  "ornek": "Ekibimize değer katacak adaylar arıyoruz."
}
```

- **id:** küçük harf ve alt çizgi, kategoriyle başlar.
- **kategori:** dosyanın başındaki `kategoriler` listesinden biri.
- **agirlik:** 1 (zayıf işaret, insanlar da sık kullanır), 2 (belirgin), 3 (neredeyse yalnızca yapay zekâ).
- **desen:** Türkçe küçük harfe çevrilmiş metin üzerinde çalışan bir Python regex'i. Desende büyük harf kullanmayın.
- **ornek:** desenin yakalaması gereken gerçekçi bir cümle. Testler bunu zorunlu tutar.
- **serbest** (isteğe bağlı): bir metinde ilk kaç eşleşmenin doğal sayılıp puana girmeyeceği. Bir kez geçtiğinde insan yazısında da olağan olan ifadeler için `1` verin ("anlamına gelir", "ilk olarak").

### Hız

Desen doğrusal sürede çalışmalı. `\w+ kalbinde` gibi sözcük başı sınırı olmayan bir desen, uzun tek bir sözcükte karesel geri izlemeye düşer. Böyle desenleri `(?<![^\W\d_])` ile sözcük başına bağlayın, değişken uzunluklu tekrarlara üst sınır koyun (`{0,40}`). `test_kotu_niyetli_girdiler_hizli` testi bunu denetler.

### Türkçe çekimlere dikkat

Desenler çekimli biçimleri de yakalamalı. En sık atlanan durumlar:

| Olay | Örnek | Desen |
|---|---|---|
| Ünlü daralması | arala + -yor → aralıyor, oyna + -yor → oynuyor | `aral[aı]\w*`, `oyn[aıu]\w*` |
| Ünsüz yumuşaması | güç → gücü | `gü[çc]\w*` |
| t/d değişimi | et → ediyor, keşfet → keşfedin | `e[td]\w*`, `keşfe[td]` |
| Çoğul ile fiil karışması | deneyimler (ad) / deneyimle (fiil) | fiil eklerini açıkça yazın |

### Yanlış alarm kontrolü

Yeni bir desen eklediğinizde, desenin yakalamaması gereken doğal bir cümleyi `tests/test_analiz.py` içindeki `test_dogal_cumlelerde_yanlis_alarm_yok` listesine ekleyin. Örneğin "kapılarını aralamak" mecazı için "Kapıyı açtı ve içeri girdi." cümlesi.

## Testler

```bash
python3 -m unittest discover -s tests -v
```

Testler Python 3.9 ve üstünde, ek bağımlılık olmadan çalışır. Kalıp ağırlıklarını ya da eşikleri değiştirirseniz `references/ornekler.md` içindeki ölçüm satırları güncelliğini yitirir. Test bunu yakalar. Belgeyi `python3 tools/ornekleri_uret.py` ile yeniden üretin.

## Örnek eklemek

1. `tests/fixtures/ai_<ad>.md` ve `tests/fixtures/dogal_<ad>.md` dosyalarını ekleyin. Doğal metin kaynaktaki her iddiayı, sayıyı, adı, nicelik sözcüğünü, olasılık ifadesini ve zamanı korumalı. Yeni olgu ya da genelleme eklememeli.
2. `tests/test_analiz.py` içindeki `CIFTLER` ve `USLUP` sözlüklerine ekleyin.
3. Açıklamaları `tools/ornekleri_uret.py` içindeki `ORNEKLER` listesine ekleyin ve betiği çalıştırın.

## Belge yazım kuralları

Bu repodaki belgeler skill'in kendi kurallarına uyar: ara söz için uzun çizgi yok, düz yazıda noktalı virgül yok, şablon giriş ve kapanış yok. Kurala aykırı yapılar yalnızca yapay zekâ örneği olarak, tırnak ya da kod bloğu içinde yer alır.

SKILL.md 500 satırın altında kalmalı. Ayrıntılar `references/` altına gider ve SKILL.md'den bir düzey derinlikte bağlanır.

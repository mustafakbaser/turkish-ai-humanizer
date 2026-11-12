# Değişiklik Günlüğü

Biçim [Keep a Changelog](https://keepachangelog.com/tr-TR/1.1.0/), sürümleme [Semantic Versioning](https://semver.org/lang/tr/) esaslıdır.

## [1.0.0] - 2026-11-12

İlk sürüm.

### Eklendi

- Yedi adımlı iş akışı: teşhis, ölçüm, anlam iskeleti, yeniden kurma, insan sesi, denetim, teslim.
- Yedi üslup (resmi, akademik, profesyonel, gazetecilik, deneme, edebi, genel) ve üç yoğunluk düzeyi (hafif, orta, derin).
- Dört çıktı biçimi: varsayılan, sadece metin, rapor, yalnızca teşhis.
- Çeviri ve sıfırdan yazım modları.
- `scripts/analiz.py`: bağımlılıksız ölçüm aracı. İmza puanı, ritim (CV), ek yükü, geçiş açılışları, noktalama, yapı, gizli karakter ve homoglif taraması, önce/sonra karşılaştırması, sayı ve özel ad koruma kontrolü, ses kartı, JSON çıktı ve CI eşiği.
- `scripts/kaliplar.json`: sekiz kategoride 118 kalıp. Her biri açıklama, onarım önerisi ve testle doğrulanan örnek cümle taşır. Bir kez geçtiğinde doğal olan kalıplar (`serbest`) ilk kullanımda puana girmez. Türkçe harfler olmadan yazılmış metinlerde kalıplar ASCII karşılıklarıyla aranır.
- Referans belgeleri: kalıp sözlüğü, yapısal imzalar, insan sesi ve doz tablosu, üsluplar, noktalama ve yazım, tespit mekanizmaları, altı üslupta yedi önce/sonra örneği (`tools/ornekleri_uret.py` ile üretilir).
- Birim testleri ve Python 3.9 / 3.11 / 3.13 üzerinde CI.
- `tools/paketle.py`: claude.ai ve Claude Desktop için ZIP paketi.
- `tools/ornekleri_uret.py`: örnek belgesini test metinlerinden ve gerçek ölçümlerden üretir.
- Claude Code eklenti pazarı manifestleri (`.claude-plugin/`). Tek komutla kurulum: `/plugin install turkish-ai-humanizer --marketplace mustafakbaser/turkish-ai-humanizer`.
- Etiket atıldığında testleri çalıştırıp ZIP paketini Release'e ekleyen iş akışı.
- Türkçe ve İngilizce README, logo, açık ve koyu tema bantları, sosyal önizleme görseli.
- Issue formları (yeni kalıp, yanlış alarm, hata), PR şablonu ve güvenlik politikası.
- Sadakat kuralları: olasılık, nicelik, zaman, önem ve zorunluluk derecesi korunur. Süs (senaryo, ortam, duygu yorumu, pekiştireç) yeni içerik sayılır. Haber dilinde söyleme fiillerinin tonu korunur.
- "Canlılığı içerikten değil biçimden al" ilkesi: uydurmadan doğallık için somut biçim teknikleri.
- Ölçüm adımı çıktı biçiminden bağımsız olarak zorunlu, teslim mesajında süreç anlatımı yasak.
- `--karsilastir -` kipi: kaynak ve taslak tek standart girdi akışında, `===TASLAK===` satırıyla ayrılarak karşılaştırılır. Skill geçici dosya yazmadan, tek bir `python3` komutuyla ölçer.
- Güvenlik: analiz komutları her çağrıda rastgele bir heredoc sınırlayıcısı kullanır, böylece metindeki bir satır kabuk komutu olarak çalışamaz. Yeniden yazılacak metindeki talimatlar uygulanmaz. `allowed-tools` yalnızca skill'in kendi analiz betiğine izin verir.
- Analiz aracı kötü niyetli girdilerde doğrusal sürede çalışır (ReDoS testleriyle doğrulanır) ve 400.000 karakterden uzun girdiyi reddeder.
- Anlam koruma: sayılar değerleriyle ve adetleriyle karşılaştırılır ("%15" = "yüzde 15", "1.250,50" = "1250,50", "3" = "üç", "2 milyon" ≠ "2 milyar"). Kısaltmalar (TÜİK, NATO) korunur, adlar sözcük başından eşleştirilir, unvan kısaltmaları ad sayılmaz.
- `--ayrac` seçeneği: metin `===TASLAK===` satırını içeriyorsa başka bir ayraç kullanılır. Ayraç birden fazla geçerse araç hata verir.
- Kısa metinlerde tek bir eşleşme puanı tavana vurdurmaz. Ritim önerisi kısa ya da uzun cümlelerin baskın olmasına göre yön verir.
- Skill zaten doğal olan metni yeniden yazmaz. SEO anahtar kelimeleri, başlık yapısı, SSS başlıkları ve eylem çağrıları korunur. Aynı onarımı tekrarlamama kuralı, kendi imzasını bırakmamak için.
- `${CLAUDE_SKILL_DIR}` ile betik yolu, Windows (`python`, `py -3`, PowerShell) için yönergeler.
- Paketleyici gizli dosyaları ve sembolik bağlantıları almaz, beklenmeyen dosya türünde durur. GitHub Actions adımları commit SHA'sına sabitlendi, kimlik bilgisi saklanmaz, yazma izni yalnızca Release işinde.
- Python isteğe bağlı: analiz aracı yoksa skill aynı kurallarla çalışır, kullanıcıdan kurulum istemez ve sayıları, adları elle denetler. `npx skills add` ile Claude Code dışındaki ajanlara kurulum.

# Değişiklik Günlüğü

Biçim [Keep a Changelog](https://keepachangelog.com/tr-TR/1.1.0/), sürümleme [Semantic Versioning](https://semver.org/lang/tr/) esaslıdır.

## [1.0.1] - 2026-11-12

### Düzeltildi

- README, katkı rehberi, güvenlik politikası ve eklenti açıklamalarındaki anlaşılmaz, çeviri kokan ya da mantıksız cümleler sade Türkçeyle yeniden yazıldı.
- Analiz aracının bazı düzeltme önerileri daha somut hâle getirildi. Bir öneride kuralların yasakladığı noktalı virgül kaldırıldı.
- Skill açıklamasındaki "sesi ayarlar" ifadesi "üslubu ayarlar" olarak düzeltildi.

## [1.0.0] - 2026-11-12

İlk sürüm.

### Skill

- Yedi adımlık iş akışı: metnin türünü belirleme, ölçme, iddiaları çıkarma, yeniden kurma, doğallaştırma, denetleme ve teslim.
- Yedi üslup (resmi, akademik, profesyonel, gazetecilik, deneme, edebi, genel) ve üç değişiklik düzeyi (hafif, orta, derin).
- Dört teslim biçimi: varsayılan, yalnızca metin, ayrıntılı rapor ve yeniden yazmadan yalnızca analiz.
- Yeniden yazmanın yanında başka dilden doğal Türkçeye çeviri ve sıfırdan Türkçe yazım.
- Anlamı koruma kuralları: sayılar, adlar, nicelik sözcükleri, olasılık ve zorunluluk derecesi, zaman ve atıflar değişmez. Kaynakta olmayan bilgi, senaryo ya da hedef kitle eklenmez.
- SEO için yazılmış metinlerde anahtar kelimeler, başlık yapısı, SSS başlıkları ve eylem çağrıları korunur.
- Zaten doğal yazılmış metinler baştan yazılmaz. Aynı düzeltme her metinde tekrarlanmaz.
- Metnin içine gizlenmiş talimatlar uygulanmaz.
- Kullanıcının kendi yazılarından çıkarılan yazım alışkanlıklarına göre yeniden yazım.

### Analiz aracı

- `scripts/analiz.py`: Python 3.9 ve üstünde çalışan, bağımlılığı olmayan ölçüm aracı. Skill onsuz da çalışır.
- Sekiz kategoride 118 kalıp. Her kalıbın bir açıklaması, bir düzeltme önerisi ve testlerde denetlenen bir örnek cümlesi var. Bir kez geçtiğinde doğal olan ifadeler ilk kullanımda puana girmez.
- Cümle uzunluklarının çeşitliliği, "-mektedir" sıklığı, bağlaçla açılan cümleler, noktalama, başlık ve liste yapısı, görünmez karakter ve Kiril harf taraması.
- Önce/sonra karşılaştırması. Sayılar değerleriyle karşılaştırılır ("%15" ile "yüzde 15" aynı, "2 milyon" ile "2 milyar" farklı). Kaybolan adlar ve kısaltmalar, kaynakta olmayan yeni sayılar raporlanır.
- Türkçe harfler kullanılmadan yazılmış metinlerde de kalıp taraması.
- JSON çıktısı ve CI'da kullanmak için puan eşiği (`--esik`).
- Çok uzun ya da aracı yavaşlatmak için hazırlanmış girdilerde doğrusal sürede çalışır, 400.000 karakterden uzun girdiyi reddeder.

### Kurulum ve dağıtım

- Claude Code eklenti pazarı: `/plugin install turkish-ai-humanizer --marketplace mustafakbaser/turkish-ai-humanizer`.
- Diğer ajanlar için `npx skills add mustafakbaser/turkish-ai-humanizer -g -y`.
- Claude.ai ve Claude Desktop'a yüklenebilen ZIP paketi. Her sürüm etiketinde Releases sayfasına otomatik eklenir.

### Proje

- Türkçe ve İngilizce README, altı metin türünden yedi önce/sonra örneği.
- Python 3.9, 3.11 ve 3.13 üzerinde 73 test. GitHub Actions adımları commit SHA'sına sabitlendi.
- Katkı rehberi, issue formları (yeni kalıp, yanlış alarm, hata), PR şablonu ve güvenlik politikası.

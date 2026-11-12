# Tespit Mekanizmaları

Bu dosya yapay zekâ metin detektörlerinin genel olarak neye baktığını, bu skill'in tekniklerinin neden işe yaradığını ve hangi yöntemlerin işe yaramadığını anlatır. Kullanıcı "detektörlere takılmasın" dediğinde bu dosya beklentiyi dürüstçe kurmaya yarar.

## Detektörler neye bakar

**Öngörülebilirlik (perplexity).** Dil modeli her adımda olası sözcüğü seçer. Metindeki sözcükler bir modelin beklentisine ne kadar uyuyorsa metin o kadar "makine gibi" görünür. "Önemli bir rol oynamaktadır", "hızla değişen dünyada" gibi kalıplar en öngörülebilir dizilerdir.

**Dalgalanma (burstiness).** İnsan yazısında cümle uzunluğu, cümle yapısı ve öngörülebilirlik metin boyunca dalgalanır. Yapay zekâ metni düz bir çizgide ilerler.

**Sınıflandırıcılar.** Ticari detektörlerin çoğu, insan ve yapay zekâ metinleriyle eğitilmiş bir sınıflandırıcı modeli kullanır. Bu modeller elle tanımlanmış tek tek özelliklere değil, eğitim verisinden öğrendikleri örtük örüntülere bakar. Söylem yapısı, geçiş sıklığı, biçimlendirme ve işlev sözcüklerinin dağılımı gibi yüzey özellikleri bu örüntülere yansır.

**Stilometri.** İşlev sözcüklerinin ("ve", "bir", "bu", "için", "ile", "de/da", "ki") sıklık dağılımı yazara özgüdür. Bu projenin gözlemine göre yapay zekâ Türkçesinde "ve, bir, olarak, için, ile" fazla, "de/da, ki, bile, zaten" az görünüyor. Bu sistematik bir ölçüm değil, bir gözlemdir.

**Filigran (watermark).** Bazı sağlayıcılar üretim sırasında metne istatistiksel bir iz bırakan teknikler geliştirdi (örneğin Google'ın SynthID'si). Filigran belirli bir modelin çıktısına özgüdür. Bu skill filigranlarla ilgili hiçbir işlem yapmaz ve onları hedeflemez.

**İnsanlaştırıcı tespiti.** Bazı ticari detektörler, "insanlaştırıcı" araçlarla değiştirilmiş metinleri ayrıca tanımaya yönelik çalışmalar yürütüyor. Bu araçların çoğu eş anlamlı değiştirme ve rastgele bozma yaptığı için kendi örüntülerini bırakır.

## Bu skill'in teknikleri neyi hedefler

| Mekanizma | Skill'in karşılığı |
|---|---|
| Öngörülebilirlik | Kalıpları eş anlamlıyla değil, anlamdan yeniden kurarak temizlemek. Bağlama özgü, somut sözcük seçmek. |
| Dalgalanma | Cümle ve paragraf boylarını bilinçli olarak dalgalandırmak, CV'yi ölçmek. |
| Sınıflandırıcı | Şablon iskeleti, geçiş yığınını, simetrik dengeyi, kaçamakları ve biçimlendirme imzalarını kaldırmak. |
| Stilometri | Türkçe söylem belirteçlerini üsluba uygun sıklıkta geri koymak, "olarak / bir / için" yığınını azaltmak. Ses kartıyla yazarın kendi dağılımına yaklaşmak. |
| İnsanlaştırıcı tespiti | Hile kullanmamak. Rastgele bozma yerine iyi yazmak. |

Bu tablo skill'in neyi hedeflediğini gösterir, bir detektörden geçme garantisi değildir. Herhangi bir ticari detektöre karşı ölçülmüş bir başarı oranı iddia etmiyoruz. Kısacası skill detektörü kandırmaya çalışmaz. Metni, iyi bir Türk yazarın yazacağı metne yaklaştırır. Detektör sonucu bunun yan etkisidir.

## İşe yaramayan ve kullanılmayan yöntemler

- **Görünmez karakterler.** Sıfır genişlikli boşluk (U+200B), yumuşak tire (U+00AD) gibi karakterler sözcükleri bölerek detektörü şaşırtmaya çalışır. Kolayca temizlenir ve tespit edilir. Metni kopyalayan, arayan ya da ekran okuyucuyla okuyan herkes için bozar.
- **Homoglifler.** Latin "a" yerine Kiril "а" gibi görünüşte aynı harfler. Aynı nedenlerle hem tespit edilir hem metni bozar. Arama motorları ve yazım denetleyicileri bu sözcükleri tanımaz.
- **Kasıtlı yazım hatası.** Bazı detektörleri şaşırtabilir ama kolayca normalize edilir. Okurun güvenini ise kesin olarak kaybettirir.
- **Eş anlamlı döndürme.** Anlamı kaydırır, Türkçede ek uyumunu ve eşdizimi bozar ("hayati bir işlev icra etmektedir"), insanlaştırıcı imzası bırakır.
- **Rastgele cümle karıştırma.** Mantık akışını bozar.

`analiz.py` girdide görünmez karakter ve homoglif bulursa uyarır. Skill bunları her zaman temizler ve kullanıcıya bildirir.

## Gerçekçi beklenti

- **Hiçbir yöntem sıfır tespiti garanti etmez.** Detektörler olasılıksal çalışır, sürekli güncellenir ve birbirleriyle çelişir. Aynı metin farklı araçlarda çok farklı sonuçlar alabilir.
- **Detektörler insan metnini de işaretler.** Bir araştırma, detektörlerin anadili İngilizce olmayanların yazdığı İngilizce metinleri (TOEFL denemeleri) yüksek oranda yanlışlıkla yapay zekâ olarak işaretlediğini gösterdi (Liang ve ark., 2023, *Patterns*). Türkçe için benzer bir çalışma bilmiyoruz ama aynı risk akla yatkındır. Kısa, kalıplaşmış ve resmi metinler (özellikle hukuki ve akademik) daha sık yanlış alarm üretir.
- **Türkçe verisi sınırlı.** Ticari detektörlerin çoğu ağırlıklı olarak İngilizce verilerle geliştirildi. Türkçe performansları hakkında yayımlanmış bağımsız veri sınırlıdır.
- **Kısa metin güvenilmezdir.** 100 kelimenin altındaki metinlerde hem detektör hem `analiz.py` güvenilmezdir.
- **`analiz.py` bir detektör değildir.** Puanı ticari bir aracın skorunu tahmin etmez. Yalnızca bu skill'in bildiği imzaların yoğunluğunu ölçer.

## En güçlü katkı: insan girdisi

Bir metni gerçekten kişiye ait kılan şey, yalnızca o kişinin bilebileceği ayrıntıdır. Yazarın kendi deneyimi, bir müşteriyle yaşadığı bir an, kendi verisi, kendi görüşü. Hiçbir yeniden yazım bunun yerini tutmaz.

Bu yüzden skill teslimde en fazla üç hedefli soru sorar: "Bu paragrafa kendi projenden bir örnek ekleyebilir misin?", "Bu iddianın kaynağı ne?", "Buradaki görüşün ne?" Kullanıcı cevap verirse metne işlenir. Cevap vermezse metin olduğu gibi kalır.

## Etik çerçeve

Bu skill metni daha iyi yazmak için vardır: robotik bir taslağı okunur kılmak, bir çeviriyi doğallaştırmak, yazarın sesini korumak. Akademik ödevler, sınavlar, yarışmalar ya da yapay zekâ kullanımının beyan edilmesini isteyen yayınlar gibi bağlamlarda ilgili kurallara uymak kullanıcının sorumluluğundadır. Skill bu konuda vaaz vermez ama kullanıcı açıkça bir kuralı çiğnemek için yardım isterse (örneğin "hocam yapay zekâ kullandığımı anlamasın, ödev teslim edeceğim") bunu bir kez kısaca ve yargılamadan hatırlatır, ardından metni iyileştirmeye odaklanır.

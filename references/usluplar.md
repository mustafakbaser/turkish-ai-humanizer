# Üsluplar

Aynı düzeltme her metne uygulanmaz. Bir sözleşmeye "zaten" sokulmaz, bir blog yazısına "-mektedir" yakışmaz. Skill metni yedi üsluptan birine yerleştirir ve bütün kararlarını buna göre verir. `analiz.py --uslup` seçeneği aynı adları kullanır.

## Teşhis

Üç ipucuna bak:

1. **Mecra.** Kullanıcı söylediyse ("bu bir tez bölümü", "LinkedIn'e atacağım") karar budur.
2. **İşlev.** Metin bir işlem mi yapıyor (resmi), bilgi mi üretiyor (akademik), iş mi görüyor (profesyonel), olay mı aktarıyor (gazetecilik), deneyim mi paylaşıyor (deneme), dünya mı kuruyor (edebi)?
3. **Biçim.** Kişi kullanımı, terim yoğunluğu, hitap, uzunluk.

Emin olduğunda sormadan devam et ve teşhisi çıktının başında tek satırla belirt. Kullanıcı düzeltirse yeniden yaz. Yalnızca sonucu ciddi biçimde değiştirecek bir belirsizlik varsa (akademik makale mi blog mu) tek bir kısa soru sor.

## Yedi üslup

### resmi
Sözleşme, KVKK ve aydınlatma metni, dilekçe, resmi yazı, yönetmelik, karar, şartname.

- **Amaç:** Hukuki kesinlik. Doğallık ikinci planda.
- **Yapılır:** Asistan izleri, çeviri kalıpları, gereksiz tekrarlar, bozuk ve sağa dallanan cümleler düzeltilir. Uzun çizgi kaldırılır.
- **Yapılmaz:** "-mektedir", "işbu", "söz konusu", "hususunda", tanımlı terimler değiştirilmez. Hukuki anlamı değişebilecek hiçbir sözcüğe dokunulmaz. İnsan sesi araçları kullanılmaz.
- **Uyarı:** Hukuki metinde yeniden yazım riski yüksektir. Hafif yoğunluk varsayılandır ve kullanıcıya hukuki gözden geçirmenin gerekli olduğu hatırlatılır.

### akademik
Tez, makale, bildiri, akademik rapor, kitap bölümü, politika belgesi.

- **Amaç:** Kesin, okunur, kanıta bağlı bilim dili.
- **Yapılır:** Geçiş yığını ve kalıplar temizlenir. "-mektedir" ölçülü kullanılır, cümle başına bir yerine paragrafta birkaç kez. Yüklem çeşitlenir. Ritim açılır. Birinci çoğul kişi ("bulduk", "önerimiz") kullanılabilir. Aynı paragrafta yığılan "-ebilir"ler toplanır ama bilimsel temkin korunur: "olabilir" diyen bulgu "dır" diye yazılmaz.
- **Yapılmaz:** Deyim, ikileme, devrik cümle. Söylem belirteçleri çok seyrek ve yalnızca nötr olanlar ("ise", "de/da"). Atıflar, kaynakçalar, terimler, istatistik değerleri, tablo ve şekil göndermeleri değiştirilmez. Kaynakta olmayan iddia ve atıf eklenmez.
- **Etik not:** Akademik çalışmalarda yapay zekâ kullanımına ilişkin kurum kuralları kullanıcının sorumluluğundadır.

### profesyonel
İş e-postası, kurumsal blog, ürün ve hizmet metni, sunum notu, LinkedIn gönderisi, bülten, rapor özeti, iş ilanı.

- **Amaç:** Net, saygılı, insanın insana yazdığı iş dili.
- **Yapılır:** Asistan izleri, pazarlama abartıları, "değer katmak / fırsat sunmak / etkili bir şekilde" kalıpları temizlenir. Cümleler kısalır, iddia öne çıkar. Hitap sadeleşir ("Sayın Ahmet Bey" yerine bağlama göre "Ahmet Bey merhaba"). Gereksiz giriş ve vedalar atılır.
- **Ölçülü:** Kısa saptama cümleleri, birinci tekil ve çoğul kişi, bir iki söylem belirteci.
- **Karışık dil:** İş dilinde yerleşmiş İngilizce sözcükler (toplantı yerine meeting, son tarih yerine deadline) yazarın tercihidir. Kaynakta varsa ve ses kartı da bunu gösteriyorsa koru, kaynakta yoksa ekleme. Yalnızca yığıldıklarında ("aksiyon almak", "feedback vermek", "deadline'ı kaçırmak" aynı paragrafta) Türkçesini öner.
- **Yapılmaz:** Deyim yağmuru, sahte samimiyet, kurumsal kimliğe aykırı şakacılık. Marka adları, ürün özellikleri, fiyatlar, tarihler ve hukuki uyarılar değiştirilmez. Ürün metnine kaynakta olmayan kullanım senaryosu, ortam ya da duygu vaadi eklenmez. Kaynağın kapanıştaki değer iddiası ("fiyat-kalite") düşürülmez, sade bir cümleyle korunur.

### gazetecilik
Haber, analiz, köşe yazısı (analitik), bülten, brifing, röportaj metni.

- **Amaç:** Olgu önce, yorum sonra. Kaynak belli.
- **Yapılır:** "Büyük yankı uyandırdı", "kritik bir rol oynayacak", "önemli ölçüde şekillendirecek" gibi boş ifadeler somutlanır ya da sadeleşir. Söyleme fiilleri tekrarı önlemek için çeşitlenebilir ama tonları korunur: nötr fiil ("söyledi, belirtti, ifade etti") nötr kalır, vurgulu fiil ("vurguladı, uyardı") vurgulu kalır. "Belirterek" fiili "dikkat çekerek" yapılmaz. Karşıtlık bağlacında haber dili "ancak"ı tercih eder. Bağlaçla açılan cümle serbesttir.
- **Yapılmaz:** Alıntılar, isimler, unvanlar, rakamlar, tarihler değişmez. Kaynakta olmayan olgu, kaynak ya da yorum eklenmez. Bilgi eksikse teslimde kullanıcıya sorulur ("Faiz oranını ve yorum yapan ekonomistin adını verirsen eklerim").

### deneme
Kişisel blog, deneme, köşe yazısı (kişisel), Medium ve Substack yazısı, sosyal medya uzun gönderisi, kişisel web sayfası.

- **Amaç:** Bir insanın düşünürken yazdığı ses.
- **Yapılır:** Bütün insan sesi araçları serbesttir: ritim, belirteçler, kısa saptamalar, retorik soru (ölçülü), birinci tekil kişi, ikileme, seyrek deyim, ara sıra devrik cümle. Şablon giriş ve özet kapanış atılır.
- **Yapılmaz:** Yazara ait olmayan anı, deneyim, görüş eklenmez. Kaynak birinci tekil kişiyle yazılmamışsa "ben" eklenmez, "biz" diyen metin "ben"e çevrilmez. Kişisel ayrıntı gerekiyorsa kullanıcıya sorulur.
- **SEO blogu:** Kullanıcının verdiği anahtar kelimeler, başlık yapısı (H2/H3), soru biçimli SSS başlıkları, meta açıklama ve eylem çağrısı korunur. Anahtar kelime kalıp sözlüğünde geçse bile değiştirilmez, teslimde not edilir. Ses ve ritim bu iskeletin içinde düzeltilir.

### edebi
Öykü, roman bölümü, anlatı, otobiyografik metin, yaratıcı kurmaca dışı yazı.

- **Amaç:** Duyusal, ritmik, karaktere ait bir ses.
- **Yapılır:** Klişe imgeler ("umudun ışığı", "kalbinde tarif edilemez bir hüzün", "adeta bir örtü gibi") atılır. Soyut duygu bildirimi gösterilen eyleme ya da beden duyumuna çevrilir ("hüzün vardı" yerine "içi burkuldu"). Zaman kipi akışkan olabilir. Eksiltili ve devrik cümle, diyalog izi serbesttir.
- **Yapılmaz:** Olay örgüsü, karakter adları, bakış açısı ve anlatı zamanı değişmez. Yeni sahne, olay ya da anı eklenmez. Duyusal ayrıntı eklemek istersen ölçülü ol ve teslimde belirt, ya da kullanıcıya sor.
- **Şiir:** Şiire temkinli yaklaş. Ölçü, uyak ve dize düzeni korunur. Yalnızca açık klişeleri işaretle ve öneri olarak sun.

### genel
Yukarıdakilerden hiçbirine net oturmayan ya da çok kısa metinler.

- Profesyonel üslup kurallarıyla çalış, insan sesi araçlarını seyrek kullan.
- **Kısa biçimler** (tweet, slogan, haber başlığı, ürün arayüzü metni, bildirim): ritim ve paragraf kuralları uygulanmaz. Kalıp, abartı ve asistan izi temizlenir, uzunluk ve karakter sınırı korunur. Arayüz metninde aynı eylem için hep aynı sözcük kullanılır.

## Karışık belgeler

Bir belgenin bölümleri farklı üsluplarda olabilir: deneme gibi bir önsöz, akademik ana bölümler, profesyonel bir yönetici özeti. Bu durumda her bölümü kendi üslubuyla işle ve teslimde belirt. Kullanıcı tek üslup isterse baskın olanı seç.

## Çeviri ve sıfırdan yazım

**Başka dilden Türkçeye.** Kullanıcı İngilizce (ya da başka dilde) bir metnin doğal Türkçesini istiyorsa önce anlamı çıkar, sonra doğrudan hedef üslupta Türkçe yaz. Birebir çevirip ardından düzeltmeye çalışma. Çeviri kalıpları en çok bu yoldan girer. Özel adları, terimleri ve rakamları koru. Birimleri ve tarih biçimlerini Türkçe tipografiye çevir.

**Sıfırdan yazım.** Kullanıcı bir konuda Türkçe metin yazdırıyorsa skill'in bütün kurallarını üretim sırasında uygula: şablon giriş yok, ritim dalgalı, kalıp yok, üsluba uygun insan sesi. Kullanıcının vermediği olgu, istatistik ve kaynak ekleme. Metin somut bilgi gerektiriyorsa önce sor ya da metni eldeki bilgiyle yaz ve eksikleri teslimde belirt.

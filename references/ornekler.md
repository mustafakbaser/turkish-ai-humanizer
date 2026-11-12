# Örnekler

Her örnek, tipik bir yapay zekâ çıktısının önce ve sonra hâlidir. "Sonra" metinleri skill'in kurallarına göre elle hazırlanmış başvuru yeniden yazımlarıdır ve `tests/fixtures/` klasöründeki test metinleriyle birebir aynıdır. Ölçüm satırları `analiz.py --karsilastir` ile hesaplanır. Bu dosya `tools/ornekleri_uret.py` ile üretilir, elle düzenlenmez.

Örneklerde dikkat edilecek ilke: kaynaktaki her iddia, nicelik ("birçok", "bazı"), olasılık ifadesi ("-ebilir", "gibi görünüyor") ve zaman kipi korunur. Yeniden yazım üslubu değiştirir, iddiayı değiştirmez.

Örnekler aynı zamanda varsayılan teslim biçimini gösterir: kısa bir üslup satırı, metin, "Ne değişti" ve yalnızca gerçekten işe yarayacaksa "Sana kalan".

## İçindekiler

1. Uzaktan çalışma üzerine blog yazısı (deneme)
2. Kitap duyurusu, LinkedIn gönderisi (profesyonel)
3. Literatür değerlendirmesi paragrafı (akademik)
4. Bütçe onayı e-postası (profesyonel)
5. Faiz kararı haberi (gazetecilik)
6. Öyküden bir paragraf (edebi)
7. Kurum içi bilgi güvenliği duyurusu (resmi)
8. Aşırı düzeltme: nasıl yapılmaz

## 1. Uzaktan çalışma üzerine blog yazısı

### Önce

````markdown
Günümüzde uzaktan çalışma, hayatımızın ayrılmaz bir parçası haline gelmiştir. Teknolojinin hızla gelişmesiyle birlikte, birçok şirket çalışanlarına esnek çalışma imkânı sunmaktadır. Ancak, uzaktan çalışmanın sadece avantajları değil, aynı zamanda bazı zorlukları da bulunmaktadır.

Öncelikle, uzaktan çalışma iş-yaşam dengesini olumsuz etkileyebilmektedir. Ev ile ofis arasındaki sınırlar belirsizleştiğinde, çalışanlar kendilerini sürekli çevrimiçi olmak zorunda hissedebilirler. Bu durum, tükenmişlik sendromuna yol açabilmektedir.

Bunun yanı sıra, iletişim de önemli bir zorluk olarak öne çıkmaktadır. Yüz yüze etkileşimin eksikliği, ekip içi bağların zayıflamasına neden olabilmektedir. Bu bağlamda, şirketlerin dijital iletişim araçlarını etkili bir şekilde kullanması kritik bir rol oynamaktadır.

Sonuç olarak, uzaktan çalışma doğru stratejilerle yönetildiğinde hem çalışanlar hem de şirketler için büyük fırsatlar sunmaktadır. Önemli olan, bu dengeyi sağlıklı bir şekilde kurabilmektir.
````

### Sonra

**Üslup:** deneme · **Yoğunluk:** orta

````markdown
Uzaktan çalışma artık gündelik hayatın parçası. Teknoloji geliştikçe birçok şirket çalışanlarına esnek çalışma imkânı tanıyor. Ama bu düzenin avantajlarının yanında bazı zorlukları da var.

Önce iş ile özel hayat arasındaki denge zarar görebiliyor. Ev ile ofis arasındaki sınır bulanıklaştığında çalışanlar kendilerini sürekli çevrimiçi olmak zorunda hissedebiliyor, bu da tükenmişlik sendromuna yol açabilir.

İletişim de önemli bir zorluk. Yüz yüze görüşmenin eksikliği ekip içindeki bağları zayıflatabiliyor, bu yüzden şirketlerin dijital iletişim araçlarını etkili kullanması çok önemli.

Doğru stratejilerle yönetildiğinde uzaktan çalışma hem çalışanlar hem de şirketler için büyük fırsatlar barındırıyor, yeter ki bu denge sağlıklı kurulabilsin.
````

**Ne değişti**

- "Günümüzde ... ayrılmaz bir parçası haline gelmiştir" şablon girişi düz bir saptamaya indi: "artık gündelik hayatın parçası".
- "Sadece avantajları değil, aynı zamanda bazı zorlukları" kalıbı "avantajlarının yanında bazı zorlukları da var" oldu. "Bazı" korundu.
- Sekiz "-mekte/-makta" yüklemi "-iyor" ve geniş zamana çevrildi. Olasılık ifadeleri korundu: "etkileyebilmektedir" → "zarar görebiliyor", "yol açabilmektedir" → "yol açabilir", "neden olabilmektedir" → "zayıflatabiliyor".
- "Öncelikle / Bunun yanı sıra / Bu bağlamda / Sonuç olarak" iskeleti kaldırıldı. "Bu bağlamda" gerçek bir bağa ("bu yüzden") dönüştü.
- "Kritik bir rol oynamaktadır" → "çok önemli", "etkili bir şekilde" → "etkili". "Büyük fırsatlar sunmaktadır" fırsat olarak kaldı ("büyük fırsatlar barındırıyor"), kesin bir kazanca çevrilmedi.
- Cümle boyları açıldı (CV 0,26 → 0,48). Kısalma silinen kalıplardan geliyor. Yeni bilgi eklenmedi.

**Sana kalan**

- Kendi ekibinden ya da deneyiminden tek bir somut örnek verirsen ikinci paragrafa işlerim. Yazıyı en çok bu kişiselleştirir.

*Ölçüm: İmza puanı 73 → 8 · kalıp 14 → 0 · -mekte/-makta 8 → 0 · cümle CV 0,26 → 0,48 (hedef ≥ 0,55) · kelime 118 → 95 · kısa metin, puanlar yalnızca yön gösterir*

## 2. Kitap duyurusu, LinkedIn gönderisi

### Önce

````markdown
🚀 Heyecan verici bir haberi sizlerle paylaşmaktan mutluluk duyuyorum!

Uzun soluklu bir yolculuğun ardından, yeni kitabım "Veriyle Karar Vermek" nihayet raflarda! 📚 Bu kitap, sadece bir rehber değil, aynı zamanda veri odaklı düşünmenin kapılarını aralayan kapsamlı bir kaynak niteliğindedir.

Kitapta şu konulara derinlemesine değiniyorum:

✅ **Veri Okuryazarlığı:** Verileri doğru yorumlamanın temelleri
✅ **Karar Mekanizmaları:** Etkili kararlar almanın stratejileri
✅ **Gerçek Vaka Analizleri:** Sektörden ilham verici örnekler

Bu yolculukta bana destek olan herkese içtenlikle teşekkür ederim. 🙏 Kitabın, kariyer yolculuğunuzda size değerli içgörüler sunacağına inanıyorum!

#VeriBilimi #Liderlik #KitapÖnerisi
````

### Sonra

**Üslup:** profesyonel · **Yoğunluk:** derin (yapıya dokunuldu)

````markdown
Uzun süredir üzerinde çalıştığım kitap sonunda çıktı. "Veriyle Karar Vermek" artık raflarda. Bir rehber olarak yazdım ama veri odaklı düşünmeye kapsamlı bir giriş olarak da okunabilir.

Kitapta şu konulara ağırlık verdim:

- veriyi doğru yorumlamanın temelleri,
- etkili karar almanın yolları,
- sektörden gerçek vakalar.

Bu süreçte bana destek olan herkese içtenlikle teşekkür ederim. Kitabın kariyerinizde işinize yarayacak fikirler vereceğine inanıyorum.

#VeriBilimi #Liderlik #KitapÖnerisi
````

**Ne değişti**

- "Paylaşmaktan mutluluk duyuyorum" açılışı atıldı. Gönderi doğrudan haberle başlıyor.
- "Uzun soluklu bir yolculuğun ardından" yerine "uzun süredir üzerinde çalıştığım".
- "Sadece bir rehber değil, aynı zamanda ... kapılarını aralayan kapsamlı bir kaynak" iddiası iki parçasıyla korundu: "Bir rehber olarak yazdım ama veri odaklı düşünmeye kapsamlı bir giriş olarak da okunabilir."
- ✅ ve kalın etiketli maddeler sade maddelere dönüştü (derin yoğunlukta yapısal değişiklik). Madde içerikleri korundu, "ilham verici" sıfatı atıldı.
- "Kariyer yolculuğunuzda size değerli içgörüler sunacağına" → "kariyerinizde işinize yarayacak fikirler vereceğine". Okura söz verilen şey aynı.
- Altı emoji ve üç ünlem kaldırıldı, etiketler korundu. Kelime sayısındaki düşüş silinen kalıplardan ve emojilerden geliyor.

*Ölçüm: İmza puanı 45 → 3 · kalıp 7 → 0 · -mekte/-makta 0 → 0 · kelime 78 → 58 · kısa metin, puanlar yalnızca yön gösterir*

## 3. Literatür değerlendirmesi paragrafı

### Önce

````markdown
Sosyal medya kullanımının ergenlerin psikolojik iyi oluşu üzerindeki etkileri, son yıllarda akademik literatürde giderek artan bir ilgi görmektedir. Bu bağlamda, yapılan çalışmalar sosyal medya kullanımının hem olumlu hem de olumsuz sonuçlar doğurabileceğini ortaya koymaktadır. Söz konusu çalışmalar incelendiğinde, aşırı kullanımın kaygı ve depresyon belirtileriyle ilişkili olduğu görülmektedir. Öte yandan, sosyal medyanın sosyal destek sağlama potansiyeline sahip olduğu da göz ardı edilmemelidir. Dolayısıyla, bu alanda daha kapsamlı ve boylamsal çalışmalara ihtiyaç duyulmaktadır.
````

### Sonra

**Üslup:** akademik · **Yoğunluk:** orta

````markdown
Sosyal medya kullanımının ergenlerin psikolojik iyi oluşu üzerindeki etkileri, son yıllarda akademik literatürde giderek daha çok ilgi görmektedir. Çalışmalar, sosyal medya kullanımının hem olumlu hem olumsuz sonuçlar doğurabileceğini göstermiştir. Aşırı kullanım bu çalışmalarda kaygı ve depresyon belirtileriyle ilişkili bulunmuştur. Buna karşılık sosyal medyanın bir sosyal destek kaynağı olabileceği de dikkate alınmalıdır. Bu nedenle bu alanda daha kapsamlı ve boylamsal çalışmalara ihtiyaç vardır.
````

**Ne değişti**

- "Bu bağlamda / Söz konusu / Öte yandan / Dolayısıyla" zinciri kaldırıldı. Tek bağ olarak "Bu nedenle" kaldı.
- Dört "-mektedir" yükleminden biri kaldı, diğerleri "-mıştır" ve ad cümlesine döndü. Akademik üslupta ölçülü kullanım doğaldır.
- "Giderek artan bir ilgi görmektedir" → "giderek daha çok ilgi görmektedir". Literatür özne olmaktan çıktı, ilgi gören konu oldu.
- "Potansiyeline sahip olduğu da göz ardı edilmemelidir" → "kaynağı olabileceği de dikkate alınmalıdır". Olasılık ve uyarı tonu korundu.
- Terimler (psikolojik iyi oluş, boylamsal) ve iddiaların kapsamı korundu. Atıf ya da bulgu eklenmedi.

*Ölçüm: İmza puanı 68 → 11 · kalıp 6 → 0 · -mekte/-makta 4 → 1 · cümle CV 0,19 → 0,23 (hedef ≥ 0,40) · kelime 71 → 62 · kısa metin, puanlar yalnızca yön gösterir*

## 4. Bütçe onayı e-postası

### Önce

````markdown
Sayın Ahmet Bey,

Umarım bu e-posta sizi iyi bulur. 15 Kasım tarihinde gerçekleştirdiğimiz toplantıda ele alınan konulara ilişkin olarak sizinle iletişime geçmek istedim. Toplantıda belirtildiği üzere, projenin ikinci aşamasının başarılı bir şekilde tamamlanabilmesi için bütçe onayının en kısa sürede sağlanması büyük önem arz etmektedir.

Bu doğrultuda, ekte yer alan bütçe tablosunu incelemenizi ve onayınızı 20 Kasım tarihine kadar iletmenizi rica ederim. Herhangi bir sorunuz olması durumunda benimle iletişime geçmekten çekinmeyiniz.

Saygılarımla,
Elif Kaya
````

### Sonra

**Üslup:** profesyonel · **Yoğunluk:** orta

````markdown
Ahmet Bey merhaba,

15 Kasım'daki toplantıda konuştuğumuz konularla ilgili yazıyorum. Toplantıda da belirtildiği gibi, projenin ikinci aşamasını başarıyla tamamlayabilmemiz için bütçe onayının bir an önce çıkması çok önemli.

Bütçe tablosu ekte. İnceleyip onayınızı 20 Kasım'a kadar iletmenizi rica ederim. Sorunuz olursa yazabilirsiniz.

Saygılarımla,
Elif Kaya
````

**Ne değişti**

- "Umarım bu e-posta sizi iyi bulur" ve "iletişime geçmekten çekinmeyiniz" çeviri kalıpları atıldı. Kapanışta tek ve sade bir cümle kaldı.
- "Sayın Ahmet Bey" yerine iş yazışmasında yaygın olan "Ahmet Bey merhaba". Kurum kültürü daha resmiyse eski hitap korunur.
- "Toplantıda belirtildiği üzere" → "Toplantıda da belirtildiği gibi". Atıf edilgen kaldı, "biz"e çevrilmedi.
- "Başarılı bir şekilde tamamlanabilmesi için ... en kısa sürede sağlanması büyük önem arz etmektedir" → "başarıyla tamamlayabilmemiz için bütçe onayının bir an önce çıkması çok önemli". Önem derecesi ve aciliyet aynı.
- Tarihler (15 Kasım, 20 Kasım) ve talep aynı. Kelime sayısındaki düşüş silinen kalıplardan geliyor, içerik kaybı yok.

*Ölçüm: İmza puanı 43 → 0 · kalıp 7 → 0 · -mekte/-makta 1 → 0 · cümle CV 0,61 → 0,8 (hedef ≥ 0,45) · kelime 74 → 45 · kısa metin, puanlar yalnızca yön gösterir*

## 5. Faiz kararı haberi

### Önce

````markdown
Merkez Bankası'nın faiz kararı, piyasalarda büyük bir yankı uyandırdı. Ekonomistler, kararın enflasyonla mücadelede kritik bir rol oynayacağını ifade ederken, bazı uzmanlar ise kararın büyüme üzerinde olumsuz etkiler yaratabileceği konusunda uyarılarda bulundu. Bu gelişme, yatırımcıların gelecekteki adımlara ilişkin beklentilerini de önemli ölçüde şekillendirecek gibi görünmektedir.
````

### Sonra

**Üslup:** gazetecilik · **Yoğunluk:** orta

````markdown
Merkez Bankasının faiz kararı piyasalarda büyük yankı uyandırdı. Ekonomistler kararın enflasyonla mücadelede belirleyici olacağını söyledi. Bazı uzmanlar ise kararın büyümeyi olumsuz etkileyebileceği konusunda uyardı. Karar, yatırımcıların bundan sonraki adımlara dair beklentilerini de büyük ölçüde belirleyecek gibi görünüyor.
````

**Ne değişti**

- "Büyük bir yankı uyandırdı" neredeyse aynen kaldı (yalnızca virgül ve "bir" atıldı). Kalıp olmayan bir ifadeyi eş anlamlısıyla değiştirmeye gerek yok.
- "Kritik bir rol oynayacağını ifade ederken" → "belirleyici olacağını söyledi". Nötr söyleme fiili nötr kaldı, atıf (ekonomistlerin tümü) korundu.
- "Konusunda uyarılarda bulundu" → "konusunda uyardı". Uzun cümle ikiye bölündü, geçmiş zaman korundu.
- "Önemli ölçüde şekillendirecek gibi görünmektedir" → "büyük ölçüde belirleyecek gibi görünüyor". Etkinin derecesi ve belirsizlik korundu.
- "Merkez Bankası'nın" TDK kuralına göre "Merkez Bankasının" yazıldı: kurum adlarına gelen ekler kesmeyle ayrılmaz. Yayın kuralın farklıysa kaynaktaki gibi bırakılır.

**Sana kalan**

- Faiz oranı, karar tarihi ve yorum yapan ekonomistlerin adları metni hem güçlendirir hem de şablon hissini kırar. Bunları verirsen eklerim.

*Ölçüm: İmza puanı 44 → 0 · kalıp 1 → 0 · -mekte/-makta 1 → 0 · kelime 44 → 37 · kısa metin, puanlar yalnızca yön gösterir*

## 6. Öyküden bir paragraf

### Önce

````markdown
Yağmur, şehrin sokaklarını adeta bir örtü gibi kaplıyordu. Elif, pencerenin önünde durmuş, geçmişin hatıralarıyla dolu zihninde kaybolmuştu. Her damla, ona annesiyle geçirdiği o eşsiz anları hatırlatıyordu. Kalbinde tarif edilemez bir hüzün vardı; ama aynı zamanda, umudun ışığı da hâlâ parlıyordu.
````

### Sonra

**Üslup:** edebi · **Yoğunluk:** orta

````markdown
Yağmur şehrin sokaklarını kaplıyordu. Elif pencerenin önünde durmuş, geçmişin anıları arasında kaybolup gitmişti. Her damla ona annesiyle geçirdiği o anları hatırlatıyordu. İçi burkuluyordu. Yine de bir yanı hâlâ umutluydu.
````

**Ne değişti**

- "Adeta bir örtü gibi" klişe benzetmesi ve "o eşsiz anlar"daki abartı çıkarıldı. "O anlar"daki gösterme sözcüğü duyguyu taşıyor.
- "Geçmişin hatıralarıyla dolu zihninde kaybolmuştu" → "geçmişin anıları arasında kaybolup gitmişti".
- "Kalbinde tarif edilemez bir hüzün vardı" duygu bildirimi beden duyumuna çevrildi: "İçi burkuluyordu." Anlatı zamanı korundu.
- Noktalı virgül ve "ama aynı zamanda" yerine iki cümle. "Umudun ışığı" klişesi sade bir cümleye indi, "hâlâ" korundu.
- Karakter, mekân, zaman ve olay aynı kaldı. Kısalma silinen klişelerden geliyor. Yeni sahne, ayrıntı ya da anı eklenmedi.

**Sana kalan**

- Yağmurun sesi, odadaki bir koku ya da annesine dair tek bir somut nesne sahneyi çok daha canlı kılar. Bunu senin kurgundan alalım.

*Ölçüm: İmza puanı 37 → 6 · kalıp 2 → 0 · -mekte/-makta 0 → 0 · kelime 40 → 29 · kısa metin, puanlar yalnızca yön gösterir*

## 7. Kurum içi bilgi güvenliği duyurusu

### Önce

````markdown
Değerli Çalışanlarımız,

Şirketimizin bilgi güvenliği politikası çerçevesinde, tüm çalışanlarımızın şifrelerini 90 günde bir değiştirmesi büyük önem arz etmektedir. Bu bağlamda, 1 Aralık 2026 tarihinden itibaren sistem, şifresi 90 günden eski olan kullanıcıları otomatik olarak uyaracaktır. Bunun yanı sıra, şifrelerin en az 12 karakterden oluşması ve harf, rakam ve özel karakter içermesi gerekmektedir. Söz konusu kurallara uyulmaması halinde, hesaplar geçici olarak askıya alınabilecektir.

Bu süreçte göstereceğiniz anlayış ve işbirliği için şimdiden teşekkür ederiz. Herhangi bir sorunuz olması durumunda Bilgi İşlem birimiyle iletişime geçmekten çekinmeyiniz.
````

### Sonra

**Üslup:** resmi · **Yoğunluk:** hafif

````markdown
Değerli Çalışanlarımız,

Şirketimizin bilgi güvenliği politikası gereği tüm çalışanlarımızın şifrelerini 90 günde bir değiştirmesi çok önemlidir. 1 Aralık 2026 tarihinden itibaren sistem, şifresi 90 günden eski olan kullanıcıları otomatik olarak uyaracaktır. Şifrelerin ayrıca en az 12 karakterden oluşması ve harf, rakam ve özel karakter içermesi gerekmektedir. Bu kurallara uyulmaması hâlinde hesaplar geçici olarak askıya alınabilecektir.

Anlayışınız ve iş birliğiniz için şimdiden teşekkür ederiz. Sorularınızı Bilgi İşlem birimine iletebilirsiniz.
````

**Ne değişti**

- "Büyük önem arz etmektedir" → "çok önemlidir". Önem derecesi korundu, zorunluluğa çevrilmedi.
- "Bu bağlamda" ve "Bunun yanı sıra" kaldırıldı, "Söz konusu kurallara" → "Bu kurallara".
- "Gerekmektedir" ve resmi hitap üslubun gereği olarak korundu. Sayılar, tarih ve birim adı aynı.
- "İletişime geçmekten çekinmeyiniz" → "Sorularınızı Bilgi İşlem birimine iletebilirsiniz." TDK'ya göre "halinde" → "hâlinde", "işbirliği" → "iş birliği".
- Hafif yoğunlukta cümle yapısı büyük ölçüde korundu. Metnin hukuk ya da İK onayından geçmesi gerekiyorsa bu adım atlanmamalı.

*Ölçüm: İmza puanı 42 → 4 · kalıp 6 → 1 · -mekte/-makta 2 → 1 · cümle CV 0,42 → 0,49 (hedef ≥ 0,35) · kelime 83 → 68 · kısa metin, puanlar yalnızca yön gösterir*

## 8. Aşırı düzeltme: nasıl yapılmaz

Aynı haber metninin kötü bir "insanlaştırılmış" hâli:

````markdown
Merkez Bankasının faiz kararı piyasada adeta deprem etkisi yarattı, yani ortalık bir anda karıştı işte. Zaten ekonomistlerin bir kısmı bu işin suyunun çıktığını, enflasyonun artık köşeye sıkıştığını düşünüyor. Bazı uzmanlarsa hani şu meşhur büyüme var ya, onun bundan pek hoşlanmayacağını söylüyor! Yatırımcılar mı? Onlar da diken üstünde, ne olacak diye bekleşip duruyorlar.
````

**Neden yanlış**

- Gazetecilik üslubuna konuşma dili ve belirteç yağmuru (yani, işte, zaten, hani) sokulmuş.
- Üç deyim üst üste (suyunun çıkması, köşeye sıkışmak, diken üstünde). İnsanlaştırıcı imzası.
- Kaynakta olmayan iddialar eklenmiş: "deprem etkisi", "enflasyon köşeye sıkıştı", yatırımcıların "diken üstünde" olduğu.
- Nicelik değişmiş: kaynakta "ekonomistler" var, burada "ekonomistlerin bir kısmı".
- "Yatırımcılar mı? Onlar da..." soru-cevap kalıbı ve ünlem haberin ciddiyetini bozuyor.
- "Adeta" kalmış. Kalıp temizlenmeden üstüne süs eklenmiş.

Doğru hâli 5. örnektedir. İnsan sesi araçları üsluba göre dozlanır. Gazetecilikte olgu önce gelir, süs hiç gelmez.

# İnsan Sesi

Yapay zekâ izini silmek işin yarısıdır. Geriye kalan metin temiz ama cansız olabilir. Bu dosya, insan Türkçesinin ölçülebilir özelliklerini metne üsluba uygun dozda geri koymanın yollarını anlatır.

## İçindekiler

1. Ritim
2. Yüklem çeşitliliği
3. Söylem belirteçleri
4. Somutluk
5. Tavır
6. Asimetri
7. Türkçeye özgü araçlar (ikileme, deyim, zarf-fiil, devrik cümle)
8. Doz tablosu
9. Aşırı düzeltme: yeni imza üretme
10. Ses kartıyla çalışma

## 1. Ritim

Yapay zekâ cümleleri birbirine benzer uzunluktadır. Bu projenin örneklerinde Türkçe yapay zekâ cümleleri çoğunlukla 9-14 kelime arasında toplanıyor ve sapma az (bu bir gözlemdir, genel bir ölçüm değil). İnsan yazısında üç kelimelik bir cümlenin ardından otuz kelimelik bir cümle gelebilir. Bu dalgalanmaya "burstiness" denir ve detektörlerin baktığı özelliklerden biri olarak sık anılır.

Ölçüt, cümle uzunluğu varyasyon katsayısıdır (CV = standart sapma / ortalama). `analiz.py` bunu raporlar. Kabaca 0,30'un altı belirgin biçimde tekdüzedir. Hedef üsluba göre değişir: resmi 0,35, akademik 0,40, profesyonel ve gazetecilik 0,45, genel 0,50, deneme ve edebi 0,55. Bu değerler sezgiseldir ve kısa metinlerde güvenilmezdir.

Ritmi açmanın yolları:

- **Kısa ve kesin bir cümle.** Bir iddiadan sonra, onu sabitleyen dört beş kelime: "Kazançları herkes biliyor. Bedeli ise daha geç fark ediliyor."
- **Uzun ve akışkan bir cümle.** Zarf-fiillerle (-ip, -erek, -ince, -ken, -dıkça) birbirine bağlanan, nefesi uzun bir cümle. "Ve" zinciriyle değil.
- **Birleştir.** Aynı şeyi söyleyen iki orta cümleyi tek cümlede topla.
- **Böl.** Virgülle uzatılmış üç yan cümleyi iki ayrı cümleye ayır.
- **Paragraf boyunu oynat.** Tek cümlelik bir paragraf, ardından yedi cümlelik bir paragraf. Bütün paragraflar dört cümle olmasın.

Ritim kuralı mekanik değildir. Kısa cümle ancak bir şeyi vurgulamak için gelir. Rastgele kısaltılmış cümle yine yapay durur.

## 2. Yüklem çeşitliliği

Türkçe zaman ve kip açısından zengindir. Yapay zekâ ise tek bir kipe yapışır (çoğunlukla -mektedir ya da geniş zaman + -dır).

| Kip | Ne zaman | Örnek |
|---|---|---|
| -di (görülen geçmiş) | olgular, anlatı | "Ekip planı mart ayında değiştirdi." |
| -miş (duyulan geçmiş) | aktarılan bilgi, şaşkınlık | "Toplantı iptal olmuş." |
| -iyor | süren durum, canlı anlatım | "Fiyatlar her ay biraz daha artıyor." |
| -ir (geniş zaman) | genel doğrular, alışkanlık | "Böyle projeler genelde uzar." |
| -ecek | öngörü, plan | "Karar haftaya çıkacak." |
| ad cümlesi | kısa saptama | "Sonuç belli." |
| -dir | genelleme, kesinlik (seyrek) | "Bu tür hatalar yaygındır." |

Anlatıda zaman geçişleri de doğaldır. Bir öykü geçmiş zamanda akarken bir an şimdiki zamana geçip okuru sahneye sokabilir.

## 3. Söylem belirteçleri

Türkçe konuşmanın ve canlı yazının küçük sözcükleri. Yapay zekâ metinlerinde neredeyse hiç bulunmazlar. Doğru yerde ve az kullanıldıklarında metne en çok insan sesi katan araç bunlardır.

| Belirteç | İşlev | Örnek |
|---|---|---|
| de/da | ekleme, vurgu, karşıtlık | "Ekip arkadaşlarınızla aranızdaki bağ da zayıflıyor." |
| bile | beklenmedik uç | "Müdür bile itiraz etmedi." |
| zaten | önceden bilinen | "Zaten herkes biliyordu." |
| artık | durum değişimi | "Artık kimse sormuyor." |
| hani | ortak bilgiye gönderme | "Hani geçen yıl konuştuğumuz plan..." |
| işte | gösterme, sonuç | "İşte o zaman anladım." |
| ki | açıklama, şaşkınlık | "Öyle bir kalabalık vardı ki..." |
| oysa, hâlbuki | beklentiye karşıtlık | "Oysa plan çok basitti." |
| üstelik, hatta | yükseltme | "Hatta bir kısmı geri döndü." |
| meğer | sonradan fark edilen | "Meğer herkes aynı şeyi düşünüyormuş." |
| galiba, herhalde, belki | ölçülü tahmin | "Galiba erken davrandık." |
| ise | karşılaştırma | "Kazancı herkes biliyor, bedeli ise geç fark ediliyor." |

"Ama, oysa, üstelik" ile açılan cümle Türkçede doğaldır, özellikle deneme ve blogda. Resmi ve akademik metinde bağlacı cümlenin içinde tutmak daha uygundur.

## 4. Somutluk

Detektörler ve okurlar için en güçlü insan işareti, yalnızca o metne ait olan ayrıntıdır: bir isim, bir tarih, bir yer, bir sayı, bir anı, bir alıntı.

**Ama ayrıntıyı uydurma.** Bu skill'in kırmızı çizgisidir. Kaynakta olmayan bir olguyu, istatistiği, kaynağı ya da kişisel anıyı ekleme. Üç seçeneğin var:

1. **Kaynaktaki ayrıntıyı öne çıkar.** Metin bir sayı içeriyorsa onu cümlenin merkezine taşı.
2. **Genel ve varsayımsal örnek ver (yalnızca deneme ve edebi).** Herkesin tanıyacağı türden, olgu iddiası taşımayan tek bir örnek: "Akşam gelen bir mesajı cevapsız bırakmak ayıp gibi geliyor." Metin başına en fazla bir tane, her zaman "Ne değişti" bölümünde belirtilerek. Genelleme ("çoğu zaman", "herkes biliyor") eklemek örnek vermek değildir, yeni iddiadır.
3. **Kullanıcıya sor.** Teslimde 1-3 hedefli soru: "Bu paragrafa kendi deneyiminden bir örnek ekleyebilir misin?" Kullanıcının vereceği tek bir gerçek ayrıntı, metni yüz kelimelik düzeltmeden daha çok insanlaştırır.

## 5. Tavır

Yapay zekâ her konuda dengelidir: "bir yandan ... öte yandan", "hem avantajları hem dezavantajları var", "doğru stratejiyle yönetildiğinde". İnsan yazar bir görüş taşır ve onu söyler.

- Kaynak bir görüş taşıyorsa onu net söyle. Kesin konuşan kaynağa "-ebilir" ve "genellikle" ekleme, temkinli kaynağın temkinini de silme.
- Kaynak gerçekten iki taraflıysa iki tarafı da söyle ama simetrik bir şablonla değil. Bir tarafa daha çok yer vermek doğaldır.
- Görüş eklemek kaynakta olmayan bir iddia eklemek demektir. Kaynakta tavır yoksa sen ekleme. "Sana kalan" bölümünde "Burada net bir görüş metni güçlendirir" diye öner.

## 6. Asimetri

Yapay zekâ simetriyi sever: üç başlık, her başlıkta üç madde, her paragrafta dört cümle, her bölümün sonunda bir özet. İnsan yazısı düzensizdir.

- Liste öğe sayısını içerik belirlesin. Gerçekte iki şey varsa iki say.
- Bütün bölümler aynı uzunlukta olmasın.
- Her paragraf bir "toparlama" cümlesiyle bitmesin. Bazı paragraflar bir olguyla, bazıları bir soruyla bitebilir.
- Kalın etiket + iki nokta maddeleri ("**Verimlilik:** ...") ve emojili madde işaretleri yapay zekâ biçimlendirmesinin en tanınan görüntüsüdür. Yapıya dokunma iznin varsa bunları sade maddelere ya da düz yazıya çevir.

## 7. Türkçeye özgü araçlar

**İkilemeler.** "Yavaş yavaş, er geç, az çok, ufak tefek, eski püskü, ister istemez, aşağı yukarı, eğri büğrü." Metne yerli bir doku katarlar. Deneme, blog ve edebi metinde 300 kelimede bir ya da iki tane yeter. "Kitap mitap" gibi m'li ikilemeler yalnızca çok samimi metinlere uyar.

**Deyimler.** "Kulak asmamak, göz yummak, işin içinden çıkmak, ipin ucunu kaçırmak, bardağı taşıran son damla." Bağlama tam oturan bir deyim tek başına bir paragrafı canlandırır. Ama deyim sıklığı yapay zekâ "insanlaştırıcılarının" bilinen bir imzasıdır. Kural: deneme ve blogda 300 kelimede en fazla bir deyim. Edebi metinde karakterin ve anlatıcının sesine göre daha sık olabilir, ama aynı paragrafta iki deyim yan yana gelmesin. Resmi ve akademik metinde hiç kullanma.

**Zarf-fiiller.** "-ip, -erek, -ince, -ken, -dıkça, -madan, -alı, -cesine." Türkçe uzun cümleyi "ve" ile değil bunlarla kurar. "Eve geldi ve yemek yedi ve uyudu" yerine "Eve gelip yemeğini yedi, uyudu." "-dığı zaman" yerine çoğu zaman "-ince" ya da "-ken", art arda eylemlerde "-dıktan sonra" yerine "-ip" yeter.

**Devrik cümle.** Yüklemi öne almak. Deneme ve edebi metinde ara sıra: "Bilmiyordu kimse ne olacağını." Akademik ve resmi metinde kullanma.

**Zamir düşürme ve hitap.** Türkçe zamiri düşürür: "Ben düşündüm" değil "düşündüm". Hitapta tutarlı ol: metin "siz" ile başladıysa "sen"e geçme.

**Parantez.** Uzun çizginin yerine ara söz için parantez kullanmak doğaldır ve insan yazısında sık görülür: "Toplantı (iki kez ertelenmişti) sonunda cuma günü yapıldı."

## 8. Doz tablosu

Hangi aracın hangi üslupta ne kadar kullanılacağı. "Yok" kullanma demektir. "Çok seyrek" uzun bir metinde bir kez, "seyrek" metin başına bir iki kez demektir. "Serbest" aracın bu üslupta doğal olduğunu söyler, ama yine de bir tavandır: paragraf başına bir kullanımı geçme ve aynı aracı art arda iki cümlede kullanma. Hiçbir araç her metinde bulunmak zorunda değildir.

| Araç | Resmi | Akademik | Profesyonel | Gazetecilik | Deneme-blog | Edebi |
|---|---|---|---|---|---|---|
| Ritim varyasyonu (CV hedefi) | 0,35+ | 0,40+ | 0,45+ | 0,45+ | 0,55+ | 0,55+ |
| -mekte/-makta | serbest | ölçülü | yok | yok | yok | yok |
| Söylem belirteçleri | yok | çok seyrek | seyrek | seyrek | serbest | serbest |
| Bağlaçla açılan cümle | yok | seyrek | seyrek | serbest | serbest | serbest |
| Kısa saptama cümlesi | yok | seyrek | serbest | serbest | serbest | serbest |
| Eksiltili cümle | yok | yok | seyrek | seyrek | serbest | serbest |
| Retorik soru | yok | çok seyrek | seyrek | seyrek | seyrek | seyrek |
| 1. tekil kişi | yok | yok | kaynakta varsa | yok | kaynakta varsa | karaktere bağlı |
| 1. çoğul kişi (biz) | kurumsal | serbest | serbest | seyrek | serbest | karaktere bağlı |
| İkileme | yok | yok | çok seyrek | seyrek | serbest | serbest |
| Deyim | yok | yok | çok seyrek | seyrek | seyrek | serbest |
| Devrik cümle | yok | yok | yok | çok seyrek | seyrek | serbest |
| Parantez içi ara söz | serbest | serbest | serbest | serbest | serbest | serbest |
| Diyalog çizgisi (—) | yok | yok | yok | yok | yok | kaynakta varsa |

## 9. Aşırı düzeltme

İnsanlaştırma yaparken yeni bir imza üretmek kolaydır. Bazı detektörler artık özellikle "insanlaştırıcı" araçların çıktısını tanımak için eğitiliyor. Şunlardan kaçın:

- **Belirteç yağmuru.** Her cümlede "zaten", "işte", "yani". Belirteçler serpiştirilir, dökülmez.
- **Deyim vitrini.** Her paragrafa bir deyim. Doğal yazar deyimi bulduğu zaman kullanır, aramaz.
- **Kısa cümle saplantısı.** Bütün cümleleri kısaltmak da tekdüzeliktir, sadece tersinden.
- **Soru yağmuru.** Her paragraf bir soruyla açılıp bir soruyla kapanmasın.
- **Sahte samimiyet.** Kurumsal bir metne "Açıkçası", "Dürüst olmak gerekirse", "Bakın" serpiştirmek.
- **Kasıtlı hata.** Yazım hatası, eksik harf, bozuk dilbilgisi eklemek. Bazı detektörleri şaşırtabilir ama kolayca normalize edilir. Metnin kalitesini düşürür ve profesyonel okurun güvenini kesin olarak kaybettirir. Asla yapma.
- **Görünmez karakter ve harf hilesi.** Sıfır genişlikli boşluk, Kiril "а" ile Latin "a" değişimi. Bunlar tespit edilir ve metni bozar. Asla yapma. Girdide varsa temizle ve bildir.
- **Rastgele eş anlamlı.** Sözcükleri eş anlamlılarıyla değiştirmek ("paraphrase spinning"). Anlam kayar, metin tuhaflaşır, detektörler bunu da tanır.

Test: Çıktıyı sesli okuduğunda bir Türk yazar böyle yazar mıydı? Bir editör "bu cümle zorlama" der miydi?

## 10. Ses kartıyla çalışma

Kullanıcı kendi yazdığı metinlerden örnek verirse (toplam 300 kelime ve üstü ideal), en iyi sonuç onun sesine yaklaşmaktır.

1. Örnekleri `analiz.py --profil` ile ölç ya da betik yoksa aynı ölçütleri gözle çıkar: cümle ortalaması ve dalgalanması, paragraf boyu, sık açılışlar, söylem belirteçleri, kişi kullanımı, noktalama alışkanlıkları.
2. Ölçülemeyeni de not et: yazar kavram mı üretiyor, mizah kullanıyor mu, uzun alıntıları seviyor mu, hangi sözcükleri hiç kullanmıyor.
3. Yeniden yazarken cümle ortalamasını kartın ±3 kelimesi, CV'yi ±0,1 içinde tut. Yazarın belirteçlerini onun sıklığında kullan. Yazarın hiç kullanmadığı bir şeyi (noktalı virgül, devrik cümle, belirli bir bağlaç) ekleme.
4. Kart sohbet boyunca geçerlidir. Kullanıcı isterse kartı bir dosyaya (örneğin kendi projesinde `ses-karti.md`) kaydedebilirsin. Skill klasörüne yazma.

Ses kartı yazarın imzasını yapay zekâ imzasından ayırmaya da yarar. Yazar "söz konusu" ifadesini sık kullanıyorsa o ifade onundur ve silinmez.

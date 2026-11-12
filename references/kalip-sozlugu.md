# Kalıp Sözlüğü

Türkçe yapay zekâ metninin sözcük ve söyleyiş düzeyindeki imzaları. Makine tarafından taranabilen kalıpların tam listesi `scripts/kaliplar.json` dosyasındadır (`python3 scripts/analiz.py --kaliplar`). Bu dosya o listeyi açıklar, onarım yollarını gösterir ve regex ile yakalanamayan dilbilgisel imzaları ekler.

## İçindekiler

1. Temel ilke: kalıbı değiştirme, cümleyi yeniden kur
2. Asistan izleri
3. Şablon giriş ve kapanışlar
4. Çeviri söyleyişler (calque)
5. Boş sıfatlar ve dolgu sözleri
6. Bürokratik geçişler
7. Retorik kalıplar
8. Ek ve destek fiil yükü
9. Regex'in göremediği dilbilgisel imzalar
10. Bağlamın kalıbı akladığı durumlar

## 1. Temel ilke

Kalıbı eş anlamlısıyla değiştirmek işe yaramaz. "Kritik bir rol oynamaktadır" yerine "hayati bir işlev üstlenmektedir" yazmak aynı cümleyi farklı kılıkla tekrarlamaktır. Dikkatli bir okur bunu hemen fark eder. Doğru hamle, cümlenin ne demek istediğini bulup onu Türkçenin kendi kuruluşuyla yeniden söylemektir.

| Yapay zekâ | Eş anlamlı değişimi (yanlış) | Yeniden kuruluş (doğru) |
|---|---|---|
| Eğitim bu süreçte kritik bir rol oynamaktadır. | Eğitim bu süreçte hayati bir işlev görmektedir. | Bu süreci asıl eğitim belirliyor. |
| Bu yöntem önemli avantajlar sağlar. | Bu yöntem kayda değer faydalar sunar. | Bu yöntemin epey faydası var. |
| Veri güvenliği büyük bir öneme sahiptir. | Veri güvenliği son derece önemlidir. | Veri güvenliği önemli. |

Üçüncü sütun hiçbir şey eklemiyor, yalnızca aynı iddiayı Türkçenin kendi kuruluşuyla söylüyor. Kaynak bir sonuç ya da olgu içeriyorsa ("yöntem işi yarı sürede bitiriyor") onu öne çıkar, çünkü somut sonuç soyut değerlendirmeden her zaman güçlüdür. Kaynakta yoksa ekleme. Somut bilgiyi "Sana kalan" bölümünde kullanıcıdan iste.

## 2. Asistan izleri

Sohbet arayüzünden metne sızan cümleler. Her biri tek başına metni ele verir. Hiç düşünmeden sil.

- Açılış onayları: "Elbette!", "Tabii ki!", "Harika bir soru!", "Memnuniyetle."
- Duyurular: "Bu yazıda ... ele alacağız", "Aşağıda ... bulabilirsiniz", "İşte dikkat etmeniz gereken 5 nokta:"
- Davetler: "Gelin birlikte bakalım", "Hadi keşfedelim", "Hiç merak ettiniz mi?"
- Vedalar: "Umarım yardımcı olur", "Başka bir sorunuz olursa...", "Keyifli okumalar!"
- Yazışma çevirileri: "Umarım bu e-posta sizi iyi bulur" (I hope this email finds you well), "İletişime geçmekten çekinmeyin" (don't hesitate to contact), "Bu haberi paylaşmaktan mutluluk duyuyorum" (I'm thrilled to share)

Metin ne yapacağını duyurmaz, yapar. İlk cümle doğrudan ilk fikirdir.

## 3. Şablon giriş ve kapanışlar

Onarım sütunundaki somut bilgiler (zaman, sayı, örnek) yalnızca kaynakta varsa kullanılır.

| Kalıp | Sorun | Onarım |
|---|---|---|
| Günümüzde, çağımızda, modern dünyada | Zaman belirtmiyor, her konuya uyuyor | Belirli zaman ("2020'den beri") ya da sil |
| Hızla değişen dünyada, dijital çağda | "In today's fast-paced world" | Sil, değişimi bir örnekle göster |
| Teknolojinin hızla gelişmesiyle birlikte | Gerekçe gibi duran boş zarf | Hangi teknoloji neyi değiştirdi, onu söyle |
| Son yıllarda giderek artan bir ilgi | Kalıplaşmış eğilim ifadesi | Kaynakta varsa sayı ver, yoksa "giderek daha çok ilgi görüyor" gibi sade söyle |
| Her zamankinden daha önemli | "More than ever" | Neden şimdi önemli, tek cümle |
| Hayatımızın ayrılmaz bir parçası | "Integral part of" | Ne kadar yer kapladığını söyle |
| Geleceği şekillendirecek | "Shape the future" | Neyi nasıl değiştireceğini söyle |
| Unutmamak gerekir ki, belirtmekte fayda var | Uyarı kılığında dolgu | Uyarıyı at, söyleneceği söyle |
| Sonuç olarak, özetle, kısacası | Özet kapanışın işareti | Son paragraf yalnızca tekrar ediyorsa tamamen sil |
| Kariyer yolculuğu, dönüşüm yolculuğu | Mecazi "journey" | "süreç", "yıllar" ya da süreyi ver |

En güçlü onarım çoğu zaman ilk ve son paragrafa dokunmaktır. Yapay zekâ metinleri genel bir girişle açılıp girişi tekrarlayan bir özetle kapanır. İnsan yazısı genellikle konunun ortasından girer ve son paragrafta yeni bir şey söyler ya da hiç özet yapmaz.

## 4. Çeviri söyleyişler

İngilizce kalıpların birebir aktarımı. Türkçe yapay zekâ metninin en ayırt edici katmanı budur, çünkü model Türkçe yazarken İngilizce düşünür.

| Çeviri | Kaynak | Türkçenin kendi yolu |
|---|---|---|
| önemli/kritik/kilit bir rol oynamak | play a key role | "X olmadan Y olmaz", "X belirliyor", "X'e bağlı" |
| büyük önem taşımak, önem arz etmek, öneme sahip olmak | is of great importance | önemli olduğunu gösteren sonucu söyle |
| potansiyele/kapasiteye sahip | has the potential | "-ebilir", "X'i var" |
| bir üst seviyeye taşımak | take to the next level | neyin nasıl iyileştiğini söyle |
| oyunun kurallarını değiştirmek | game changer | değişikliği anlat |
| değer katmak | add value | ne kazandırdığını söyle |
| ışık tutmak | shed light on | açıklamak, göstermek |
| kapılarını aralamak | open the doors to | mümkün kılmak, yolunu açmak |
| potansiyelini ortaya çıkarmak | unlock potential | kişinin ne yapabileceğini söyle |
| içgörü | insight | fikir, bulgu, gözlem, ders |
| değerli bilgiler/ipuçları | valuable insights/tips | sıfatı at, bilgiyi ver |
| geniş bir yelpazede, birçok farklı | a wide range of | sayı ya da iki somut örnek |
| etkili/başarılı/sorunsuz bir şekilde | effectively/successfully | "-ce/-ca", yalın sıfat ya da başka fiil |
| değişimi kucaklamak | embrace change | benimsemek, ayak uydurmak |
| deneyimlemek | to experience | yaşamak, denemek, görmek, tatmak |
| en iyi uygulamalar | best practices | işe yarayan yöntemler |
| dijital manzara, iş manzarası | landscape | piyasa, durum, tablo |
| zengin bir mozaik/doku | rich tapestry | çeşitliliği adlarıyla say |
| temel taşı, itici güç | cornerstone, driving force | nedensellik fiili |
| cevabı X'te yatıyor | the answer lies in | "X'e bağlı", "X'ten geçiyor" |
| başarının anahtarı | the key to success | "en önemlisi", "belirleyen" |
| günün sonunda, | at the end of the day | sonuçta, neticede |
| akılda tutmak | keep in mind | unutmamak ya da hiç uyarmamak |
| hayatınızı kolaylaştırmak | make your life easier | hangi işi kısalttığını söyle |
| bu da ... anlamına geliyor | this means | yani, demek ki, ya da sonucu doğrudan söyle |

**"Bir şekilde" sorunu.** İngilizce "-ly" zarfları Türkçeye "X bir şekilde" olarak geçer: "etkili bir şekilde", "hızlı bir şekilde", "doğru bir şekilde". Türkçe ise ya "-ce/-ca" eki kullanır ("dikkatlice", "kolayca"), ya sıfatı doğrudan zarf yapar ("hızlı çalışıyor", "iyi anlattı"), ya da fiili değiştirir ("başarılı bir şekilde tamamladık" yerine "bitirdik").

## 5. Boş sıfatlar ve dolgu sözleri

**Değerlendirme sıfatları:** eşsiz, benzersiz, paha biçilmez, olağanüstü, büyüleyici, muhteşem, inanılmaz, etkileyici, nefes kesici, unutulmaz, vazgeçilmez, kusursuz.

Bunlar okura ne düşüneceğini söyler ama nedenini göstermez. Onarım: sıfatı sil, yerine sıfatı hak ettiren ayrıntıyı koy. "Eşsiz bir manzara" yerine "terastan bütün körfez görünüyor". Ayrıntı kaynakta yoksa sıfatı sil ve öyle bırak.

**Vurgu dolguları:** gerçekten de, tam anlamıyla, kelimenin tam anlamıyla, gerçek anlamda, esasen, özünde, son derece, hiç şüphesiz, kuşkusuz.

**Kaçamaklar:** bir bakıma, bir anlamda, belli bir ölçüde, önemli ölçüde, kayda değer ölçüde.

**Belirsiz benzetme:** "adeta", "sanki" somut ayrıntının yerine kullanıldığında. "Şehir adeta bir açık hava müzesi" yerine ya müzeyi andıran ayrıntıyı ver ya da cümleyi sil.

Türkçe vurguyu sözcük ekleyerek değil, sözcük dizilişiyle yapar. Vurgulanan öge yüklemin hemen önüne gelir: "Bu kararı Ayşe verdi." cümlesinde vurgu Ayşe'dedir. Yüklemin önüne alınan öge "gerçekten de" gibi bir dolguya gerek bırakmaz.

## 6. Bürokratik geçişler

| Geçiş | Yerine |
|---|---|
| Bu bağlamda, bu çerçevede, bu doğrultuda, bu noktada | gerçek mantıksal bağ ("bu yüzden", "oysa", "üstelik") ya da hiçbiri |
| Bunun yanı sıra, buna ek olarak, ek olarak | "üstelik", "bir de", "ayrıca" (seyrek) ya da sil |
| Öte yandan, diğer taraftan, bununla birlikte | "oysa", "ama", "yine de" ya da karşıtlığı cümlenin içine al |
| İlk olarak, ikinci olarak, son olarak | sil, sıra paragraflardan zaten belli |
| Söz konusu | "bu" ya da adı tekrarla |
| ... ilişkin olarak, belirtildiği üzere | "ile ilgili", "hakkında" ya da cümleyi baştan kur |

Yapay zekâ cümlelerin dörtte birinden fazlasını bir geçişle açar ve geçişten sonra virgül koyar ("Ancak, ...", "Ayrıca, ..."). İkisi de İngilizce alışkanlığıdır. İnsan yazısında cümlelerin çoğu doğrudan özneyle ya da tümleçle başlar. Kalan geçişler de ya virgülsüz yazılır ("Ama kimse gelmedi.") ya da cümlenin içine yerleşir ("Kimse gelmedi ama...").

## 7. Retorik kalıplar

**"Sadece X değil, aynı zamanda Y."** En çok tanınan imza. Onarım: "hem X hem Y", iki ayrı cümle ya da yalnızca Y. Çoğu zaman X'e hiç gerek yoktur.

**"Bu bir X değil, Y."** Dramatik karşıtlık. Yalnızca Y'yi söyle. İnsan yazarlar bu yapıyı da kullanır, ama metin başına bir kez ve gerçekten bir yanlış anlamayı düzeltmek için.

**"Asıl mesele şudur: ..."** ve "Gerçek şu ki ..." İddianın önüne konan duyuru. Duyuruyu sil, iddiayı doğrudan söyle. Cümleyi "X olan Y" yapısına sıkıştırmaya çalışma, bu bozuk Türkçe üretir.

| Yapay zekâ | Yanlış onarım | Doğru onarım |
|---|---|---|
| Asıl mesele şudur: kimse sorumluluk almıyor. | Asıl meselenin kimsenin sorumluluk almaması olduğu. | Kimse sorumluluk almıyor. Mesele bu. |

**"Sonuç mu? Kaos."** Soru sorup tek sözcükle cevaplama. Reklam metninden geçme. Metin başına en fazla bir kez.

**Zorlama üçlüler.** "Hızlı, güvenilir ve kullanıcı dostu." Model her şeyi üçlü sayar. Gerçek liste kaç öğeliyse o kadar say. İki öğe de olur, dört de.

## 8. Ek ve destek fiil yükü

**-mekte/-makta yığılması.** "Kullanılmaktadır, görülmektedir, bulunmaktadır." Resmi ve akademik metinde yerindedir ama orada bile her cümlede olmaz. Diğer üsluplarda neredeyse hiç kullanılmaz.

| Yerine kullanılabilecek | Örnek |
|---|---|
| Geniş zaman (-ir) | "Sistem verileri gece işler." |
| Şimdiki zaman (-iyor) | "Veriler gece işleniyor." |
| Görülen geçmiş (-di) | "Ekip yöntemi geçen yıl değiştirdi." |
| Yalın ad cümlesi | "Sonuç açık." |
| -dir (genelleme için, seyrek) | "Bu tür hatalar yaygındır." |

**Destek fiiller.** Ad + "gerçekleştirmek / sağlamak / sunmak / olanak tanımak". "Analiz gerçekleştirdik" yerine "inceledik", "avantaj sağlar" yerine "işi hızlandırır", "imkân sunar" yerine "-ebilirsiniz".

**Ad-fiil zincirleri.** "Uygulanmasının sağlanmasının önemi" gibi -ma/-me ekli adların art arda dizilmesi. Zinciri çöz ve fiile çevir: "Uygulamak önemli."

**"-ebilir" yığılması.** Model her yüklemi "-ebilir" yapar: "yol açabilir, neden olabilir, etkileyebilir". Ama bu olasılık ifadeleri kaynağın iddiasıdır ve silinmez. Yapılacak iş tekrarı azaltmaktır: aynı cümlede ya da art arda gelen cümlelerde biriken "-ebilir"leri tek bir olasılık ifadesinde topla ("Sınır bulanıklaşınca tükenmişlik riski doğabiliyor.") ya da kipi çeşitlendir ("-ebiliyor", "gibi görünüyor", "riski var"). Olasılığı kesinliğe çevirme.

**"Haline gelmek", "olarak değerlendirilmek".** "Yaygın hale geldi" yerine "yaygınlaştı". "Dönüm noktası olarak değerlendiriliyor" yerine kimin değerlendirdiğini söyle.

## 9. Regex'in göremediği dilbilgisel imzalar

Bunları analiz betiği yakalamaz. Okurken sen yakalarsın.

**Gereksiz zamir.** Türkçe özneyi fiil ekinden anlar. "Ben bu konuda düşündüm ve ben şuna karar verdim" İngilizce kuruluştur. Doğrusu: "Düşündüm ve şuna karar verdim." Zamir yalnızca vurgu ya da karşıtlık için kullanılır: "Ben gelirim, sen kal."

**"Bir" tanımlığı fazlalığı.** İngilizce "a/an" Türkçeye fazladan "bir" olarak geçer: "önemli bir rol", "büyük bir fırsat", "kapsamlı bir analiz". Her "sıfat + bir + ad" yanlış değildir, ama bir paragrafta beş tane varsa çeviri kokusu verir. "Büyük fırsat", "kapsamlı analiz" çoğu zaman yeter.

**"Olarak" yığılması.** "Sonuç olarak, uzman olarak, yaygın olarak, temel olarak, aktif olarak". Bir paragrafta üçten fazlaysa çoğunu at: "aktif olarak kullanıyor" yerine "kullanıyor".

**"Tarafından" ile edilgen.** "Rapor ekip tarafından hazırlandı" (the report was prepared by the team). Türkçe etken çatıyı sever: "Raporu ekip hazırladı."

**Sağa dallanan uzun özne.** İngilizce "The fact that X, which Y, is Z" kuruluşunun çevirisi, öznesi bir türlü bitmeyen cümleler üretir. Türkçede özne kısa kalır, uzun bilgi yüklemden önceki tümleçlere ya da ayrı cümleye taşınır.

**Hep düz sıralama.** Model her cümleyi Özne-Tümleç-Yüklem sırasıyla kurar ve hiç devrik cümle yazmaz. Deneme ve edebi metinde ara sıra devrik cümle doğaldır: "Gitti işte, dönmedi bir daha."

**Söylem belirteci kıtlığı.** İnsan Türkçesi "de/da, bile, zaten, hani, işte, artık, ki" gibi küçük sözcüklerle doludur. Yapay zekâ metninde bunlar ya hiç yoktur ya da yalnızca "ise" ve "ancak" vardır. Ayrıntı: `references/insan-sesi.md`.

**Eş anlamlı rotasyonu.** Aynı şeye her cümlede başka bir ad vermek ("şirket", "kuruluş", "firma", "işletme"). İnsan yazar terimi seçer ve tekrarlamaktan korkmaz. Teknik terimleri sabit tut, yalnızca genel sözcükleri çeşitlendir.

**Söyleme fiili çeşitlemesi.** "Belirtti, ifade etti, vurguladı, dile getirdi, altını çizdi" diye dönüp duran haber metni. Haberde bunlar yerindedir, ama "dedi" ve "söyledi" de Türkçedir ve tekrar edilebilir.

**Tipografi.** Ondalık ayracı virgül (3,5), binlik ayracı nokta (1.000), yüzde işareti sayıdan önce (%40), tarih "10 Kasım 2026" biçiminde yazılır. "3.5", "1,000", "40%" ya da "Kasım 10, 2026" İngilizce biçimdir. Ayrıntı: `references/noktalama-ve-yazim.md`.

## 10. Bağlamın kalıbı akladığı durumlar

Sözlükteki her eşleşme bir hata değildir. Şu durumlarda dokunma:

- **Terim olarak kullanılan sözcük.** Biyoloji metninde "ekosistem", yazılım metninde "en iyi uygulamalar" (best practices) yerleşik terimdir.
- **Hukuki ve resmi kalıplar.** Sözleşmede "söz konusu", "işbu", "hususunda", "-mektedir" türün gereğidir. Bunları gündelik dile çevirmek metnin işlevini bozar.
- **Gerçek gönderim.** "Uzay yolculuğu" mecaz değildir. "Kapıyı araladı" gerçek bir kapı olabilir. "Filmde önemli bir rol oynadı" oyunculuktur.
- **Doğrudan alıntı.** Başkasının sözü olduğu gibi kalır.
- **Yazarın bilinçli tercihi.** Ses kartı varsa ve yazar bir ifadeyi sık kullanıyorsa o ifade yazarındır, imza değil.

Şüphedeysen tek bir kısa soru sor ya da dokunma ve "Ne değişti" bölümünde belirt.

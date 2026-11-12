# Noktalama ve Yazım

Bu dosya skill'in noktalama varsayılanlarını ve Türkçe tipografi kurallarını anlatır. Kurallar TDK Yazım Kılavuzu ile modern Türkçe düz yazı pratiğine dayanır. Bir kuralın TDK'daki kesin hâli için [tdk.gov.tr](https://www.tdk.gov.tr) adresindeki yazım kılavuzuna bakılmalıdır. Bu dosya bir yazım kılavuzu değil, yapay zekâ izini temizlemeye yönelik bir uygulama notudur.

## Varsayılanlar

Bunlar mutlak yasak değil, güçlü varsayılanlardır. Bir yazar bilinçli olarak kullanıyorsa (ses kartı ya da açık talep) yazara uyulur.

### Uzun çizgi (—)

**Varsayılan:** Ara söz için hiç kullanılmaz.

Türkçe yapay zekâ çıktısı uzun çizgiyi İngilizce em dash gibi, cümle içinde ara söz açmak için kullanır. TDK uzun çizgiyi esas olarak konuşma çizgisi (diyalog) olarak tanımlar. Modern Türkçe düz yazıda ara söz virgülle, parantezle ya da cümleyi bölerek verilir.

| Yapay zekâ | Onarım |
|---|---|
| Bu yöntem — özellikle büyük ekiplerde — sorun yaratır. | Bu yöntem, özellikle büyük ekiplerde, sorun yaratır. |
| Sonuç belliydi — kimse gelmedi. | Sonuç belliydi. Kimse gelmedi. |
| Üç şehir — Ankara, İzmir, Bursa — seçildi. | Üç şehir seçildi: Ankara, İzmir ve Bursa. |

**İstisna:** Edebi metinde satır başındaki diyalog çizgisi kaynakta varsa korunur. Kaynakta yoksa eklenmez, diyalog tırnakla verilir.

Boşluklu kısa çizgi ( - ) ve boşluklu en dash ( – ) ile yapılan ara sözler biraz farklıdır. TDK ara sözün kısa çizgiyle ayrılmasına da izin verir, bu yüzden kaynakta tek tük geçiyorsa dokunma. İmza olan şey yığılmadır: aynı paragrafta birden fazla çizgili ara söz varsa virgüle ya da paranteze çevir. Analiz betiği de kısa çizgi için 300 kelimede bir kullanımlık pay bırakır.

### Noktalı virgül (;)

**Varsayılan:** Düz yazıda kullanılmaz. Cümle ikiye bölünür.

TDK noktalı virgüle izin verir ama modern Türkçe düz yazıda nadirdir. Yapay zekâ ise onu İngilizce "; however / ; also" mantığıyla sık kullanır.

| Yapay zekâ | Onarım |
|---|---|
| Plan hazırdı; ancak uygulamada aksadı. | Plan hazırdı ama uygulamada aksadı. |
| Kalbinde hüzün vardı; umudu da hâlâ yaşıyordu. | Kalbinde hüzün vardı. Umudu da hâlâ yaşıyordu. |

**İstisna:** Resmi ve hukuki metinlerde madde sıralamasında kaynakta varsa ("a) ...; b) ...;") yapı gereği korunur.

### Cümle başı bağlaçtan sonra virgül

**Varsayılan:** Konmaz.

"Ancak, ...", "Ayrıca, ...", "Bu nedenle, ...", "Sonuç olarak, ..." İngilizce "However, / Moreover," alışkanlığıdır. Türkçede bu bağlaçlardan sonra virgül genellikle gerekmez: "Ancak kimse gelmedi."

"Evet, hayır, peki, tamam" gibi cevap sözlerinden sonraki virgül ise doğrudur ve kalır: "Peki, öyle olsun."

### Karşıtlık bağlacından önce virgül

**Varsayılan:** "ama, fakat, ancak, lakin" öncesinde virgül konmaz.

"Plan hazırdı, ancak aksadı." yerine "Plan hazırdı ancak aksadı." Bu konuda kullanım karışıktır ve virgüllü yazan insan yazarlar da vardır. Skill virgülsüz biçimi tercih eder, çünkü yapay zekâ virgülü sistematik olarak koyar. Ses kartı yazarın virgül koyduğunu gösteriyorsa yazara uy.

### Cümle içi iki nokta

**Varsayılan:** Seyrek.

İki nokta açıklama ve örnek sıralamak için doğaldır: "Üç şehir seçildi: Ankara, İzmir ve Bursa." Ama yapay zekâ onu dramatik açıklama için kullanır: "Sonuç açık: değişim kaçınılmaz." "Asıl mesele şudur: ..." Metin başına bir iki kez yeter.

İki noktadan sonra cümle devam ediyorsa küçük harfle başlar. Yeni ve bağımsız bir cümle ya da alıntı geliyorsa büyük harf kullanılır.

### Ünlem

Kurumsal ve profesyonel metinde ünlem neredeyse hiç kullanılmaz. Sosyal medya gönderisinde bir tane yeterlidir. Art arda ünlemli cümleler ("Harika bir haber! Kitabım çıktı!") pazarlama ve yapay zekâ kokusu verir.

## Türkçe tipografi

| Konu | Doğru | Yanlış (İngilizce biçim) |
|---|---|---|
| Ondalık | 3,5 | 3.5 |
| Binlik | 1.250.000 | 1,250,000 |
| Yüzde | %40 | 40% |
| Tarih | 10 Kasım 2026 | Kasım 10, 2026 |
| Saat | 14.30 ya da 14:30 | 2:30 PM |
| Sıra sayısı | 19. yüzyıl, 3. kat | 19th yüzyıl |
| Para | 250 TL, 1.500 lira | TL250 |

**Kesme işareti.** Özel adlara gelen ekler kesmeyle ayrılır: "İstanbul'da", "Ayşe'nin", "2026'da". Kurum, kuruluş ve kurul adlarına gelen ekler ise TDK'ya göre kesmeyle ayrılmaz: "Türk Dil Kurumuna", "Millî Eğitim Bakanlığının". Kaynak bu konuda tutarlıysa kaynağa uy.

**Bağlaç "de/da" ve "ki".** Bağlaç olan "de/da" ve "ki" ayrı yazılır: "Ben de geldim.", "Duydum ki gitmişsin." Kalıplaşmış "belki, çünkü, sanki, hâlbuki, oysaki, mademki" bitişiktir. Soru eki "mi" ayrı yazılır.

**Şapka.** "Yapay zekâ", "hâlâ", "kâr", "imkân" gibi yazımlarda TDK şapkalı biçimi önerir. Kaynakta şapkasız yazılmışsa ("yapay zeka") tutarlılığı bozma. Metin içinde tek bir biçim kullan.

**Büyük harf.** Başlıklarda her sözcüğü büyük harfle başlatmak Türkçede de kullanılır ve hata değildir. Yalnızca yayın kuralına ya da metnin kendi içindeki tutarlılığa bak. Başlık biçimine dokunma, yalnızca bir metin içinde karışık kullanılıyorsa tek biçime getir.

**Tırnak.** "Çift tırnak" ya da “kıvrık tırnak” kullanılabilir. Metin içinde tutarlı ol.

## Kasıtlı hata yok

Skill hiçbir zaman yazım hatası, eksik harf, bozuk dilbilgisi ya da tutarsız noktalama eklemez. İnsan yazısı kusurlu olabilir ama kusur eklemek insanlaştırmak değildir. Yapılacak iş metni iyi bir Türk yazarın yazacağı gibi yazmaktır.

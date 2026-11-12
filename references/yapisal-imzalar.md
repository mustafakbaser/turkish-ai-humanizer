# Yapısal İmzalar

Yapay zekâ metni sözcüklerden önce iskeletinden tanınır. Bu dosya paragraf ve belge düzeyindeki imzaları ve onarım yollarını anlatır. Sözcük düzeyi için `references/kalip-sozlugu.md` dosyasına bakılır.

## Belge düzeyi

**Şablon iskelet.** Genel bir girişle açılış ("Günümüzde X önemli bir konu"), üç ya da beş eşit bölüm, her bölümde aynı yapı, girişi tekrarlayan bir "Sonuç" paragrafı. Onarım:

- Girişi at ya da konunun ortasından gir. İlk cümle okura yeni bir şey söylesin.
- Son paragraf yalnızca özetliyorsa sil. Kalacaksa yeni bir gözlem, bir soru ya da bir sonraki adım söylesin.
- Bölüm uzunluklarını içerik belirlesin.

**Başlık enflasyonu.** 500 kelimelik bir yazıda dört ara başlık, her başlıkta iki nokta ("Uzaktan Çalışma: Fırsatlar ve Zorluklar"), soru biçiminde başlıklar ("Peki, Uzaktan Çalışma Nedir?"). İnsan yazısında ara başlık ancak metin uzadığında gelir. Yapıya dokunma iznin yoksa başlıkları silme ama iki noktalı ve soru biçimli başlıkları sadeleştirmeyi "Sana kalan" bölümünde öner. **İstisna:** SEO için yazılmış bir metinde soru biçimli başlıklar ve SSS bölümü bilinçli bir tercihtir (arama sonuçlarındaki soru kutuları bu başlıkları kullanır). Kullanıcı SEO'dan söz ettiyse ya da metin anahtar kelime odaklıysa bu başlıklara ve başlıklardaki anahtar kelimelere dokunma.

**Her şeyi listeleme.** Düz yazıyla anlatılacak bir akıl yürütmeyi maddelere bölmek. Madde, sıralanabilir ve birbirinden bağımsız öğeler içindir. Gerekçe, neden-sonuç, karşıtlık düz yazı ister.

**Kalın etiketli maddeler.** "**Verimlilik:** Çalışanlar daha verimli olur." biçimi. Her madde aynı kalıpla başlar, etiket ile açıklama aynı şeyi iki kez söyler. Onarım: etiketi at ve maddeyi tek cümle yap, ya da maddeleri düz yazıya çevir.

**Emoji madde işaretleri ve süsler.** ✅, 🚀, 💡, 👉 ile başlayan satırlar, başlık başına emoji. Sosyal medya gönderisinde bir iki emoji doğaldır, her satırda değil.

**Hazır ekler.** "Sıkça Sorulan Sorular", "Önemli Not:", "Özet", "TL;DR", "Anahtar Çıkarımlar" bölümleri. İstenmediyse ekleme. SEO metnindeki SSS bölümü kullanıcının tercihidir, korunur. Kaynakta varsa ve yapıya dokunma iznin varsa sadeleştirmeyi öner.

**Yapıya ne zaman dokunulur?** Varsayılan olarak hiç. Başlık, liste, tablo, alıntı ve kod yerinde kalır. Kullanıcı "yapıyı da düzelt" derse ya da derin yoğunluk seçerse, yapısal imzaları sadeleştirebilirsin. Her yapısal değişikliği "Ne değişti" bölümünde belirt.

## Paragraf düzeyi

**Okul paragrafı.** Konu cümlesi, iki destek cümlesi, toparlama cümlesi. Her paragrafta aynı. Onarım: bazı paragraflar doğrudan örnekle başlasın, bazıları bir olguyla bitsin, bazıları tek cümle olsun.

**Toparlama cümlesi.** Paragrafı "Bu da X'in ne kadar önemli olduğunu göstermektedir." gibi bir değerlendirmeyle kapatmak. Değerlendirmeyi sil, paragraf son bilgi cümlesiyle kapansın.

**Simetrik denge.** "Bir yandan ... öte yandan", "avantajları ... dezavantajları". Gerçek bir karşıtlık varsa kalsın ama şablon olarak değil. Bir tarafa daha çok yer vermek doğaldır.

**Tekrar eden açılış.** Art arda üç cümlenin "Bu" ile başlaması, ya da her paragrafın bir geçişle ("Ayrıca", "Bunun yanı sıra", "Son olarak") açılması. `analiz.py` en sık açılış sözcüğünü ve resmi geçiş oranını raporlar.

**Bilgi eklemeyen yeniden ifade.** "Yani başka bir deyişle", "Diğer bir ifadeyle" ile aynı şeyi ikinci kez söylemek. Bir kez söyle.

## Cümle düzeyi

**Orta boy tekdüzelik.** Bütün cümleler aşağı yukarı aynı boyda (bu projenin örneklerinde çoğunlukla 9-14 kelime). Ritim için `references/insan-sesi.md` bölüm 1.

**Önce bağlam, sonra iddia.** Her cümle bir yan cümleyle açılır ("X göz önüne alındığında", "Y açısından değerlendirildiğinde") ve asıl iddia sona kalır. Bazen iddiayla başla.

**İki noktalı açıklama.** "Sonuç açık: X." Bir metinde bir kez doğal, beş kez şablon.

**Uzun çizgiyle ara söz.** "Bu yöntem — özellikle büyük ekiplerde — sorun yaratır." İngilizce em dash alışkanlığı. Virgül, parantez ya da iki cümle.

## Onarım sırası

Yukarıdan aşağıya çalış. Belge iskeleti bozuksa cümle cilalamak işe yaramaz.

1. Belge: giriş, kapanış, bölüm dengesi, başlıklar ve listeler (izin varsa)
2. Paragraf: okul paragrafı, toparlamalar, açılış tekrarları
3. Cümle: ritim, sıralama, iki nokta ve çizgi
4. Sözcük: kalıplar, ekler, belirteçler
5. Noktalama ve yazım

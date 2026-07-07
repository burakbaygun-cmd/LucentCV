# Sprint 1 — Backlog Dağıtma Mantığı ve Story Seçimleri

## 1. Sprint Planlama (Sprint Planning)
Sprint 1 planlama toplantısı yapılmıştır. Bu sprintte projenin temel iskeletini oluşturmak, LLM orkestrasyonunu (CV Analizi, İlan Analizi, Eşleştirme ve Mülakat modülleri) kurmak ve veritabanı (Supabase) katmanını tamamlamak hedeflenmiştir. Toplam sprint kapasitesi **20 Story Point (SP)** olarak belirlenmiştir.

## 2. User Story'ler (Kullanıcı Hikayeleri) & Story Point'ler
Sprint 1 kapsamında ele alınan ana işler kullanıcı hikayelerine (User Story) bölünmüş ve Fibonacci serisi kullanılarak puanlandırılmıştır:

### US-01: CV ve İş İlanı Metin Analizi (5 SP)
* **Açıklama:** Bir aday olarak, CV metnimi ve başvurmak istediğim iş ilanını yapıştırıp analiz edebilmek istiyorum; böylece sistemin bu verileri anlamlandırıp ayrıştırmasını sağlayabilirim.
* **Kabul Kriterleri (Acceptance Criteria):**
  * CV ve ilan metinlerinin başarılı şekilde analiz edilmesi.
  * Beceriler, deneyim yılı ve eğitim gibi bilgilerin yapılandırılmış formatta çıkarılması.

### US-02: CV-İlan Eşleştirme ve Öneri Sistemi (5 SP)
* **Açıklama:** Bir aday olarak, analiz edilen CV'm ile ilan arasındaki uyum skorunu, eksik becerilerimi ve iyileştirme önerilerini görmek istiyorum; böylece CV'mi ilana uygun hale getirebilirim.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Uyum skorunun hesaplanması.
  * Eksik yeteneklerin listelenmesi.
  * En az 3-4 somut öneri üretilmesi.

### US-03: Akıllı Mülakat Soruları Üretimi (3 SP)
* **Açıklama:** Bir aday olarak, CV ve ilan eşleşme sonuçlarıma göre bana özel üretilmiş mülakat soruları almak istiyorum; böylece zayıf ve güçlü yönlerime göre mülakata hazırlanabilirim.
* **Kabul Kriterleri (Acceptance Criteria):**
  * CV ve ilan analizine göre tam olarak 5 adet kişiselleştirilmiş mülakat sorusunun oluşturulması.

### US-04: Mülakat Değerlendirme ve Feedback Sistemi (5 SP)
* **Açıklama:** Bir aday olarak, mülakat sorularına verdiğim yanıtların değerlendirilmesini ve detaylı geri bildirim almayı istiyorum; böylece mülakat performansımı analiz edebilirim.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Her soru için puan ve yapıcı geri bildirim üretilmesi.
  * Genel mülakat skorunun hesaplanması.

### US-05: Analiz Geçmişi ve Hafıza Sistemi (2 SP)
* **Açıklama:** Bir aday olarak, geçmişte yaptığım analizleri ve mülakat sonuçlarını tekrar görebilmek istiyorum; böylece gelişimimi takip edebilirim.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Geçmiş analizlerin listelenmesi.
  * Üzerine tıklandığında detayların görüntülenebilmesi.

**Toplam Puan:** 20 SP

## 3. Backlog Açıklaması
Product Backlog, kullanıcıların uygulamadan alacağı temel değerlere (değer önerisi) göre önceliklendirilmiştir. Sprint başına hedeflenen toplam puan (20 SP), tek kişilik aktif geliştirici kapasitesine göre gerçekçi şekilde sınırlandırılmıştır. 
Miro board üzerinde mavi kartlar ana **User Story**'leri, kırmızı kartlar ise bu hikayelerin altındaki teknik işleri (**Task**'leri) temsil etmektedir. Story puanları belirlenirken işin karmaşıklığı, belirsizlik derecesi ve gerektirdiği efor göz önünde bulundurulmuştur.

## 4. GitHub Project Linki
Proje süreçlerini takip ettiğimiz Kanban tahtasına ve iş listesine aşağıdaki bağlantıdan ulaşabilirsiniz:
[LucentCV GitHub Project Board](https://github.com/users/AsilDogukanSamay/projects/1/views/1)

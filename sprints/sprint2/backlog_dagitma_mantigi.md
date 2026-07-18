# Sprint 2 — Backlog Dağıtma Mantığı ve Story Seçimleri

## 1. Sprint Planlama (Sprint Planning)
Sprint 2 planlama toplantısı yapılmıştır. Bu sprintte projenin Streamlit monolit yapısından modern Next.js frontend + FastAPI backend mimarisine taşınması, Supabase entegrasyonu, kimlik doğrulama/oturum yönetimi katmanlarının yazılması, mülakat simülasyonunun ve PDF çıktısının aktif edilmesi hedeflenmiştir. 

Toplam sprint kapasitesi ekip üyelerinin genişlemesiyle birlikte **37 Story Point (SP)** olarak belirlenmiştir.

## 2. User Story'ler (Kullanıcı Hikayeleri) & Story Point'ler

### US-06: Modern Mimari Dönüşümü ve Temel UI Altyapısı (8 SP)
* **Açıklama:** Bir yazılımcı/geliştirici olarak, uygulamanın Streamlit tabanlı monolitik yapısını Next.js ve FastAPI olarak iki katmana bölmek istiyorum; böylece uygulamanın ölçeklenebilirliğini, hızını ve UI esnekliğini artırabilirim.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Next.js (frontend) ve FastAPI (backend) iskelet yapısının kurulması.
  * API haberleşme altyapısının kurulması.
  * Tasarım sistemine (Tailwind CSS, Shadcn) uygun temel dashboard şablonlarının çıkarılması.
  * *Sorumlu:* Asil

### US-07: Kimlik Doğrulama, Oturum Yönetimi ve Google Auth (5 SP)
* **Açıklama:** Bir aday olarak, uygulamaya e-posta/şifre veya Google hesabımla giriş yapabilmek, oturumumu açık tutabilmek ve çıkış yapabilmek istiyorum; böylece kişisel analiz geçmişimi güvenle saklayabilirim.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Supabase Auth kullanılarak Kayıt ve Giriş ekranlarının kodlanması.
  * Korumalı rotalar (`AuthGuard`) aracılığıyla yetkisiz kullanıcıların engellenmesi.
  * Google OAuth ile tek tıkla giriş desteğinin aktif edilmesi.
  * Çıkış (Logout) fonksiyonunun Navbar'a entegre edilmesi.
  * *Sorumlu:* Burak / Asil (Ortak Geliştirme)

### US-08: Mülakat Simülasyonu ve Arayüz Temaları (5 SP)
* **Açıklama:** Bir aday olarak, CV ve ilan analiz sonuçlarıma göre oluşturulan mülakat sorularını interaktif olarak cevaplayabilmek ve arayüzü göz yormayacak şekilde karanlık/aydınlık temalarda görebilmek istiyorum.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Mülakat soruları ve cevap değerlendirme modülünün frontend'de çalışır hale getirilmesi.
  * Dark / Light mode geçişinin (Next Themes) tüm bileşenlerle uyumlu şekilde eklenmesi.
  * *Sorumlu:* Nuri

### US-09: Modern Bildirimler, Popup'lar ve PDF Çıktı Entegrasyonu (5 SP)
* **Açıklama:** Bir aday olarak, analiz sonuçlarımı ve mülakat raporlarımı PDF olarak dışa aktarabilmek, verilerimi silerken veya işlem yaparken modern uyarı pencereleriyle karşılaşmak istiyorum.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Ham tarayıcı diyaloglarının (`window.alert`, `window.confirm`) Shadcn AlertDialog ve Sonner/Toast bildirimleri ile değiştirilmesi.
  * Analiz raporlarının PDF formatında başarıyla dışa aktarılması.
  * *Sorumlu:* Büşra / Ece

## 3. Backlog Açıklaması
Sprint 2 ile birlikte ekibe yeni üyelerin katılmasıyla iş bölümü yapılmış ve kapasite 37 SP'ye çıkarılmıştır. Story Point puanlamaları işlerin teknik karmaşıklığı, tasarım eforu ve entegrasyon belirsizlikleri (örneğin OAuth ve PDF oluşturma) göz önünde bulundurularak yapılmıştır.

## 4. GitHub Project Linki
Tüm süreçleri ve Kanban kartlarını takip ettiğimiz proje tahtasına aşağıdaki bağlantıdan ulaşabilirsiniz:
[LucentCV GitHub Project Board](https://github.com/users/AsilDogukanSamay/projects/1/views/1)

# Sprint 3 — Backlog Dağıtma Mantığı ve Story Seçimleri

## 1. Sprint Planlama (Sprint Planning)
Sprint 3 planlama toplantısında projenin canlı prodüksiyon ortamına (Production) alınması, yayın sonrası güvenlik, CORS ve environment değişkenleri optimizasyonları, uçtan uca testlerin icrası, final sunum videosu ve proje teslim dökümantasyonunun tamamlanması hedeflenmiştir. 

Toplam sprint kapasitesi **42 Story Point (SP)** olarak belirlenmiştir.

## 2. User Story'ler (Kullanıcı Hikayeleri) & Story Point'ler

### US-10: Production Deployment & Cloud Altyapısı (19 SP)
* **Açıklama:** Bir DevOps/Yazılımcı olarak, uygulamanın Next.js frontend kısmını Vercel'e, FastAPI backend kısmını Render/Railway cloud platformlarına canlıya almak, CORS ve Supabase Auth yönlendirmelerini canlı ortama tam uyumlu hale getirmek istiyorum.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Vercel üzerinde Next.js frontend'in 0 hata ile build alınması ve yayınlanması.
  * Render / Railway üzerinde FastAPI backend'in bağımsız web servisi olarak ayağa kalkması.
  * `ALLOWED_ORIGINS` ve `NEXT_PUBLIC_API_URL` değişkenleri ile canlı CORS ve API bağlantılarının kurulması.
  * Supabase Auth & Google OAuth yönlendirme URL'lerinin canlı domainler için yapılandırılması.
  * Deploy sonrası PDF export ve API haberleşme sorunlarının çözülmesi.
  * *Sorumlu:* Asil Doğukan Samay

### US-11: Kapsamlı Dokümantasyon & README Düzenlemesi (8 SP)
* **Açıklama:** Bir kullanıcı ve incelemeci olarak, projenin canlı adreslerini, mimari şemasını, kurulum adımlarını ve ekran görüntülerini detaylı ve güncel bir README dosyasında görmek istiyorum.
* **Kabul Kriterleri (Acceptance Criteria):**
  * README.md dosyasının Sprint 3 vizyonuna uygun şekilde güncellenmesi.
  * Ekran görüntüleri, Miro mimari şemaları ve yayın bağlantılarının eklenmesi.
  * *Sorumlu:* Nuri Duldar

### US-12: Uçtan Uca Kalite Güvence ve Test Senaryoları (8 SP)
* **Açıklama:** Bir test uzmanı olarak, uygulamanın tüm mutlu yol (happy path) ve sınır durum (edge cases) senaryolarını test etmek, tespit edilen bug'ların düzeltilmesini sağlamak istiyorum.
* **Kabul Kriterleri (Acceptance Criteria):**
  * Register → Login → Analysis → Interview → PDF Export akışının uçtan uca test edilmesi.
  * Boş veri, hatalı token ve yetkisiz erişim senaryolarının kontrol edilmesi.
  * *Sorumlu:* Burak Baygün

### US-13: Final Sunum Videosu ve Teslim Kontrolleri (7 SP)
* **Açıklama:** Bir izleyici ve jüri üyesi olarak, projenin değer önerisini ve canlı uygulamanın kullanımını özetleyen 3 dakikalık kaliteli bir final demosunu izlemek istiyorum.
* **Kabul Kriterleri (Acceptance Criteria):**
  * 3 dakikalık video çekilmesi ve YouTube'a yüklenmesi.
  * Tüm repo linkleri ve formların teslim öncesi kontrol edilmesi.
  * *Sorumlu:* Büşra Demir

---

## 3. GitHub Project Linki
Proje Kanban tahtası ve yayın adımları takip bağlantısı:
[LucentCV GitHub Project Board](https://github.com/users/AsilDogukanSamay/projects/1/views/1)

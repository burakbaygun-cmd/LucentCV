# LucentCV — Çok Adımlı AI Agent ile CV-İlan Uyum Analizi

## Takım İsmi
Takım 126

## Takım Elemanları

- **Burak Baygün** – Product Owner & Developer
- **Büşra Demir** – Scrum Master & Developer
- **Asil Doğukan Samay** – Developer
- **Ece Toygun** – Developer
- **Nuri Duldar** – Developer

## Ürün İsmi
LucentCV

## Ürün Açıklaması
LucentCV, bir kullanıcının CV metnini ve başvurmak istediği iş ilanının metnini analiz ederek,
ikisi arasındaki uyumu değerlendiren bir yapay zeka uygulamasıdır. Tek bir prompt'a değil,
**birbirini besleyen 5 ayrı AI agent'ına** dayanır:

1. **CV Analyzer Agent** — CV'deki beceri, deneyim ve eğitim bilgilerini yapılandırılmış
   şekilde çıkarır.
2. **Job Analyzer Agent** — İlan metnindeki gereksinimleri, aranan anahtar kelimeleri ve
   sorumlulukları çıkarır.
3. **Matcher Agent** — İlk iki agent'ın çıktısını karşılaştırarak bir uyum skoru, eksik
   kalan noktaları ve CV'yi güçlendirmek için somut öneriler üretir.
4. **Interview Generator Agent** — CV analizi, ilan analizi ve uyum değerlendirmesine göre
   adaya özel 5 mülakat sorusu üretir (güçlü noktalar, eksik beceriler, senaryo ve
   deneyim soruları karışık şekilde).
5. **Interview Evaluator Agent** — Kullanıcının mülakat sorularına verdiği cevapları
   değerlendirir; soru bazlı puan, genel skor, güçlü yönler ve geliştirilmesi gereken
   alanlar üretir.

Uygulama ayrıca basit bir **hafıza (memory) katmanı** içerir: kullanıcının geçmişte yaptığı
analizler yerel bir JSON dosyasında saklanır ve tekrar görüntülenebilir, böylece zaman
içindeki gelişim takip edilebilir.

## Ürün Özellikleri
- CV ve ilan metni girişi
- 5 agent'lı orkestrasyon (CV Analyzer → Job Analyzer → Matcher → Interview Generator → Interview Evaluator)
- Uyum skoru (0-100), eksik beceri/anahtar kelime listesi, somut iyileştirme önerileri
- **Akıllı Mülakat Simülasyonu**: CV ve ilana özel üretilen 5 mülakat sorusu, kullanıcının cevaplarının AI tarafından değerlendirilmesi (soru bazlı puan + genel geri bildirim)
- Geçmiş analizleri saklayan Supabase tabanlı bulut veritabanı
- Premium SaaS standartlarında, modern arayüz ve kullanıcı deneyimi

## Hedef Kitle
- Aktif iş başvurusu yapan üniversite mezunları ve yeni başlayanlar
- ATS (Applicant Tracking System) uyumlu CV hazırlamak isteyen adaylar
- Kariyer değişikliği yapan, CV'sini farklı sektörlere uyarlaması gereken kişiler

## Product Backlog
Sprint bazlı backlog için `sprints/` klasörüne bakınız.


# Sprint 1

## Sprint 1 Product Backlog

| # | User Story | Öncelik | Durum |
|---|---|:---:|:---:|
| 1 | Kullanıcı olarak CV metnimi ve iş ilanını sisteme girebilmeliyim. | Yüksek | ✅ Tamamlandı |
| 2 | Kullanıcı olarak CV analiz sonuçlarını görüntüleyebilmeliyim. | Yüksek | ✅ Tamamlandı |
| 3 | Kullanıcı olarak iş ilanı analizini görüntüleyebilmeliyim. | Yüksek | ✅ Tamamlandı |
| 4 | Kullanıcı olarak CV ve ilan arasındaki uyum skorunu ve önerileri görebilmeliyim. | Yüksek | ✅ Tamamlandı |
| 5 | Kullanıcı olarak CV ve ilana özel AI mülakat soruları oluşturabilmeliyim. | Yüksek | ✅ Tamamlandı |
| 6 | Kullanıcı olarak mülakat cevaplarımın AI tarafından değerlendirilmesini alabilmeliyim. | Yüksek | ✅ Tamamlandı |
| 7 | Kullanıcı olarak analiz geçmişimi görüntüleyebilmeliyim. | Orta | ✅ Tamamlandı |
| 8 | Kullanıcı olarak CV dosyamı PDF/DOCX formatında yükleyebilmeliyim. | Orta | ✅ Tamamlandı |
| 9 | Kullanıcı olarak analiz geçmişimin Supabase üzerinde saklanmasını istiyorum. | Orta | ✅ Tamamlandı |
| 10 | Kullanıcı olarak analiz sonuçlarını PDF veya Markdown olarak dışa aktarabilmeliyim. | Düşük | ⏳ Sprint 2 |
| 11 | Kullanıcı olarak Google hesabımla giriş yapabilmeliyim. | Orta | ⏳ Sprint 2 |
| 12 | Modern React tabanlı kullanıcı arayüzüne geçilmelidir. | Yüksek | ⏳ Sprint 2 |
| 13 | Uygulamanın production ortamına deploy edilmesi. | Orta | ⏳ Sprint 3 |

---

## Backlog Düzeni ve Story Seçimleri

Sprint 1 backlog'u hazırlanırken öncelik, kullanıcıya çalışabilir bir Minimum Viable Product (MVP) sunacak temel fonksiyonlara verilmiştir. Kullanıcı hikâyeleri öncelik seviyelerine göre sıralanmış, geliştirilebilir alt görevlere (task) ayrılmış ve ekip üyeleri arasında paylaştırılmıştır.

Sprint boyunca çoklu AI Agent mimarisi, Google Gemini entegrasyonu, Supabase veri yönetimi, CV analiz sistemi ve Akıllı Mülakat modülü başarıyla tamamlanmıştır.

Dışa aktarma (Export), Google Authentication ve modern React tabanlı frontend mimarisine geçiş gibi geliştirmeler ise Sprint 2 kapsamına aktarılmıştır.

---

## Daily Scrum
 
Ekip üyelerimizin profesyonel çalışma takvimlerinin yoğunluğu ve son dönemde özel
hayatlarında gelişen durumların sebebiyet verdiği meşguliyetler nedeniyle, gün
içerisinde herkesin katılabileceği ortak bir zaman dilimi oluşturmak mümkün
olmamıştır. Süreci aksatmamak, birbirimize destek olmak ve ilerlememizi
şeffaf bir şekilde sürdürebilmek adına iletişimin Slack üzerinden asenkron
olarak yürütülmesine karar verilmiştir.
 
Projenin genel gidişatı, görev dağılımı ve anlık ilerleme durumu Slack grup
sohbetimizde paylaşılan mesajlar üzerinden yürütülmüştür. İlgili iletişim süreci
ekteki bağlantıda sunulmuştur: [iletişim sürecinden kesitler](https://imgur.com/a/R4R2gFU)
 
### Toplantı Özeti
 
#### Genel Durum ve Proje Birleştirme
- Ekip içi iletişim kopukluğu nedeniyle başlangıçta Burak ve Büşra, diğer üyeler tarafından katılım sağlanmayacağını varsayarak projelerine bağımsız olarak başlamıştır.
- İletişim problemlerinin çözülmesi sonucu mevcut projelerden biri üzerinden
  ortak ilerleme kararı alınarak ekip içi görev dağılımları tekrardan
  oluşturulmuş ve tüm ekip üyelerinin görev dağılımları yapılarak aktif katılımları sağlanmıştır.
  
#### Görev Dağılımı (Sprint 1)
- **Asil Doğukan Samay:** Backlog Dağıtma Mantığı (Sprint Planning, User
  Story'ler, Story Point'ler, Backlog açıklaması ve GitHub Project linki)
- **Burak Baygün:** Daily Scrum sürecinin belgelenmesi
- **Büşra Demir:** Sprint Retrospective, Ürün Durumu ve Sprint Review
  aşamalarının hazırlanması
- **Nuri Duldar:** Sprint Board'un Miro kullanılarak hazırlanması

### Sprint 2 Vizyonu
 
- **Veritabanı:** Veriler yerel JSON yerine Supabase'e taşınacak. Ortam
  değişkeni tanımlı değilse sistem otomatik olarak `local_db.json` ile
  çalışmaya devam edecek (local fallback).
- **Model Çıktı Kararlılığı:** Gemini'nin geçersiz JSON döndürme sorununu
  çözmek için `google-genai` SDK'sının Pydantic şema desteği entegre edilecek.
- **Frontend:** Next.js, React, Tailwind ve TypeScript ile modern mimariye
  geçilecek.
- **Kullanıcı Deneyimi:**
  - Sürükle-bırak dosya yükleme + PDF/DOCX'ten otomatik metin çıkarma (parser)
  - Analiz sonuçlarını PDF/Markdown olarak dışa aktarma
  - Uyum skorunu dairesel grafik ve ilerleme barlarıyla gösteren dashboard
  - Google hesabıyla giriş (kimlik doğrulama)
---

## Sprint Board Update

> Bu bölüme Sprint Board (Miro) ekran görüntüleri eklenecektir.

---

## Ürün Durumu

### Ana Sayfa

<p align="center">
  <img src="images/home.png" width="900">
</p>

### CV - İş İlanı Analizi

<p align="center">
  <img src="images/analysis.png" width="900">
</p>

### Akıllı Mülakat Simülasyonu

<p align="center">
  <img src="images/interview.png" width="900">
</p>

### Geçmiş Analizler

<p align="center">
  <img src="images/history.png" width="900">
</p>

---

## Sprint Review

Sprint 1 sonunda LucentCV'nin çalışabilir **Minimum Viable Product (MVP)** sürümü başarıyla tamamlanmıştır.

Bu sprint kapsamında kullanıcıların CV ve iş ilanı metinlerini analiz edebildiği, çoklu AI Agent mimarisi ile uyum skorunu görüntüleyebildiği, kişiselleştirilmiş mülakat soruları oluşturabildiği ve cevaplarını yapay zekâ tarafından değerlendirebildiği çalışan bir sistem ortaya çıkarılmıştır.

### Sprint Boyunca Tamamlanan Geliştirmeler

- Çoklu AI Agent mimarisi (CV Analyzer, Job Analyzer, Matcher, Interview Generator ve Interview Evaluator) geliştirildi.
- Google Gemini API entegrasyonu tamamlandı.
- Supabase entegrasyonu gerçekleştirilerek analiz geçmişi PostgreSQL veritabanında saklanmaya başlandı.
- PDF ve DOCX dosya yükleme desteği eklendi.
- Streamlit tabanlı arayüz yeniden düzenlenerek component tabanlı daha modüler bir yapı oluşturuldu.
- Services ve Database katmanları oluşturularak kod yapısı sadeleştirildi.
- AI destekli mülakat oluşturma ve değerlendirme sistemi geliştirildi.
- Uygulamanın temel kullanıcı akışı uçtan uca çalışır hale getirildi.

Sprint sonunda yapılan değerlendirmelerde mevcut MVP'nin proje hedeflerini karşıladığı görülmüş, ancak kullanıcı deneyimi, sürdürülebilirlik ve ölçeklenebilirlik açısından yeni bir mimariye geçilmesinin gerekli olduğuna karar verilmiştir.

### Sprint Review Katılımcıları

- Burak Baygün — Product Owner
- Büşra Demir — Scrum Master
- Asil Doğukan Samay — Developer
- Ece Toygun — Developer
- Nuri Duldar — Developer

---

## Sprint Retrospective

Sprint sonunda geliştirilen ürün ve teknik süreç ekip tarafından değerlendirilmiştir. Sprint 1 hedeflerinin büyük bölümü başarıyla tamamlanmış ve çalışan bir MVP ortaya çıkarılmıştır.

### Güçlü Yönler

- Çoklu AI Agent mimarisi başarıyla geliştirildi.
- Google Gemini API entegrasyonu tamamlandı.
- Supabase ile kalıcı veri yönetimine geçildi.
- PDF/DOCX yükleme desteği eklendi.
- AI destekli mülakat oluşturma ve değerlendirme sistemi geliştirildi.
- Services, Components ve Database katmanları oluşturularak proje daha modüler hale getirildi.
- MVP sürümü başarıyla tamamlandı.

### İyileştirilmesi Gereken Noktalar

- Streamlit mimarisinin uzun vadede kullanıcı deneyimi açısından sınırlı olduğu görüldü.
- Frontend ve backend'in aynı yapı içerisinde bulunması geliştirme süreçlerini zorlaştırmaktadır.
- Kod tabanının API tabanlı ve bağımsız servislerden oluşan modern bir mimariye dönüştürülmesi gerektiği değerlendirildi.
- Responsive tasarım ve modern UI/UX standartlarının uygulanmasına ihtiyaç olduğu belirlendi.
- Code Review, Pull Request ve test süreçlerinin daha sistematik yürütülmesine karar verildi.


# Sprint 2

> Sprint 2 dokümantasyonu sprint sonunda eklenecektir.

---

# Sprint 3

> Sprint 3 dokümantasyonu sprint sonunda eklenecektir.


## Kurulum
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="senin-api-keyin"
streamlit run app.py
```

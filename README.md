# LucentCV — Çok Adımlı AI Agent ile CV-İlan Uyum Analizi

## Takım İsmi
Takım 126

## Takım Rolleri

- **Product Owner & Developer:** Burak Baygün
- **Scrum Master & Developer:** Büşra Demir
- **Developer:** Asil Doğukan Samay, Ece Toygun, Nuri Duldar

Not: Sprint 1 kapsamındaki geliştirmeler (fikir, agent mimarisi, dosya yükleme, düzenlemeler) Burak ve Büşra tarafından yürütülmüştür. Diğer takım üyeleri resmi
olarak takımda yer almaktadır; ekip içi görev dağılımı ilerleyen sprintlerde
katılımlarına göre netleştirilecektir.
  

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

## Ekran Görüntüleri

<div align="center">
  <img src="images/home.png" alt="Home Page" width="800"/>
  <br/><br/>
  <img src="images/analysis.png" alt="Analysis Dashboard" width="800"/>
  <br/><br/>
  <img src="images/interview.png" alt="Smart Interview Simulation" width="800"/>
  <br/><br/>
  <img src="images/history.png" alt="History Dashboard" width="800"/>
</div>

## Hedef Kitle
- Aktif iş başvurusu yapan üniversite mezunları ve yeni başlayanlar
- ATS (Applicant Tracking System) uyumlu CV hazırlamak isteyen adaylar
- Kariyer değişikliği yapan, CV'sini farklı sektörlere uyarlaması gereken kişiler

## Product Backlog
Sprint bazlı backlog için `sprints/` klasörüne bakınız.

### Genel Backlog (yüksek seviye)
| # | User Story | Öncelik | Durum |
|---|---|---|---|
| 1 | Kullanıcı olarak CV metnimi ve ilan metnini bir arayüze yapıştırabilmeliyim | Yüksek | Sprint 1 |
| 2 | Kullanıcı olarak CV'mden çıkarılan becerileri görebilmeliyim | Yüksek | Sprint 1 |
| 3 | Kullanıcı olarak ilan gereksinimlerinin analizini görebilmeliyim | Yüksek | Sprint 1 |
| 4 | Kullanıcı olarak bir uyum skoru ve öneriler alabilmeliyim | Yüksek | Sprint 2 |
| 5 | Kullanıcı olarak geçmiş analizlerimi görebilmeliyim (hafıza) | Orta | Sprint 2 |
| 6 | Kullanıcı olarak CV-ilan analizime özel mülakat soruları alabilmeliyim | Yüksek | Sprint 1 |
| 7 | Kullanıcı olarak mülakat cevaplarım için AI geri bildirimi alabilmeliyim | Yüksek | Sprint 1 |
| 8 | Kullanıcı olarak sonuçları dışa aktarabilmeliyim (PDF/metin) | Düşük | Sprint 3 |
| 9 | Uygulama canlıya alınmalı (Streamlit Cloud) | Orta | Sprint 3 |
| 10 | Kullanıcı olarak CV'yi pdf/word dökümanı olarak yükleyebilmeliyim | Yüksek | Sprint 1 |

## Teknolojiler
- **Backend/Logic:** Python
- **AI:** Google Gemini API (`google-genai` SDK, `gemini-2.5-flash` modeli)
- **Frontend:** Streamlit
- **Hafıza:** Yerel JSON dosyası (MVP), ileride SQLite'a geçilebilir
- **Deploy (opsiyonel):** Streamlit Community Cloud

## Kurulum
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="senin-api-keyin"
streamlit run app.py
```

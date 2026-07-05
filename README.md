# UygunCV — Çok Adımlı AI Agent ile CV-İlan Uyum Analizi

## Takım İsmi
Solo Takım — Burak Baygün

## Takım Rolleri
Bu bootcamp döneminde takım arkadaşlarımla iletişim sağlanamadığı için (bkz. Slack #bootcamp-2026
kanalındaki bildirim), süreci tek başıma sürdürüyorum. Tüm Scrum rollerini kendim üstleniyorum:

- **Product Owner:** Burak Baygün
- **Scrum Master:** Burak Baygün
- **Developer:** Burak Baygün

## Ürün İsmi
UygunCV

## Ürün Açıklaması
UygunCV, bir kullanıcının CV metnini ve başvurmak istediği iş ilanının metnini analiz ederek,
ikisi arasındaki uyumu değerlendiren bir yapay zeka uygulamasıdır. Tek bir prompt'a değil,
**birbirini besleyen 3 ayrı AI agent'ına** dayanır:

1. **CV Analyzer Agent** — CV'deki beceri, deneyim ve eğitim bilgilerini yapılandırılmış
   şekilde çıkarır.
2. **Job Analyzer Agent** — İlan metnindeki gereksinimleri, aranan anahtar kelimeleri ve
   sorumlulukları çıkarır.
3. **Matcher Agent** — İlk iki agent'ın çıktısını karşılaştırarak bir uyum skoru, eksik
   kalan noktaları ve CV'yi güçlendirmek için somut öneriler üretir.

Uygulama ayrıca basit bir **hafıza (memory) katmanı** içerir: kullanıcının geçmişte yaptığı
analizler yerel bir JSON dosyasında saklanır ve tekrar görüntülenebilir, böylece zaman
içindeki gelişim takip edilebilir.

## Ürün Özellikleri
- CV ve ilan metni girişi (metin kutusu, dosya yükleme gerekmez — MVP için hızlı)
- 3 agent'lı orkestrasyon (CV Analyzer → Job Analyzer → Matcher)
- Uyum skoru (0-100), eksik beceri/anahtar kelime listesi, somut iyileştirme önerileri
- Geçmiş analizleri saklayan basit hafıza sistemi (JSON tabanlı)
- Streamlit tabanlı tek-sayfa arayüz (frontend + backend aynı dosyada, hızlı deploy)

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
| 6 | Kullanıcı olarak sonuçları dışa aktarabilmeliyim (PDF/metin) | Düşük | Sprint 3 |
| 7 | Uygulama canlıya alınmalı (Streamlit Cloud) | Orta | Sprint 3 |

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

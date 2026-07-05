# Sprint 1 — Sprint Review

**Tarih:** 5 Temmuz 2026

## Bu Sprint'te Tamamlananlar
- Ürün fikri netleştirildi: **UygunCV**, çok adımlı AI agent mimarisiyle CV-ilan
  uyum analizi yapan bir araç.
- 3 agent'lı bir orkestrasyon zinciri kuruldu:
  - CV Analyzer Agent
  - Job Analyzer Agent
  - Matcher Agent (ilk ikisinin çıktısını birleştirip skor/öneri üretir)
- Basit bir hafıza (memory) katmanı eklendi — kullanıcının geçmiş analizleri
  yerel JSON dosyasında saklanıyor.
- Streamlit tabanlı çalışan bir arayüz geliştirildi (CV/ilan girişi, sonuç
  gösterimi, geçmiş analizler sekmesi).
- README ve proje dokümantasyonu tamamlandı.

## Demo Notları
Uygulama yerel olarak `streamlit run app.py` ile çalıştırılabiliyor. Kullanıcı
CV ve ilan metnini girip "Analiz Et" butonuna bastığında, sırasıyla 3 agent
çalışıyor ve sonuç (uyum skoru, eksik/eşleşen beceriler, öneriler) ekranda
gösteriliyor.

## Sprint Hedefine Ulaşıldı mı?
Evet. Sprint 1 hedefi olan "temel proje iskeletinin kurulması" tamamlandı.

## Ürün Durumu (Ekran Görüntüsü Notu)
Ekran görüntüleri `sprints/sprint1/screenshots/` klasörüne eklenmiştir
(yerel çalıştırmadan alınan görüntüler).

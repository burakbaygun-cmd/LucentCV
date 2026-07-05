# Sprint 1 — Retrospective

## İyi Gidenler
- Elimde zaten hazır olan Gemini API deneyimi (önceki proje denemesinden) sayesinde
  agent prompt'larını hızlı yazabildim.
- 3 agent'lı mimariyi tek dosyada (`agents.py`) düzenli tutmak, kodun okunabilirliğini
  kolaylaştırdı.

## Zorlanılanlar
- Takım dağıldığı için proje fikrini ve tüm teknik kurulumu sıfırdan, tek başıma ve
  kısa sürede yeniden yapmak zorunda kaldım.
- Google'ın `google-generativeai` paketini deprecated ilan etmesi ve `gemini-1.5-flash`
  modelinin kaldırılmış olması beklenmedik bir teknik engel oluşturdu; `google-genai`
  paketine geçiş yapıp modeli güncellemek gerekti.

## Sonraki Sprint İçin Aksiyonlar
- Gerçek CV/ilan örnekleriyle daha kapsamlı test yapılacak.
- Hata durumları (Gemini'nin geçersiz JSON döndürmesi gibi) için daha sağlam
  hata yönetimi eklenecek.
- Zaman uygunsa uygulamanın Streamlit Community Cloud'a deploy edilmesi
  değerlendirilecek.

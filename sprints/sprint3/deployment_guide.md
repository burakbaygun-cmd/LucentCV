# Sprint 3 — LucentCV Deployment & Production Configuration Guide

**Hazırlayan:** Asil Doğukan Samay (Developer / DevOps)  
**Tarih:** Temmuz 2026  
**Proje:** LucentCV — AI Destekli Özgeçmiş & İlan Uyum Analiz SaaS Platformu

---

## 🚀 1. Genel Mimarisi ve Canlıya Alma Stratejisi

Sprint 3 kapsamında LucentCV projesi, modern SaaS standartlarına uygun şekilde ayrık (decoupled) iki ana bileşen olarak canlıya alınacak şekilde yapılandırılmıştır:

- **Frontend (Kullanıcı Arayüzü):** Next.js 15 App Router tabanlı yapı → **Vercel Platformu**
- **Backend (API & AI Orkestrasyonu):** FastAPI + Uvicorn tabanlı Python servisi → **Render.com / Railway Platformu**
- **Veritabanı & Authentication:** Supabase (PostgreSQL + Supabase Auth / Google OAuth)

---

## 📱 2. Frontend Deployment (Vercel)

Vercel, Next.js uygulamaları için resmi ve en yüksek performanslı barındırma platformudur.

### Adım Adım Vercel Dağıtımı:

1. **Vercel'e Giriş Yapın:** [Vercel Dashboard](https://vercel.com/dashboard) adresine girip GitHub hesabınızla giriş yapın.
2. **Yeni Proje Ekle:** **"Add New..."** → **"Project"** seçeneğine tıklayın.
3. **Repository Seçimi:** `burakbaygun-cmd/LucentCV` reposunu seçip **"Import"** butonuna basın.
4. **Root Directory Ayarı:**
   - Framework Preset: **Next.js**
   - Root Directory: **`frontend`** (Edit diyerek `frontend` klasörünü seçin).
5. **Environment Variables (Çevre Değişkenleri):**
   Aşağıdaki değişkenleri Vercel arayüzüne ekleyin:

   | Key | Açıklama | Örnek Değer |
   |---|---|---|
   | `NEXT_PUBLIC_SUPABASE_URL` | Supabase Proje URL adresi | `https://runvrifzcsjptzluyvqq.supabase.co` |
   | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase Anonim Anahtarı | `eyJhbGciOi...` |
   | `NEXT_PUBLIC_API_URL` | Canlı Backend API Adresi | `https://lucentcv-backend.onrender.com/api` |

6. **Deploy:** **"Deploy"** butonuna basın. Vercel otomatik olarak `npm run build` komutunu çalıştıracak ve canlı alan adını (Örn: `https://lucent-cv.vercel.app`) üretecektir.

---

## ⚡ 3. Backend Deployment (Render / Railway)

FastAPI backend servisi Docker veya doğrudan Python ortamlarda Render.com üzerinde kolayca dağıtılır.

### Option A: Render.com Üzerinden Dağıtım (Önerilen)

1. [Render.com Dashboard](https://dashboard.render.com/) adresine girin.
2. **"New +"** → **"Web Service"** butonuna tıklayın.
3. GitHub reponuzu (`LucentCV`) bağlayın.
4. Ayarları şu şekilde yapılandırın:
   - **Name:** `lucentcv-backend`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables (Çevre Değişkenleri):**

   | Key | Açıklama | Değer / Örnek |
   |---|---|---|
   | `GEMINI_API_KEY` | Google Gemini API Anahtarı | `AIzaSy...` |
   | `SUPABASE_URL` | Supabase Proje URL | `https://runvrifzcsjptzluyvqq.supabase.co` |
   | `SUPABASE_ANON_KEY` | Supabase Anon Key | `eyJhbGciOi...` |
   | `SUPABASE_SERVICE_ROLE_KEY` | Supabase Service Role Key | `eyJhbGciOi...` |
   | `ALLOWED_ORIGINS` | İzin Verilen Frontend Adresleri | `https://lucent-cv.vercel.app,http://localhost:3000` |

6. **Create Web Service:** Butona bastığınızda canlı backend adresi üretilecektir (Örn: `https://lucentcv-backend.onrender.com`).

---

## 🔐 4. Supabase Auth & Google OAuth Production Yapılandırması

Canlıya geçişte Supabase ve Google OAuth yönlendirmelerinin sorunsuz çalışması için yapılması gereken ayarlar:

### A. Supabase Dashboard Ayarları
1. [Supabase Dashboard](https://supabase.com/dashboard) adresine gidin.
2. **Authentication** → **URL Configuration** sekmesini açın.
3. **Site URL:** Canlı Vercel adresinizi girin: `https://lucent-cv.vercel.app`
4. **Redirect URLs:** Aşağıdaki URL'leri izin verilenler listesine ekleyin:
   - `https://lucent-cv.vercel.app/**`
   - `https://lucent-cv.vercel.app/dashboard`
   - `http://localhost:3000/**`

### B. Google Cloud Console Ayarları
1. [Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials) sayfasına gidin.
2. Oluşturduğunuz Web OAuth Client'ı seçin.
3. **Authorized JavaScript origins:**
   - `https://lucent-cv.vercel.app`
   - `http://localhost:3000`
4. **Authorized redirect URIs:**
   - `https://runvrifzcsjptzluyvqq.supabase.co/auth/v1/callback`

---

## 🛠️ 5. CORS ve Production Bağlantı Kontrolleri

- Backend `main.py` ve `config.py` içerisinde `ALLOWED_ORIGINS` dinamik olarak okunacak şekilde yapılandırılmıştır.
- Üretim ortamında `ALLOWED_ORIGINS="https://lucent-cv.vercel.app"` tanımı ile tarayıcı CORS engellemeleri tamamen ortadan kaldırılmıştır.
- PDF Export servisindeki Türkçe karakter encoding ve dynamic URL yönlendirmeleri canlı ortama hazır hale getirilmiştir.

---

## 📋 6. Asil - Deployment Kontrol Listesi (Checklist)

- [x] Backend CORS ayarları dinamik `ALLOWED_ORIGINS` ile güncellendi (`main.py` & `config.py`).
- [x] Backend deployment dosyaları eklendi (`Procfile`, `render.yaml`, `.env.example`).
- [x] Frontend deployment konfigürasyonu eklendi (`vercel.json`, `.env.example`).
- [x] Frontend üretim build'i (`npm run build`) 0 hata ile doğrulandı.
- [x] Supabase Auth ve Google OAuth canlı yönlendirme dokümantasyonu tamamlandı.
- [x] Vercel & Render adım adım yayınlama rehberi eklendi.

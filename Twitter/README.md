# Twitter Clone + Ad Hominem Moderation

Bu klasor, Twitter benzeri bir uygulamayi ve ad hominem moderasyon entegrasyonunu icerir.

## Proje Ozeti

Tum sistem iki ana domain uzerinden ilerler:

1. `Twitter/`
   - `twitter-clone-with-next-js-frontend` (Next.js 14 + TypeScript)
   - `twitter-clone-backend-django` (Django + DRF + Channels)
2. `Ad Hominem Detection/` (NLP/API tarafi)
   - Tweet metnini ad hominem acisindan degerlendirir
   - `POST /predict` endpoint'i ile skor/etiket doner

Not: Kod agacinda klasor ismi daha uzun bir adla gecebilir, ancak bu dokumanda AI tarafi `Ad Hominem Detection` olarak adlandirilmistir.

Ek altyapi:
- PostgreSQL
- Redis
- Kafka (Redpanda)
- Prometheus + Grafana

## Mevcut Ozellikler (Kodda Olanlar)

### Kimlik dogrulama ve kullanici
- Kayit olma (`/api/v1/auth/register/`)
- JWT token alma/yenileme (`/api/v1/auth/token/`, `/api/v1/auth/token/refresh/`)
- `me` endpoint'i ile profil goruntuleme/guncelleme
- Kullanici listeleme ve tekil kullanici sorgulama

### Sosyal ozellikler
- Tweet olusturma ve listeleme
- Reply (yorum) mantigi (`reply_to` alani)
- Repost/retweet modeli (`repost_of` ve retweet endpoint'leri)
- Like/unlike
- Follow/unfollow toggle
- Takipciler ve takip edilenler listesi
- Follow status sorgusu

### Mesajlasma
- Direkt mesaj API'leri
- WebSocket ile gercek zamanli mesajlasma (`/ws/messages/<user_id>/`)
- Mesajlasma izni: kullanici sadece takip ettiklerine mesaj atabilir

### Ad Hominem moderasyon pipeline
- Yeni tweet olusunca moderation event publish edilir
- Consumer event'i okuyup NLP endpoint'ine gonderir
- Sonuc tweet kaydina yazilir:
  - `is_ad_hominem`
  - `ad_hominem_score`
  - `ad_hominem_checked_at`
- Redis TTL ile tekrar isleme engeli (dedup)

### Operasyon ve gozlemlenebilirlik
- Health endpoint: `/api/v1/health/`
- OpenAPI schema + Swagger
- Prometheus metrik toplama
- Grafana dashboard

## Eksik Ozellikler (MISSING_FEATURES.md'den)

### Core social features
- Quote tweets
- Threaded tweet composer (multi-tweet threads)
- Drafts and scheduled posts
- Polls
- Bookmarks
- Lists
- Spaces (audio)
- Communities

### Discovery
- Search with filters
- Trends / topics
- Hashtag pages
- User recommendations

### Messaging and notifications
- Notification inbox and settings
- Push/email notifications

### Safety and moderation
- Report flow
- Block and mute
- Private accounts / follow requests
- Content moderation tools (admin side genisletme)

### Media
- Gelismis media upload/processing (video pipeline, thumbnail vb.)
- Link previews
- Media CDN / object storage entegrasyonu

### Account and settings
- Two-factor auth
- Device/session management
- Privacy controls
- Deactivation and data export

### Platform
- Rate limiting / abuse protection
- Arka plan fan-out stratejileri
- Gelismis analytics (user/post davranis analizi)

## Bilinen Teknik Aciklar / Iyilestirme Alanlari

- Frontend'de bazi legacy endpointler hala eski Strapi URL'lerine isaret ediyor (`localhost:1337`).
  - Ornek: `app/api/comments/getTweetsComments/route.ts`
  - Bunlarin Django endpointleriyle tamamen hizalanmasi gerekiyor.
- Frontend README su an bos; bu ana README dokumantasyon yukunu ustleniyor.
- E2E/load test scriptleri var ama CI pipeline ile otomatik calisma akisi dokumante degil.

## Genel Isleyis

### Kullanici akis senaryosu
1. Kullanici frontend uzerinden kayit olur veya giris yapar.
2. Frontend, backend'den JWT alir ve API cagrilarinda kullanir.
3. Kullanici tweet atar, begenir, retweet eder, takip eder.
4. Mesajlasma ekraninda uygun kullanici secilirse WebSocket baglantisi acilir.

### Moderasyon senaryosu
1. Tweet olusur (`tweets` create).
2. Moderation event Kafka topic'ine publish edilir.
3. Consumer event'i alip NLP API'ye gonderir (`/predict`).
4. Donen sonuc Tweet kaydina yazilir.
5. Frontend tweet kartinda ad hominem bilgisi gorunur.

## Lokal Calistirma (Docker ile Onerilen)

`twitter-clone-backend-django` klasorunde:

```bash
docker compose -f docker-compose.backend.yml up --build
```

Acilan temel servisler:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Swagger: `http://localhost:8000/api/v1/docs/`
- NLP API: `http://localhost:9000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001` (admin/admin)

Kapatma:

```bash
docker compose -f docker-compose.backend.yml down
```

## Ortam Degiskenleri

Backend icin `.env.example` dosyasini baz alin. Kritik degiskenler:
- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `KAFKA_ENABLED`
- `KAFKA_BOOTSTRAP_SERVERS`
- `AD_HOMINEM_MODEL_ENDPOINT`

Frontend icin onemli degiskenler:
- `NEXT_PUBLIC_API_BASE_URL`
- `API_BASE_URL_INTERNAL`
- `NEXT_PUBLIC_WS_BASE_URL`

## Testler

Backend icin:

```bash
python manage.py test
```

Ayrica `scripts/` altinda:
- `e2e_follow_ws_test.py`
- `multi_user_load_test.py`

## GitHub'a Yukleme Rehberi (Tum Proje)

Bu README, tum sistemi tek bir repo olarak yukleme senaryosuna gore guncellendi.

### Onerilen monorepo yapisi

Repo kokunde su iki alanin birlikte olmasi beklenir:
- `Twitter/`
- `Ad Hominem Detection/` (veya mevcut AI klasor adin)

### 1) Workspace kokunden tum projeyi push et

Onemli: Eger `Ad Hominem Detection` klasorunun icinde ayri bir `.git` varsa, iki secenekten birini kullan:
- Secenek A: Tek repo istiyorsan icteki `.git` klasorunu kaldirip sonra `git add .` yap.
- Secenek B: Ic repoyu submodule olarak bagla.

```bash
cd "c:\Users\PC\Desktop\Twitter and Ad Hominem Detection"
git init
git add .
git commit -m "Initial commit: Twitter clone + Ad Hominem Detection system"
git branch -M main
git remote add origin https://github.com/<kullanici_adi>/<tum-proje-repo>.git
git push -u origin main
```

### 2) `origin` zaten varsa

```bash
git remote set-url origin https://github.com/<kullanici_adi>/<tum-proje-repo>.git
git push -u origin main
```

### 3) Sadece Twitter repo'su ayri kalacaksa

Bu klasoru (`Twitter/`) ayri repo olarak tutman da mumkun. O durumda bu README'deki mimari aciklamasi degismez, sadece AI repo linkini referans olarak eklersin.

## Kisa Yol Haritasi (Oneri)

1. Legacy Strapi endpointlerini tamamen Django endpointlerine tasima
2. Notification sistemi ve bloklama/raporlama ozellikleri
3. Rate limiting + abuse protection
4. CI pipeline'da test ve lint otomasyonu
5. Medya saklama icin object storage entegrasyonu (S3/MinIO)

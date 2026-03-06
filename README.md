# Twitter + Ad Hominem Detection (System Repository)

Bu depo, Twitter clone uygulamasi ile Ad Hominem Detection model/API tarafinin birlikte nasil calistigini anlatan genel sistem dokumantasyonudur.

## Amac

Bu sistemin hedefi:
- Twitter benzeri sosyal medya akisinda icerik olusturma, etkilesim ve mesajlasma sunmak
- Tweetleri ad hominem acisindan otomatik olarak degerlendirmek
- Moderasyon pipeline'i ile NLP model sonucunu uygulamaya geri yazmak

## Bilesenler

### 1) Twitter Uygulamasi
- Repo: `https://github.com/yigitbalcioglu/Twitter-Clone.git`
- Icerik:
  - Next.js frontend
  - Django REST + Channels backend
  - Kafka/Redis tabanli moderasyon akisi
  - Prometheus + Grafana izleme

### 2) Ad Hominem Detection
- Repo: `https://github.com/yigitbalcioglu/Ad-Hominem-Detection-Turkish`
- Icerik:
  - Turkish ad hominem tespit modelleri
  - Egitim ve degerlendirme kodlari
  - Hafif API servisi (`/predict`) ile backend entegrasyonu

## Yuksek Seviye Mimari

1. Kullanici frontend uzerinden tweet olusturur.
2. Backend tweet kaydini olusturur ve moderasyon event'i yayinlar.
3. Consumer event'i alip NLP API'ye metni gonderir.
4. NLP API ad hominem tahmini doner.
5. Backend sonucu tweet alanlarina yazar (`is_ad_hominem`, `ad_hominem_score`).
6. Frontend bu sonucu tweet kartlarinda gosterir.

## Lokal Calistirma (Tum Sistem)

### On kosullar
- Docker Desktop
- Docker Compose
- Portlar: `3000`, `8000`, `9000`, `9090`, `3001`, `5432`, `6379`, `9092`

### Calistirma

```bash
cd "Twitter/twitter-clone-backend-django"
docker compose -f docker-compose.backend.yml up --build
```

### Servisler
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Swagger: `http://localhost:8000/api/v1/docs/`
- NLP API: `http://localhost:9000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`

## Bilinen Eksikler (Ozet)

- Quote tweet, bookmarks, polls, trends, hashtag sayfalari
- Gelismis notification tercihleri
- Block/mute/report akislarinin genisletilmesi
- Bazi frontend legacy endpointlerinin tam temizlenmesi

Detayli liste: `Twitter/MISSING_FEATURES.md`

## Dizin Yapisi

```text
Twitter and Ad Hominem Detection/
  README.md
  Twitter/
    README.md
    twitter-clone-backend-django/
    twitter-clone-with-next-js-frontend/
  Ad Hominem Detection/
    README.md
    api_service.py
    src/
```

## GitHub Yayini

Bu depo, iki calisan alt projeyi bir araya getiren sistem dokumantasyonu olarak kullanilir.

Onerilen yaklasim:
- Alt projeler kendi repolarinda gelistirilmeye devam eder.
- Bu depo, sistem seviye dokumantasyon ve entegrasyon giris noktasi olarak kalir.

Eger bu kok klasoru de ayri bir GitHub reposuna yuklemek istersen:

```bash
cd "c:\Users\PC\Desktop\Twitter and Ad Hominem Detection"
git init
git add README.md
git commit -m "docs: add system-level README"
git branch -M main
git remote add origin https://github.com/<kullanici>/<repo>.git
git push -u origin main
```

Not:
- `Twitter/` ve `Ad Hominem Detection/` klasorleri kendi `.git` gecmislerine sahip oldugu icin bu kok depoda tam kaynak kod yerine sistem README tutmak en temiz secenektir.

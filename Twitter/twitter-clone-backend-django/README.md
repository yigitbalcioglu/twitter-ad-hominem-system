# Twitter Clone Backend (Django)

This service replaces the Strapi backend with a Django REST API.

## Quick start (dev)
1. Copy .env.example to .env and update values.
2. Build and run with Docker (see docker-compose.backend.yml).
3. Run migrations and create a superuser.

### One-command full stack (frontend + backend + db + pipeline + monitoring)

Bu komutla tüm servisler birlikte ayağa kalkar:

```bash
docker compose -f docker-compose.backend.yml up --build
```

Ayağa kalkan servisler:
- `web` (Django API)
- `frontend` (Next.js)
- `moderation-consumer` (Kafka consumer + DB update)
- `moderation-scheduler` (periyodik publish)
- `db` (PostgreSQL)
- `redis`
- `kafka`
- `nlp-api` (Ad Hominem `/predict`)

### Monitoring (Prometheus + Grafana)

Monitoring servisleri de aynı compose içinde çalışır:

- `prometheus` (http://localhost:9090)
- `grafana` (http://localhost:3001)
- `redis-exporter` (http://localhost:9121/metrics)
- `postgres-exporter` (http://localhost:9187/metrics)
- `kafka-exporter` (http://localhost:9308/metrics)

Grafana giriş bilgileri (default):

- kullanıcı: `admin`
- şifre: `admin`

Grafana açıldığında `Twitter Moderation Overview` dashboard'u otomatik yüklenir.

Kapatmak için:

```bash
docker compose -f docker-compose.backend.yml down
```

### Health/çalışma durumu nasıl görülür?

Servisler kalktıktan sonra sağlık durumlarını anlık görmek için:

```bash
docker compose -f docker-compose.backend.yml ps
```

`STATUS` sütununda `healthy` görmelisin (özellikle `frontend`, `web`, `db`, `nlp-api`).

## Architecture
- Django REST Framework for APIs
- JWT auth (SimpleJWT)
- PostgreSQL for persistence
- Redis (optional) for async/queues later
- Service layer for business logic

## Ad Hominem Moderation Pipeline

Bu backend, tweetler için Kafka + Redis tabanlı bir moderasyon pipeline'ı içerir.

- Tweet oluşturulunca `tweet-moderation-events` Kafka topic'ine event yayınlanır.
- Consumer komutu event'i alır, metni ad hominem açısından değerlendirir.
- Sonuçlar `Tweet` modeline yazılır:
	- `is_ad_hominem`
	- `ad_hominem_score`
	- `ad_hominem_checked_at`
- Redis, aynı tweet'in tekrar işlenmesini TTL ile engeller.

### Çalıştırma

1. Migration:

```bash
python manage.py migrate
```

2. Consumer başlat:

```bash
python manage.py consume_moderation_events
```

3. Eski/işaretlenmemiş tweetleri toplu publish et:

```bash
python manage.py publish_unchecked_tweets --limit 500
```

4. Periyodik publish (belirli aralıklarla):

```bash
python manage.py run_moderation_scheduler --interval-seconds 60 --batch-size 200
```

### NLP Model Entegrasyonu

`AD_HOMINEM_MODEL_ENDPOINT` tanımlarsan backend bu endpoint'e POST atar:

```json
{"text": "tweet metni"}
```

Beklenen cevap:

```json
{"is_ad_hominem": true, "confidence": 0.91}
```

Endpoint tanımlı değilse sistem geçici olarak heuristic fallback kullanır.


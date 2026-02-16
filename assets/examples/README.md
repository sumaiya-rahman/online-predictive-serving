# API curl examples

Run the API first (`make run`), then use these from the repo root or set `BASE=http://localhost:8000`.

## GET /health

```bash
curl -s http://localhost:8000/health
```

## GET /get

```bash
curl -s http://localhost:8000/get
```

## POST /post (echo + timestamp)

```bash
curl -s -X POST http://localhost:8000/post \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'
```

## POST /predict (random forest, 4 features)

```bash
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

## GET /metrics (Prometheus)

```bash
curl -s http://localhost:8000/metrics
```

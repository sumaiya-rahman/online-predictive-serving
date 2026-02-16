#!/usr/bin/env bash
# POST /predict - random forest (4 features)
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

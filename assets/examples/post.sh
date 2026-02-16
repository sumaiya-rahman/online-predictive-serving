#!/usr/bin/env bash
# POST /post - echo body + timestamp
curl -s -X POST http://localhost:8000/post \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'

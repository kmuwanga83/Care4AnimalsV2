#!/bin/bash
# Test the Analytics POST endpoint

echo "📡 Sending test payload to Analytics..."

curl -i -X 'POST' \
  'http://localhost:8000/analytics/' \
  -H 'Content-Type: application/json' \
  -d '{
  "farmer_id": 99,
  "event_type": "workflow_test",
  "metadata_json": "{\"status\": \"automated_test\", \"tool\": \"bash\"}"
}'

echo -e "\n\n✅ Test complete."
#!/bin/bash
# API Testing Script for nova.apilageai.lk

BASE_URL="https://nova.apilageai.lk"
AUTH_CODE="AuthWiThDineth@apilageai"
API_KEY="Dineth@30133637HElovEdLithumi"

echo "🧪 Testing Apilage AI Video API"
echo "================================="
echo ""

# Test 1: Health Check (No Auth Required)
echo "1️⃣ Testing Health Check (Public)..."
curl -s "${BASE_URL}/health" | python3 -m json.tool
echo ""
echo ""

# Test 2: API Generate WITHOUT Auth (Should Fail)
echo "2️⃣ Testing API without authentication (should fail with 401)..."
curl -s -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test without auth"}' | python3 -m json.tool
echo ""
echo ""

# Test 3: API Generate WITH Auth (Should Succeed)
echo "3️⃣ Testing API with authentication (should succeed)..."
RESPONSE=$(curl -s -X POST "${BASE_URL}/api/generate" \
  -H "Content-Type: application/json" \
  -H "X-Auth-Code: ${AUTH_CODE}" \
  -H "X-API-Key: ${API_KEY}" \
  -d '{"topic": "Explain the concept of gravity"}')

echo "$RESPONSE" | python3 -m json.tool
JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('job_id', ''))" 2>/dev/null)
echo ""
echo ""

# Test 4: Check Status (If job was created)
if [ ! -z "$JOB_ID" ]; then
    echo "4️⃣ Testing Status Check with Job ID: $JOB_ID"
    curl -s "${BASE_URL}/api/status/${JOB_ID}" \
      -H "X-Auth-Code: ${AUTH_CODE}" \
      -H "X-API-Key: ${API_KEY}" | python3 -m json.tool
    echo ""
    echo ""
fi

# Test 5: Queue Status
echo "5️⃣ Testing Queue Status..."
curl -s "${BASE_URL}/api/queue" \
  -H "X-Auth-Code: ${AUTH_CODE}" \
  -H "X-API-Key: ${API_KEY}" | python3 -m json.tool
echo ""
echo ""

# Test 6: List Videos
echo "6️⃣ Testing List Videos..."
curl -s "${BASE_URL}/api/videos?limit=3" \
  -H "X-Auth-Code: ${AUTH_CODE}" \
  -H "X-API-Key: ${API_KEY}" | python3 -m json.tool
echo ""
echo ""

echo "✅ Testing Complete!"
echo ""
echo "📝 Notes:"
echo "  - Health check should work without auth"
echo "  - API endpoints should require authentication"
echo "  - Web UI at ${BASE_URL} should work without auth"
echo ""

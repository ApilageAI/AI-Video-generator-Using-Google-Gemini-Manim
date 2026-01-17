#!/bin/bash
# Quick test script to verify the Flask server is working with the fixes

echo "======================================================================"
echo "Testing Video Generation with Fixed Code"
echo "======================================================================"

# Check if Flask is running
PID=$(pgrep -f "python.*app.py")
if [ -z "$PID" ]; then
    echo "❌ Flask server is not running"
    echo "   Start it with: python3 app.py"
    exit 1
fi

echo "✓ Flask server is running (PID: $PID)"
echo ""

# Check what port it's on
PORT=$(lsof -p $PID -a -i TCP -sTCP:LISTEN | grep -o ':\d\+' | head -1 | tr -d ':')
if [ -z "$PORT" ]; then
    PORT="5002"  # Default from app.py
fi

echo "Testing on port: $PORT"
echo ""

# Test the generate endpoint
echo "Sending test request: 'Explain me past tenses'"
echo "This will take 30-60 seconds..."
echo ""

RESPONSE=$(curl -s -X POST "http://localhost:$PORT/generate" \
  -H "Content-Type: application/json" \
  -d '{"text":"Explain me past tenses"}' \
  --max-time 90 \
  2>&1)

# Check the response
if echo "$RESPONSE" | grep -q "video_id"; then
    echo "✅ SUCCESS! Video generation completed"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
elif echo "$RESPONSE" | grep -q "error"; then
    echo "❌ Error response received:"
    echo "$RESPONSE"
    exit 1
elif echo "$RESPONSE" | grep -q "timeout"; then
    echo "⏱️  Request timed out (may still be processing)"
    echo "Check server logs for progress"
else
    echo "❓ Unexpected response:"
    echo "$RESPONSE"
fi

echo ""
echo "======================================================================"
echo "To monitor server logs in real-time:"
echo "  tail -f <log_file_if_any> or check the terminal running app.py"
echo "======================================================================"

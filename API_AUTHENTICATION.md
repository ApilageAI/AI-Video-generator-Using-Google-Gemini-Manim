# API Authentication Guide

## ⚠️ IMPORTANT SECURITY NOTICE

Your API is now **PROTECTED** and requires authentication. Only requests with valid credentials will be processed.

## Authentication Setup

### Credentials (Store in .env file - NEVER share publicly)

```
AUTH_CODE=AuthWiThDineth@apilageai
API_KEY=Dineth@30133637HElovEdLithumi
```

These are already configured in your `.env` file.

---

## How to Authenticate API Requests

All API endpoints require **two headers**:
- `X-Auth-Code`: Your authorization code
- `X-API-Key`: Your API key

### Example: cURL Command

```bash
curl -X POST http://localhost:5002/api/generate \
  -H "Content-Type: application/json" \
  -H "X-Auth-Code: AuthWiThDineth@apilageai" \
  -H "X-API-Key: Dineth@30133637HElovEdLithumi" \
  -d '{"topic": "Explain photosynthesis", "level": "basic"}'
```

### Example: Python Requests

```python
import requests

url = "http://localhost:5002/api/generate"

headers = {
    "X-Auth-Code": "AuthWiThDineth@apilageai",
    "X-API-Key": "Dineth@30133637HElovEdLithumi",
    "Content-Type": "application/json"
}

data = {
    "topic": "Explain photosynthesis",
    "level": "basic"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Example: JavaScript/Fetch

```javascript
const headers = {
    "X-Auth-Code": "AuthWiThDineth@apilageai",
    "X-API-Key": "Dineth@30133637HElovEdLithumi",
    "Content-Type": "application/json"
};

const data = {
    "topic": "Explain photosynthesis",
    "level": "basic"
};

fetch("http://localhost:5002/api/generate", {
    method: "POST",
    headers: headers,
    body: JSON.stringify(data)
})
.then(res => res.json())
.then(data => console.log(data));
```

### Example: Axios (JavaScript)

```javascript
const axios = require("axios");

const headers = {
    "X-Auth-Code": "AuthWiThDineth@apilageai",
    "X-API-Key": "Dineth@30133637HElovEdLithumi",
    "Content-Type": "application/json"
};

axios.post("http://localhost:5002/api/generate", {
    topic: "Explain photosynthesis",
    level: "basic"
}, { headers })
.then(res => console.log(res.data));
```

---

## Protected API Endpoints

All these endpoints now require authentication:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate` | Generate a new video |
| GET | `/api/status/{job_id}` | Check job status |
| GET | `/api/video/{job_id}` | Get video details |
| GET | `/api/queue` | Get queue status |
| GET | `/api/videos` | List all videos |
| POST | `/api/cancel/{job_id}` | Cancel a pending job |
| GET | `/api/uploads` | List all uploads |

---

## Error Responses

### Missing or Invalid Credentials

**Status Code:** `401 Unauthorized`

```json
{
    "success": false,
    "error": "Unauthorized: Invalid or missing API credentials",
    "required_headers": {
        "X-Auth-Code": "Your authorization code",
        "X-API-Key": "Your API key"
    }
}
```

---

## Public Endpoints (No Auth Required)

The following endpoints can be accessed without authentication:

| Endpoint | Description |
|----------|-------------|
| `/` | Main web interface |
| `/api-docs` | API documentation |
| `/api/auth-info` | Authentication information and examples |

---

## Security Best Practices

✅ **DO:**
- Store credentials in `.env` file (already done)
- Never commit `.env` to public repositories
- Use HTTPS in production
- Rotate credentials periodically
- Use strong, unique credentials

❌ **DON'T:**
- Share your AUTH_CODE or API_KEY publicly
- Hardcode credentials in your source code
- Commit `.env` file to git
- Use simple/guessable credentials
- Expose credentials in logs or error messages

---

## Testing Authentication

Visit this public endpoint to see how to authenticate:

```
GET http://localhost:5002/api/auth-info
```

This will return detailed information about authentication requirements and examples.

---

## Need Help?

If you get "Unauthorized" error:
1. Verify you're sending both headers: `X-Auth-Code` and `X-API-Key`
2. Check that the values match exactly what's in your `.env` file
3. Ensure headers are properly formatted (no extra spaces)
4. Verify your request is to a `/api/` endpoint (web UI doesn't need auth)

---

**Your API is now secure! Only you can use it.** 🔒

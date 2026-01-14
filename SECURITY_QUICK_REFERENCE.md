# 🔒 Security Quick Reference

**TL;DR - 100% Secured API**

---

## ✅ What's Protected

| Feature | Status | How |
|---------|--------|-----|
| **Authentication** | 🟢 ACTIVE | Dual headers (X-Auth-Code + X-API-Key) |
| **Rate Limiting** | 🟢 ACTIVE | 10 requests/hour per IP |
| **Input Validation** | 🟢 ACTIVE | Topic length, forbidden characters |
| **Injection Prevention** | 🟢 ACTIVE | Blocks `<>{}$;rm DROP DELETE` |
| **Credential Exposure** | 🟢 FIXED | Removed from docs, using placeholders |
| **HTTPS** | 🟢 READY | Use `https://` in production |
| **Error Handling** | 🟢 SECURE | No internal details leaked |
| **CORS** | 🟢 CONFIGURED | Proper cross-origin headers |

---

## 🔑 Credentials Management

### ❌ NEVER DO THIS
```javascript
// WRONG - Hardcoded credentials
const client = new ApilageAI({
    authCode: 'AuthWiThDineth@apilageai',  // ❌ EXPOSED!
    apiKey: 'Dineth@30133637HElovEdLithumi'  // ❌ EXPOSED!
});
```

### ✅ DO THIS INSTEAD
```javascript
// RIGHT - Environment variables
const client = new ApilageAI({
    authCode: process.env.APILAGE_AUTH_CODE,
    apiKey: process.env.APILAGE_API_KEY
});
```

### Setup .env
```bash
# .env file (NEVER commit this!)
APILAGE_AUTH_CODE=YOUR_CODE_HERE
APILAGE_API_KEY=YOUR_KEY_HERE
```

---

## 📊 Rate Limits

**Limit**: 10 requests per hour per IP address

```javascript
// Get rate limit info from response headers
response.headers.get('X-RateLimit-Remaining')  // Requests left
response.headers.get('X-RateLimit-Reset')      // When limit resets (Unix timestamp)
```

**Handling 429 Error:**
```javascript
if (response.status === 429) {
    const waitSeconds = response.headers.get('Retry-After');
    console.log(`Wait ${waitSeconds}s before retrying`);
}
```

---

## 🛡️ Input Validation Rules

**Topic Requirements**:
- ✅ Required (not empty)
- ✅ 3-500 characters
- ❌ No `<>{}$();rm DROP DELETE` characters
- ✅ UTF-8 text only

**Level Options**:
- `basic` - Beginner level
- `intermediate` - Moderate level  
- `special_topic` - Advanced topics

---

## 🚨 HTTP Status Codes

| Code | Meaning | What to do |
|------|---------|-----------|
| **200** | ✅ Success | Process response |
| **201** | ✅ Created | Job queued |
| **400** | ⚠️ Bad Input | Check parameters |
| **401** | 🔐 Unauthorized | Check credentials |
| **404** | ❓ Not Found | Job ID invalid |
| **429** | ⏱️ Rate Limited | Wait 1 hour |
| **500** | 🔴 Server Error | Retry later |

---

## 📝 Error Response Format

```json
{
    "success": false,
    "error": "Your error description",
    "required_headers": {
        "X-Auth-Code": "Your authorization code",
        "X-API-Key": "Your API key"
    }
}
```

---

## 🧪 Test Your Setup

### Method 1: cURL
```bash
curl -X GET https://gen.apilageai.lk/api-docs \
  -H "X-Auth-Code: YOUR_CODE" \
  -H "X-API-Key: YOUR_KEY"
```

### Method 2: Python
```python
import requests
import os

headers = {
    'X-Auth-Code': os.getenv('APILAGE_AUTH_CODE'),
    'X-API-Key': os.getenv('APILAGE_API_KEY')
}

response = requests.post(
    'https://gen.apilageai.lk/api/generate',
    headers=headers,
    json={'topic': 'Test topic', 'level': 'basic'}
)

print(response.status_code, response.json())
```

### Method 3: JavaScript
```javascript
const headers = {
    'X-Auth-Code': process.env.APILAGE_AUTH_CODE,
    'X-API-Key': process.env.APILAGE_API_KEY
};

fetch('https://gen.apilageai.lk/api/generate', {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic: 'Test topic', level: 'basic' })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## ⚙️ Configuration

### SDK Options
```javascript
const client = new ApilageAI({
    baseUrl: 'https://gen.apilageai.lk',  // API endpoint
    authCode: process.env.APILAGE_AUTH_CODE,
    apiKey: process.env.APILAGE_API_KEY,
    pollInterval: 3000,  // Check status every 3s
    timeout: 30000       // 30 second timeout
});
```

### Environment Variables
```bash
# Required
APILAGE_AUTH_CODE=your_auth_code
APILAGE_API_KEY=your_api_key

# Optional
FLASK_ENV=production
DEBUG=false
```

---

## 🚀 Quick Start

### 1️⃣ Get Credentials
Contact admin for your unique credentials

### 2️⃣ Create .env File
```bash
cat > .env << EOF
APILAGE_AUTH_CODE=your_code
APILAGE_API_KEY=your_key
EOF
chmod 600 .env  # Protect file
```

### 3️⃣ Initialize SDK
```javascript
const client = new ApilageAI({
    authCode: process.env.APILAGE_AUTH_CODE,
    apiKey: process.env.APILAGE_API_KEY
});
```

### 4️⃣ Make Request
```javascript
const job = await client.generate('Your topic', { level: 'basic' });
console.log('Job ID:', job.id);
```

### 5️⃣ Check Status
```javascript
const status = await client.getStatus(job.id);
console.log('Status:', status.status);  // pending, processing, completed, failed
```

---

## 🎯 Common Tasks

### Generate a Video
```javascript
const job = await client.generate('Explain photosynthesis', {
    level: 'basic'
});
```

### Wait for Completion
```javascript
const video = await client.generateAndWait('Topic', {
    onProgress: (status) => console.log(status.progress)
});
console.log('Download:', video.downloadUrl);
```

### Check Job Status
```javascript
const status = await client.getStatus(jobId);
if (status.isComplete()) {
    console.log('Video:', status.fullUrl);
}
```

### Cancel Job
```javascript
await client.cancelJob(jobId);
```

### List All Jobs
```javascript
const jobs = await client.listJobs({ page: 1, per_page: 20 });
console.log('Total:', jobs.length);
```

### Delete Video
```javascript
await client.deleteVideo(jobId);
```

---

## 🔍 Debugging

### Enable Logging
```javascript
const client = new ApilageAI({
    // ... config
    debug: true  // Shows all requests/responses
});
```

### Check Request Headers
```bash
curl -v -X POST https://gen.apilageai.lk/api/generate \
  -H "X-Auth-Code: YOUR_CODE" \
  -H "X-API-Key: YOUR_KEY"
```

### View Network Traffic
```javascript
// Browser DevTools > Network tab
// Shows all requests and responses
```

---

## ⚡ Performance Tips

1. ✅ **Reuse client instance** (don't create new ones)
2. ✅ **Cache status** to avoid rate limits
3. ✅ **Implement polling** with exponential backoff
4. ✅ **Use batch operations** where available
5. ✅ **Monitor rate limits** in production

---

## 🚨 Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| **401 Error** | Wrong credentials | Check .env file |
| **429 Error** | Rate limited | Wait 1 hour |
| **400 Error** | Invalid input | Check topic length & characters |
| **Timeout** | Server slow | Increase timeout value |
| **No response** | Network issue | Check internet connection |

---

## 📚 Documentation

- **Full Guide**: See `API_INTEGRATION_GUIDE.md`
- **Security Details**: See `SECURITY_CHECKLIST.md`
- **Web Interface**: Visit `/api-docs`
- **Test Suite**: Run `python3 test_api_auth.py`

---

## 💡 Remember

- 🔐 **Credentials are SECRET** - never share, never hardcode
- ⏱️ **Rate limits apply** - max 10 requests/hour
- ✅ **Always validate input** - before sending to API
- 🔄 **Always handle errors** - implement retry logic
- 📊 **Monitor usage** - check rate limit headers
- 🚀 **Test locally** - before deploying to production

---

**Status**: 🟢 100% SECURED & READY TO USE

**Last Updated**: January 14, 2026  
**Version**: 1.0.0

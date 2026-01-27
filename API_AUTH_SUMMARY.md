# API Authentication Implementation Summary

## Changes Made

### 1. **API Authentication Added** ✅
- All `/api/*` endpoints now require authentication
- Web UI (`/`, `/generate`, `/videos`, etc.) remains **publicly accessible**
- Authentication uses custom headers: `X-Auth-Code` and `X-API-Key`

### 2. **Level Parameter Removed** 🗑️
- The `level` parameter (basic, intermediate, specialist) has been removed from all endpoints
- API now only requires `topic` parameter
- All documentation updated to reflect this change

### 3. **Credentials** 🔐
Credentials are stored securely in `.env` file:
```
AUTH_CODE=AuthWiThDineth@apilageai
API_KEY=Dineth@30133637HElovEdLithumi
```

**⚠️ Important:** These credentials are NEVER exposed in:
- API documentation
- Frontend code
- Public responses

### 3. **Protected Endpoints**
The following endpoints now require authentication:
- `POST /api/generate` - Submit video generation request
- `GET /api/status/{job_id}` - Check job status
- `GET /api/video/{job_id}` - Get video details
- `GET /api/queue` - Get queue status
- `POST /api/cancel/{job_id}` - Cancel job
- `GET /api/videos` - List all videos
- `GET /api/uploads` - List uploaded files

### 4. **Public Endpoints (No Auth Required)**
- `GET /` - Main web UI
- `GET /api-docs` - API documentation
- `POST /generate` - Web UI video generation
- `GET /videos` - List videos for web UI
- `GET /uploads/{filename}` - Serve video files
- `GET /health` - Health check

### 5. **API Documentation Updated** 📚
- Domain changed from `gen.apilageai.lk` to `nova.apilageai.lk`
- Authentication section added with clear instructions
- All code examples updated with placeholder credentials
- Contact information added for credential requests

### 6. **SDK Updated** 🛠️
The JavaScript SDK (`apilage-sdk.js`) now supports authentication:
```javascript
const client = new ApilageAI({
    baseUrl: 'https://nova.apilageai.lk',
    authCode: 'YOUR_AUTH_CODE',
    apiKey: 'YOUR_API_KEY'
});
```

## Usage

### For Public Users (Web UI)
✅ **No authentication required**
- Visit: https://nova.apilageai.lk
- Use the interface to generate videos
- No API credentials needed

### For API Users (Programmatic Access)
🔐 **Authentication required**
- Request credentials from administrator
- Include headers in all API requests:
  ```bash
  X-Auth-Code: YOUR_AUTH_CODE
  X-API-Key: YOUR_API_KEY
  ```

## Example API Request

```bash
curl -X POST https://nova.apilageai.lk/api/generate \
  -H "Content-Type: application/json" \
  -H "X-Auth-Code: YOUR_AUTH_CODE" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"topic": "Explain gravity"}'
```

**Note:** The `level` parameter is no longer used or required.

## Error Responses

### Missing Credentials (401)
```json
{
  "success": false,
  "error": "Missing authentication headers. Required: X-Auth-Code and X-API-Key"
}
```

### Invalid Credentials (403)
```json
{
  "success": false,
  "error": "Invalid authentication credentials"
}
```

## Deployment

After uploading the updated files to your server:

```bash
cd /home/nova/public_html
sudo systemctl restart video-generator
```

## Testing

### Test Web UI (No Auth)
```bash
curl https://nova.apilageai.lk/
curl https://nova.apilageai.lk/health
```

### Test API (With Auth)
```bash
curl -X POST https://nova.apilageai.lk/api/generate \
  -H "Content-Type: application/json" \
  -H "X-Auth-Code: AuthWiThDineth@apilageai" \
  -H "X-API-Key: Dineth@30133637HElovEdLithumi" \
  -d '{"topic": "Test video"}'
```

### Test API (Without Auth - Should Fail)
```bash
curl -X POST https://nova.apilageai.lk/api/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test video"}'
```

## Security Notes

1. ✅ Credentials stored in `.env` (not in git)
2. ✅ Credentials never exposed in API responses
3. ✅ API documentation shows only placeholders
4. ✅ Web UI remains publicly accessible
5. ✅ API access properly restricted

## Files Modified

1. `app.py` - Added authentication middleware
2. `templates/api-docs.html` - Updated with auth info and new domain
3. `static/apilage-sdk.js` - Added auth header support
4. Domain references changed from `gen.apilageai.lk` to `nova.apilageai.lk`

---

**Last Updated:** January 27, 2026

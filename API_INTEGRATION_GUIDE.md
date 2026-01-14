# 🚀 API Integration Guide

Complete guide for integrating Apilage AI Video API into your projects.

---

## Installation

### JavaScript/Node.js

1. **Download SDK**
```bash
# Copy the SDK to your project
cp apilage-sdk.js ./node_modules/apilage-sdk/
```

2. **Setup Credentials**
```bash
# Create .env file
cat > .env << EOF
APILAGE_AUTH_CODE=YOUR_AUTH_CODE_HERE
APILAGE_API_KEY=YOUR_API_KEY_HERE
EOF
```

3. **Basic Usage**
```javascript
const ApilageAI = require('./apilage-sdk.js');

const client = new ApilageAI({
    baseUrl: 'https://gen.apilageai.lk',
    authCode: process.env.APILAGE_AUTH_CODE,
    apiKey: process.env.APILAGE_API_KEY
});

// Generate video
const job = await client.generate('Explain photosynthesis', {
    level: 'basic',
    onProgress: (status) => console.log(status.progress)
});

console.log('Job ID:', job.id);
```

### Python

1. **Setup**
```bash
pip install requests python-dotenv
```

2. **Create .env**
```bash
cat > .env << EOF
APILAGE_AUTH_CODE=YOUR_AUTH_CODE_HERE
APILAGE_API_KEY=YOUR_API_KEY_HERE
EOF
```

3. **Basic Usage**
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    'X-Auth-Code': os.getenv('APILAGE_AUTH_CODE'),
    'X-API-Key': os.getenv('APILAGE_API_KEY')
}

# Generate video
response = requests.post(
    'https://gen.apilageai.lk/api/generate',
    headers=headers,
    json={
        'topic': 'Explain photosynthesis',
        'level': 'basic'
    }
)

if response.status_code == 200:
    job = response.json()
    print(f"Job ID: {job['job_id']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### cURL

```bash
# Set credentials
export AUTH_CODE="YOUR_AUTH_CODE_HERE"
export API_KEY="YOUR_API_KEY_HERE"

# Generate video
curl -X POST https://gen.apilageai.lk/api/generate \
  -H "X-Auth-Code: $AUTH_CODE" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Explain photosynthesis",
    "level": "basic"
  }'
```

---

## API Endpoints

### 1. Generate Video
**POST** `/api/generate`

Generate a new educational video.

**Request:**
```json
{
    "topic": "Explain the water cycle",
    "level": "basic"
}
```

**Level Options:**
- `basic` - Simple explanation (beginner level)
- `intermediate` - Moderate complexity
- `special_topic` - Advanced/specialized topics

**Response (201):**
```json
{
    "success": true,
    "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "Video generation queued",
    "queue_position": 1,
    "status_url": "/api/status/a1b2c3d4-...",
    "video_url": "/api/video/a1b2c3d4-..."
}
```

**Errors:**
- `400` - Invalid input (missing topic, invalid level)
- `401` - Missing/invalid credentials
- `429` - Rate limit exceeded (10 req/hour)

---

### 2. Check Status
**GET** `/api/status/{job_id}`

Check the status of a video generation job.

**Response (200):**
```json
{
    "success": true,
    "job": {
        "id": "a1b2c3d4-...",
        "status": "processing",
        "progress": "Rendering video...",
        "created_at": "2026-01-14T10:30:00Z",
        "updated_at": "2026-01-14T10:35:00Z",
        "video_url": null
    }
}
```

**Status Values:**
- `pending` - Waiting in queue
- `processing` - Currently generating
- `completed` - Video ready
- `failed` - Generation failed

---

### 3. Download Video
**GET** `/api/video/{job_id}`

Download the generated video file.

**Response (200):** Video file (MP4)

**Errors:**
- `404` - Job not found
- `400` - Video not yet available

---

### 4. Cancel Job
**POST** `/api/cancel/{job_id}`

Cancel a pending or processing job.

**Response (200):**
```json
{
    "success": true,
    "message": "Job cancelled successfully"
}
```

---

### 5. List All Jobs
**GET** `/api/jobs`

Get list of all your jobs (paginated).

**Query Parameters:**
- `page` (optional) - Page number (default: 1)
- `per_page` (optional) - Items per page (default: 20)

**Response (200):**
```json
{
    "success": true,
    "jobs": [
        {
            "id": "a1b2c3d4-...",
            "topic": "Explain photosynthesis",
            "level": "basic",
            "status": "completed",
            "created_at": "2026-01-14T10:00:00Z"
        }
    ],
    "total": 42,
    "page": 1,
    "per_page": 20
}
```

---

### 6. Delete Video
**DELETE** `/api/video/{job_id}`

Delete a generated video to free up storage.

**Response (200):**
```json
{
    "success": true,
    "message": "Video deleted successfully"
}
```

---

### 7. Refresh Job
**POST** `/api/refresh`

Refresh job status for multiple jobs.

**Request:**
```json
{
    "job_ids": ["id1", "id2", "id3"]
}
```

**Response (200):**
```json
{
    "success": true,
    "jobs": [
        {
            "id": "id1",
            "status": "completed",
            "progress": "100%"
        }
    ]
}
```

---

## Rate Limiting

**Limit**: 10 requests per hour per IP address

**Headers on Rate Limit (429):**
```
Retry-After: 3600
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1610620800
```

**Handling Rate Limits:**
```javascript
async function makeRequest(url, options) {
    const response = await fetch(url, options);
    
    if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        console.log(`Rate limited. Wait ${retryAfter} seconds`);
        
        // Wait before retrying
        await new Promise(r => setTimeout(r, retryAfter * 1000));
        return makeRequest(url, options); // Retry
    }
    
    return response;
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | Process response |
| 201 | Created | Job queued successfully |
| 400 | Bad Request | Check input validation |
| 401 | Unauthorized | Check credentials |
| 404 | Not Found | Job ID doesn't exist |
| 429 | Too Many Requests | Wait and retry later |
| 500 | Server Error | Retry with exponential backoff |

### Error Response Format

```json
{
    "success": false,
    "error": "Error description",
    "required_headers": {
        "X-Auth-Code": "Your authorization code",
        "X-API-Key": "Your API key"
    }
}
```

### Exponential Backoff

```javascript
async function makeRequestWithRetry(url, options, maxRetries = 3) {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const response = await fetch(url, options);
            
            if (response.ok) return response;
            if (response.status !== 429 && response.status !== 500) throw response;
            
            const delay = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
            await new Promise(r => setTimeout(r, delay));
            
        } catch (error) {
            if (attempt === maxRetries - 1) throw error;
        }
    }
}
```

---

## Examples

### Complete Node.js Example

```javascript
require('dotenv').config();
const ApilageAI = require('./apilage-sdk.js');

async function main() {
    try {
        // Initialize client
        const client = new ApilageAI({
            baseUrl: 'https://gen.apilageai.lk',
            authCode: process.env.APILAGE_AUTH_CODE,
            apiKey: process.env.APILAGE_API_KEY,
            pollInterval: 2000,  // Check status every 2 seconds
            timeout: 60000       // 60 second timeout
        });

        // Generate and wait for video
        console.log('Generating video...');
        const video = await client.generateAndWait(
            'Explain the theory of relativity',
            {
                level: 'intermediate',
                onProgress: (status) => {
                    console.log(`[${status.status}] ${status.progress}`);
                }
            }
        );

        console.log('✅ Video generated!');
        console.log('Video URL:', video.fullUrl);
        console.log('Download:', video.downloadUrl);

        // List all jobs
        const jobs = await client.listJobs({ per_page: 10 });
        console.log(`Total jobs: ${jobs.length}`);

    } catch (error) {
        console.error('❌ Error:', error.message);
        if (error.response) {
            console.error('Response:', error.response);
        }
    }
}

main();
```

### Complete Python Example

```python
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

class ApilageAI:
    def __init__(self):
        self.base_url = 'https://gen.apilageai.lk'
        self.headers = {
            'X-Auth-Code': os.getenv('APILAGE_AUTH_CODE'),
            'X-API-Key': os.getenv('APILAGE_API_KEY'),
            'Content-Type': 'application/json'
        }
    
    def generate(self, topic, level='basic'):
        """Generate video"""
        response = requests.post(
            f'{self.base_url}/api/generate',
            headers=self.headers,
            json={'topic': topic, 'level': level}
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.json()}")
        return response.json()
    
    def get_status(self, job_id):
        """Check job status"""
        response = requests.get(
            f'{self.base_url}/api/status/{job_id}',
            headers=self.headers
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")
        return response.json()['job']
    
    def wait_for_completion(self, job_id, check_interval=3):
        """Wait for video generation"""
        while True:
            job = self.get_status(job_id)
            
            if job['status'] == 'completed':
                return job
            elif job['status'] == 'failed':
                raise Exception(f"Job failed: {job.get('error')}")
            
            print(f"[{job['status']}] {job['progress']}")
            time.sleep(check_interval)

# Usage
if __name__ == '__main__':
    api = ApilageAI()
    
    # Generate video
    result = api.generate('Explain quantum computing', level='intermediate')
    job_id = result['job_id']
    print(f"Job created: {job_id}")
    
    # Wait for completion
    job = api.wait_for_completion(job_id)
    print(f"✅ Video ready: {job['video_url']}")
```

---

## Playground

### Web Interface
Visit `/api-docs` for interactive API testing.

**Features:**
- Test all endpoints
- See real request/response
- Code examples in 3 languages
- Built-in error handling

### Test Credentials
```
Auth Code: YOUR_AUTH_CODE_HERE
API Key: YOUR_API_KEY_HERE
```

---

## Troubleshooting

### 401 Unauthorized
**Problem**: Invalid or missing credentials
**Solution**: Check your `.env` file and credentials

```bash
# Verify credentials
echo $APILAGE_AUTH_CODE
echo $APILAGE_API_KEY
```

### 429 Too Many Requests
**Problem**: Exceeded rate limit (10 req/hour)
**Solution**: Wait 1 hour before trying again, or implement exponential backoff

### 400 Bad Request
**Problem**: Invalid input
**Solutions**:
- Check topic is 3-500 characters
- Check level is: basic, intermediate, or special_topic
- Ensure JSON is valid
- No forbidden characters: `<>{}$\`;rm DROP DELETE`

### Timeout
**Problem**: Request took too long
**Solution**: Increase timeout value in SDK
```javascript
const client = new ApilageAI({
    timeout: 120000  // 2 minutes
});
```

---

## Best Practices

1. ✅ **Always use .env files** for credentials
2. ✅ **Implement exponential backoff** for retries
3. ✅ **Cache status checks** to avoid rate limits
4. ✅ **Handle all error codes** gracefully
5. ✅ **Monitor rate limits** in production
6. ✅ **Use HTTPS only** for all requests
7. ✅ **Validate input** before sending
8. ✅ **Log API errors** for debugging
9. ✅ **Test locally** before production
10. ✅ **Keep SDK updated** regularly

---

## Support

- 📖 **API Docs**: `/api-docs`
- 🐛 **Report Issues**: Contact admin
- 💬 **Questions**: Email support@apilageai.lk

---

**Version**: 1.0.0  
**Last Updated**: January 14, 2026

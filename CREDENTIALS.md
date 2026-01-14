# 🔑 API Credentials & Quick Reference

## Your Credentials (KEEP PRIVATE!)

```
Authorization Code:
AuthWiThDineth@apilageai

API Key:
Dineth@30133637HElovEdLithumi
```

⚠️ **NEVER share these credentials with anyone!**

---

## Quick API Usage

### Headers Required
```
X-Auth-Code: AuthWiThDineth@apilageai
X-API-Key: Dineth@30133637HElovEdLithumi
Content-Type: application/json
```

### Quick Example (cURL)
```bash
curl -X POST http://localhost:5002/api/generate \
  -H "X-Auth-Code: AuthWiThDineth@apilageai" \
  -H "X-API-Key: Dineth@30133637HElovEdLithumi" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Your topic here", "level": "basic"}'
```

### Quick Example (Python)
```python
import requests

requests.post("http://localhost:5002/api/generate",
    headers={
        "X-Auth-Code": "AuthWiThDineth@apilageai",
        "X-API-Key": "Dineth@30133637HElovEdLithumi"
    },
    json={"topic": "Your topic", "level": "basic"}
)
```

---

## API Endpoints

| Method | Endpoint | Status |
|--------|----------|--------|
| POST | `/api/generate` | 🔐 Protected |
| GET | `/api/status/{id}` | 🔐 Protected |
| GET | `/api/video/{id}` | 🔐 Protected |
| GET | `/api/queue` | 🔐 Protected |
| GET | `/api/videos` | 🔐 Protected |
| POST | `/api/cancel/{id}` | 🔐 Protected |
| GET | `/api/uploads` | 🔐 Protected |
| GET | `/` | ✅ Public |
| GET | `/api-docs` | ✅ Public |
| GET | `/api/auth-info` | ✅ Public |

---

## Test Security

```bash
python test_api_auth.py
```

---

## Files to Keep Private

- ⚠️ `.env` - **Never commit or share**
- ⚠️ `SECURITY_SETUP.md` - Contains setup notes
- ⚠️ This file - Contains your credentials

---

## For More Details

📖 See: `API_AUTHENTICATION.md` for complete documentation
🧪 See: `test_api_auth.py` for implementation examples

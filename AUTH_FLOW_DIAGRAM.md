# API Authentication Flow Diagram

## Authentication Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Request                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │   Is this a /api/ endpoint?         │
        └─────────┬──────────────────┬────────┘
                  │                  │
                  │ NO               │ YES
                  │                  │
        ┌─────────▼──┐      ┌────────▼──────────────┐
        │   PUBLIC   │      │  Check Headers       │
        │ ENDPOINT   │      └──────┬────────────────┘
        │            │             │
        │ - /        │             ▼
        │ - /api-    │    ┌────────────────────────────┐
        │   docs     │    │  X-Auth-Code Present?     │
        │ - /api/    │    │  X-API-Key Present?       │
        │   auth-    │    └──┬──────────────────────┬──┘
        │   info     │       │NO                    │YES
        │            │       │                      │
        │ ✅ ALLOW   │       ▼                      ▼
        │    NO      │  ┌──────────────┐    ┌──────────────┐
        │    AUTH    │  │ Return 401   │    │   Verify    │
        └────────────┘  │ Unauthorized │    │ Credentials │
                        └──────────────┘    └──┬──────────┬┘
                                               │          │
                                             MATCH      NO MATCH
                                               │          │
                                               ▼          ▼
                                          ┌────────┐  ┌────────┐
                                          │ ALLOW  │  │REJECT  │
                                          │ REQUEST│  │ 401    │
                                          └────────┘  └────────┘
```

## Credential Verification Process

```
CLIENT REQUEST
    │
    ├─ Header: X-Auth-Code
    └─ Header: X-API-Key
    
         │
         ▼
    
    @require_api_key decorator
    verify_api_credentials()
    
         │
         ├─ Get X-Auth-Code from headers
         ├─ Get X-API-Key from headers
         └─ Compare with .env values
    
         │
         ├─ If BOTH match → ✅ PROCEED
         └─ If EITHER missing/wrong → ❌ REJECT (401)
```

## Request Flow Example

### Success Flow (With Valid Credentials)
```
1. Client sends POST /api/generate
   Headers:
   - X-Auth-Code: AuthWiThDineth@apilageai ✅
   - X-API-Key: Dineth@30133637HElovEdLithumi ✅
   - Content-Type: application/json
   
2. @require_api_key checks headers

3. verify_api_credentials() compares with .env:
   - AUTH_CODE from .env matches header ✅
   - API_KEY from .env matches header ✅

4. Credentials valid → Call api_generate()

5. Return: {"success": true, "job_id": "xxx"}
```

### Failure Flow (Missing/Invalid Credentials)
```
1. Client sends POST /api/generate
   Headers:
   - Missing X-Auth-Code ❌
   - Missing X-API-Key ❌
   - Content-Type: application/json

2. @require_api_key checks headers

3. verify_api_credentials() returns False
   - No matching headers found

4. Credentials invalid → REJECT

5. Return 401:
   {
     "success": false,
     "error": "Unauthorized: Invalid or missing API credentials",
     "required_headers": {...}
   }
```

## File Structure

```
Project Root/
├── .env                          ← CREDENTIALS (KEEP PRIVATE!)
│   ├── AUTH_CODE=...
│   └── API_KEY=...
│
├── app.py                        ← MODIFIED
│   ├── Load .env with load_dotenv()
│   ├── Load AUTH_CODE and API_KEY
│   ├── verify_api_credentials() function
│   ├── @require_api_key decorator
│   └── All /api/ endpoints protected
│
├── test_api_auth.py             ← NEW (TESTING)
│   └── Automated security tests
│
├── API_AUTHENTICATION.md        ← NEW (GUIDE)
│   └── Complete usage guide
│
├── SECURITY_SETUP.md            ← NEW (SETUP)
│   └── Implementation details
│
├── CREDENTIALS.md               ← NEW (QUICK REF)
│   └── Quick reference card
│
└── .gitignore                   ← UPDATED
    └── .env (never committed!)
```

## Security Layers

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: File System Protection                     │
│  • .env in .gitignore → Never committed to git      │
│  • .env has restricted file permissions             │
│  • Credentials never in source code                 │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Layer 2: Application Level Protection              │
│  • @require_api_key decorator on all /api/ routes   │
│  • verify_api_credentials() function checks headers │
│  • Returns 401 Unauthorized for failures            │
│  • Credentials loaded from .env at startup          │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Layer 3: HTTP Header Protection                    │
│  • Two required headers: X-Auth-Code & X-API-Key   │
│  • Headers case-sensitive                           │
│  • Both must match to allow access                  │
│  • Can't be in URL query strings (less secure)     │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Layer 4: Strong Credentials                        │
│  • Long, random auth code                          │
│  • Complex API key with numbers, letters, symbols  │
│  • Not guessable or dictionary words               │
│  • Unique to this system                           │
└─────────────────────────────────────────────────────┘
```

## How Authentication Works

```
REQUEST ARRIVES
        │
        ▼
Is request to /api/ endpoint? 
        │
        ├─ NO  → Public endpoint (/, /api-docs, /api/auth-info)
        │        ✅ ALLOW (no auth needed)
        │
        └─ YES → Protected endpoint
                 ▼
        @require_api_key decorator activates
                 │
                 ▼
        Call verify_api_credentials()
                 │
                 ├─ Get X-Auth-Code header
                 ├─ Get X-API-Key header
                 └─ Compare both against .env values
                 │
                 ├─ Both match? → ✅ ALLOW
                 │                Process request normally
                 │
                 └─ One/both missing or wrong? → ❌ REJECT
                                                 Return 401
                                                 Include error message
```

## Example: Step-by-Step Request

### Scenario: User generates a video with valid credentials

```
CLIENT
  │
  ├─ Prepares POST request
  │  URL: http://localhost:5002/api/generate
  │  Headers:
  │    Content-Type: application/json
  │    X-Auth-Code: AuthWiThDineth@apilageai
  │    X-API-Key: Dineth@30133637HElovEdLithumi
  │  Body: {"topic": "Explain photosynthesis", "level": "basic"}
  │
  └─ Sends request →
         
         SERVER
           │
           ├─ Receives request
           ├─ Checks if route is /api/generate
           │  → YES, has @require_api_key decorator
           │
           ├─ Calls decorated function wrapper
           │  └─ Calls verify_api_credentials()
           │     ├─ Gets headers: Auth Code & API Key
           │     ├─ Loads from .env: AUTH_CODE & API_KEY
           │     └─ Compares: Do they match?
           │        YES → Continue
           │
           ├─ Calls api_generate() function
           │  ├─ Validates input
           │  ├─ Creates job
           │  └─ Returns success response
           │
           └─ Sends response →
         
         CLIENT
           │
           ├─ Status: 200 OK
           ├─ Response body:
           │  {
           │    "success": true,
           │    "job_id": "abc123...",
           │    "message": "Video generation queued",
           │    "queue_position": 1
           │  }
           │
           └─ User can now check job status with job_id
```

## Testing Flow

```
Test Suite (test_api_auth.py)
│
├─ Test 1: Get auth info (PUBLIC)
│  └─ Should succeed without headers
│
├─ Test 2: Request without credentials
│  └─ Should fail with 401
│
├─ Test 3: Request with invalid credentials
│  └─ Should fail with 401
│
├─ Test 4: Request with valid credentials
│  └─ Should succeed with 200
│
├─ Test 5: Access protected endpoint with auth
│  └─ Should succeed with proper data
│
└─ Results: ✅ PASS/FAIL for each test
```

---

**This architecture ensures your API is secure while remaining easy to use!** 🔒

# 🚀 Deployment Checklist

## Files to Upload to Server

Upload these modified files to `/home/nova/public_html/`:

- ✅ `app.py` - Added API authentication
- ✅ `templates/api-docs.html` - Updated with authentication info & removed level parameter
- ✅ `static/apilage-sdk.js` - Added authentication headers support
- ✅ `templates/index.html` - Added debug logging (optional, can keep or revert)

## Deployment Steps

```bash
# 1. Navigate to project directory
cd /home/nova/public_html

# 2. After uploading files, restart the service
sudo systemctl restart video-generator

# 3. Check if service is running
sudo systemctl status video-generator

# 4. Check logs for any errors
sudo journalctl -u video-generator -n 50 --no-pager
```

## Testing

### Quick Test Script
```bash
# Make test script executable
chmod +x test-api.sh

# Run API tests
./test-api.sh
```

### Manual Testing

**Test 1: Web UI (No Auth - Should Work)**
```bash
curl https://nova.apilageai.lk/health
```

**Test 2: API without Auth (Should Fail with 401)**
```bash
curl -X POST https://nova.apilageai.lk/api/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test"}'
```

**Test 3: API with Auth (Should Work)**
```bash
curl -X POST https://nova.apilageai.lk/api/generate \
  -H "Content-Type: application/json" \
  -H "X-Auth-Code: AuthWiThDineth@apilageai" \
  -H "X-API-Key: Dineth@30133637HElovEdLithumi" \
  -d '{"topic": "Explain gravity"}'
```

## Verification Checklist

- [ ] Service is running: `sudo systemctl status video-generator`
- [ ] No errors in logs: `sudo journalctl -u video-generator -n 20`
- [ ] Web UI accessible: Visit https://nova.apilageai.lk
- [ ] API docs accessible: Visit https://nova.apilageai.lk/api-docs
- [ ] Health check works: `curl https://nova.apilageai.lk/health`
- [ ] API requires auth: Test without credentials (should get 401)
- [ ] API works with auth: Test with credentials (should succeed)
- [ ] Videos are loading in web UI

## What Changed

### ✅ Added
- API authentication middleware
- X-Auth-Code and X-API-Key header validation
- Authentication section in API documentation
- SDK support for authentication headers

### 🗑️ Removed
- `level` parameter from all API endpoints
- Level dropdown from API documentation
- Level selection from "Try It Live" section

### 🔄 Updated
- Domain changed: `gen.apilageai.lk` → `nova.apilageai.lk`
- All API examples updated with authentication
- SDK examples updated with credentials

## Troubleshooting

### Service won't start
```bash
# Check for Python syntax errors
cd /home/nova/public_html
source venv/bin/activate
python3 -c "import app"
```

### Authentication not working
```bash
# Verify .env file has credentials
cat .env | grep -E "AUTH_CODE|API_KEY"

# Should show:
# AUTH_CODE=AuthWiThDineth@apilageai
# API_KEY=Dineth@30133637HElovEdLithumi
```

### API returns 500 error
```bash
# Check application logs
sudo journalctl -u video-generator -n 100 --no-pager | grep -i error
```

## Rollback (If Needed)

If something goes wrong, restore previous version:
```bash
cd /home/nova/public_html
# Restore from backup (if you made one)
# cp app.py.backup app.py
# cp templates/api-docs.html.backup templates/api-docs.html
sudo systemctl restart video-generator
```

---

**Last Updated:** January 27, 2026

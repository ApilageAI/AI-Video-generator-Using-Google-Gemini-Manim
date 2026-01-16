# Quick Fix Guide: "Load failed" Error

## Problem
When testing the API on `/api-docs`, clicking "Generate a Video" shows:
```
{ "error": "Load failed" }
```

## Root Cause
SDK client initialized without authentication credentials.

## Solution (3 Steps)

### Step 1: Get Your Credentials
Open `.env` file and find:
```
AUTH_CODE=your_code_here
API_KEY=your_key_here
```

### Step 2: Enter Them in API Docs
1. Go to: `http://localhost:5002/api-docs`
2. Scroll to **"Try It Live"** section
3. Look for **"Authentication"** subsection (top of section)
4. Fill in:
   - **Auth Code:** Paste your AUTH_CODE value
   - **API Key:** Paste your API_KEY value
5. Click **"Save Credentials"** button
6. Wait for: ✅ **"Credentials saved!"** message

### Step 3: Generate Videos
Now fill in the Generate a Video section:
1. Enter topic (e.g., "Explain gravity")
2. Select level
3. Click "Generate Video"
4. 🎉 It works!

---

## What Was Added

✨ **New Authentication Section** in "Try It Live":
- Auth Code input field
- API Key input field
- Save Credentials button
- Status message display

---

## Before & After

**Before:**
```
Try It Live → Generate a Video → [Click Generate] → ❌ "Load failed"
```

**After:**
```
Try It Live → [NEW: Enter Credentials] → Save ✅ → Generate Video → ✅ Works!
```

---

## Technical Details

**File Changed:** `templates/api-docs.html`

**Functions Added:**
- `updateCredentials()` - Saves credentials and reinitializes SDK
- Updated `generateVideo()` - Validates credentials first

**No Backend Changes:** Pure frontend fix

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Still shows "Load failed" | Make sure you clicked "Save Credentials" first |
| Fields are empty | Copy from `.env` file exactly |
| 401 Unauthorized | Check AUTH_CODE and API_KEY are correct |
| "Please enter credentials" alert | You haven't filled in both fields yet |

---

**Status:** ✅ Fixed
**Time to Fix:** 5 minutes (get credentials + enter them + test)

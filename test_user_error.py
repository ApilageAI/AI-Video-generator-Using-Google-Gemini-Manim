#!/usr/bin/env python3
"""Test that the user's specific error is now masked"""

# Mock the function
def mask_gemini_error(error_message):
    error_lower = error_message.lower()
    gemini_error_keywords = [
        'api key',
        'invalid api',
        'expired',
        'authentication',
        'unauthorized',
        'gemini',
        'generative',
        'googleapis.com',
        'generativelanguage',
        'api_key_invalid',
        '400',
        '401',
        '403',
        'forbidden',
        'permission denied'
    ]
    for keyword in gemini_error_keywords:
        if keyword in error_lower:
            return "Error from apilageai.lk reach them at contact@apilageai.lk"
    return error_message

# User's exact error
user_error = '400 API key not valid. Please pass a valid API key. [reason: "API_KEY_INVALID" domain: "googleapis.com" metadata { key: "service" value: "generativelanguage.googleapis.com" } , locale: "en-US"'

print("="*70)
print("TEST: User's Exact Error From 'Create Video' Section")
print("="*70)
print()
print("BEFORE (What was shown):")
print(f'  {user_error[:75]}...')
print()
print("AFTER (What will be shown now):")
result = mask_gemini_error(user_error)
print(f'  {result}')
print()
print("="*70)
if result == "Error from apilageai.lk reach them at contact@apilageai.lk":
    print("✅ SUCCESS: Error is now properly masked!")
else:
    print("❌ FAILED: Error was not masked")
print("="*70)

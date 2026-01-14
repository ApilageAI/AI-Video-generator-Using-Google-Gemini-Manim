#!/usr/bin/env python3
"""
Test script to demonstrate Gemini API error masking.
Run this to verify the mask_gemini_error() function works correctly.
"""

# Import the mask_gemini_error function (simulated here for testing)
def mask_gemini_error(error_message):
    """
    Mask Gemini API errors to hide technology stack.
    Shows generic error message for Gemini-specific errors.
    Other errors pass through unchanged.
    """
    error_lower = error_message.lower()
    
    # Check if this is a Gemini API error
    gemini_error_keywords = [
        'api key',
        'invalid api',
        'expired',
        'authentication',
        'unauthorized',
        'gemini',
        'generative',  # Catches both "generative ai" and "generative-ai"
        'googleapis.com',
        'generativelanguage',
        'api_key_invalid',
        '400',  # Bad request (often API key issues)
        '401',
        '403',
        'forbidden',
        'permission denied'
    ]
    
    # If it's a Gemini error, return masked message
    for keyword in gemini_error_keywords:
        if keyword in error_lower:
            return "Error from apilageai.lk reach them at contact@apilageai.lk"
    
    # Otherwise, return the original error
    return error_message


def test_error_masking():
    """Test the error masking function with various error types."""
    
    print("=" * 70)
    print("🔒 GEMINI ERROR MASKING TEST SUITE")
    print("=" * 70)
    print()
    
    # Test cases: (description, input_error, should_mask)
    test_cases = [
        # Gemini API errors that should be masked
        ("Invalid API Key", "invalid_request_error: Invalid API Key provided. You can find your API Key at https://aistudio.google.com/app/apikey", True),
        ("API Key validation", "Error: The API key provided is not valid", True),
        ("Expired credentials", "Error: Your API credentials have expired", True),
        ("Authentication failure", "Authentication failed: Invalid credentials", True),
        ("Unauthorized access", "Unauthorized: 401 Forbidden", True),
        ("Gemini API down", "Gemini API service error: 503 Service Unavailable", True),
        ("Generative AI error", "generative-ai-python/models.py: APIError", True),
        ("Permission denied", "Error: Permission denied accessing the API", True),
        ("403 Forbidden", "403 Forbidden: You do not have permission to access this resource", True),
        ("API Key Invalid (User's actual error)", "400 API key not valid. Please pass a valid API key. [reason: API_KEY_INVALID domain: googleapis.com metadata service: generativelanguage.googleapis.com]", True),
        
        # Non-Gemini errors that should pass through
        ("Timeout error", "Timeout: Video rendering exceeded 5 minutes", False),
        ("Syntax error", "Syntax error at line 42: unexpected indent", False),
        ("File not found", "FileNotFoundError: /path/to/file.mp4 not found", False),
        ("Manim error", "Manim rendering failed: Unknown scene", False),
        ("General error", "An unexpected error occurred", False),
    ]
    
    passed = 0
    failed = 0
    
    for description, error, should_mask in test_cases:
        result = mask_gemini_error(error)
        is_masked = (result == "Error from apilageai.lk reach them at contact@apilageai.lk")
        
        if is_masked == should_mask:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1
        
        print(f"{status} | {description}")
        print(f"       Input:  {error[:50]}{'...' if len(error) > 50 else ''}")
        print(f"       Output: {result[:60]}{'...' if len(result) > 60 else ''}")
        print(f"       Masked: {is_masked} (expected: {should_mask})")
        print()
    
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    print()
    
    if failed == 0:
        print("✨ All tests passed! Error masking is working correctly.")
    else:
        print(f"⚠️  {failed} test(s) failed. Please review the implementation.")
    
    print()
    return failed == 0


if __name__ == '__main__':
    success = test_error_masking()
    exit(0 if success else 1)

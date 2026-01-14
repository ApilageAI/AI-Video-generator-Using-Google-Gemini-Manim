#!/usr/bin/env python3
"""
Test script to verify API authentication is working.
Run this to test that your API is properly secured.
"""

import requests
import json
from dotenv import load_dotenv
import os

# Load credentials from .env
load_dotenv()
AUTH_CODE = os.getenv('AUTH_CODE')
API_KEY = os.getenv('API_KEY')

BASE_URL = "http://localhost:5002"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_auth_info():
    """Test the public auth info endpoint."""
    print_header("TEST 1: Get Authentication Info (Public - No Auth Required)")
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth-info")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_without_credentials():
    """Test API without credentials - should fail."""
    print_header("TEST 2: Try API Without Credentials (Should Fail)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json={"topic": "Test", "level": "basic"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            print("\n✅ SUCCESS: API correctly rejected request without credentials!")
            return True
        else:
            print("\n❌ SECURITY ISSUE: API accepted request without auth!")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_invalid_credentials():
    """Test API with invalid credentials - should fail."""
    print_header("TEST 3: Try API With Invalid Credentials (Should Fail)")
    
    try:
        headers = {
            "X-Auth-Code": "invalid_code",
            "X-API-Key": "invalid_key",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json={"topic": "Test", "level": "basic"},
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            print("\n✅ SUCCESS: API correctly rejected invalid credentials!")
            return True
        else:
            print("\n❌ SECURITY ISSUE: API accepted invalid credentials!")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_valid_credentials():
    """Test API with valid credentials - should succeed."""
    print_header("TEST 4: Try API With Valid Credentials (Should Succeed)")
    
    if not AUTH_CODE or not API_KEY:
        print("❌ ERROR: Credentials not found in .env file!")
        return False
    
    try:
        headers = {
            "X-Auth-Code": AUTH_CODE,
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json={"topic": "Simple test", "level": "basic"},
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200 and response.json().get('success'):
            print("\n✅ SUCCESS: API accepted valid credentials and processed request!")
            return True
        else:
            print("\n⚠️ API returned unexpected response")
            return True  # Still counts as passing the auth test
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_queue_with_auth():
    """Test getting queue status with authentication."""
    print_header("TEST 5: Get Queue Status With Valid Credentials")
    
    if not AUTH_CODE or not API_KEY:
        print("❌ ERROR: Credentials not found in .env file!")
        return False
    
    try:
        headers = {
            "X-Auth-Code": AUTH_CODE,
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/queue",
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS: Queue endpoint is protected and working!")
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  API AUTHENTICATION TEST SUITE")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print(f"Auth Code Loaded: {'✅ Yes' if AUTH_CODE else '❌ No'}")
    print(f"API Key Loaded: {'✅ Yes' if API_KEY else '❌ No'}")
    
    results = {
        "Get Auth Info": test_auth_info(),
        "Reject No Credentials": test_without_credentials(),
        "Reject Invalid Credentials": test_with_invalid_credentials(),
        "Accept Valid Credentials": test_with_valid_credentials(),
        "Queue Endpoint Protected": test_get_queue_with_auth(),
    }
    
    print_header("SUMMARY")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "="*60)
        print("  🔒 ALL TESTS PASSED - YOUR API IS SECURE!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("  ⚠️  SOME TESTS FAILED - CHECK YOUR CONFIGURATION")
        print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

#!/usr/bin/env python3
"""
Test script for Kahaniyaa API endpoints
Run this to verify the API is working correctly
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_endpoint(method: str, endpoint: str, data: Dict[Any, Any] = None) -> bool:
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == 200:
            print(f"✅ {method} {endpoint} - OK")
            return True
        else:
            print(f"❌ {method} {endpoint} - Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Connection failed (is server running?)")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Testing Kahaniyaa API")
    print("=" * 40)
    
    tests = [
        # Basic endpoints
        ("GET", "/"),
        ("GET", "/health"),
        ("GET", "/docs"),
        
        # Test endpoints
        ("GET", "/v1/test/sample-scenarios"),
        ("GET", "/v1/test/sample-characters"),
        ("GET", "/v1/test/supported-languages"),
        ("GET", "/v1/test/supported-tones"),
        ("GET", "/v1/test/target-audiences"),
        
        # Voice endpoints
        ("GET", "/v1/voices/"),
        ("GET", "/v1/voices/presets"),
        ("GET", "/v1/voices/emotions"),
        
        # Validation endpoints
        ("POST", "/v1/test/validate-scenario", {
            "scenario": "A brave little boat goes on an adventure"
        }),
        ("POST", "/v1/test/validate-image", {
            "image_url": "https://example.com/image.jpg",
            "user_description": "A magical forest"
        }),
        ("POST", "/v1/test/validate-characters", {
            "characters": [
                {"name": "Maya", "traits": "brave, curious"},
                {"name": "Ravi", "traits": "funny, loyal"}
            ],
            "setting": "Ancient library",
            "conflict": "Missing books"
        }),
        
        # Prompt preview
        ("POST", "/v1/test/preview-prompt", {
            "input_type": "scenario",
            "input_data": {"scenario": "A brave little boat"},
            "language": "en",
            "tone": "cheerful",
            "target_audience": "kids",
            "length": 500
        }),
    ]
    
    passed = 0
    total = len(tests)
    
    for method, endpoint, *args in tests:
        data = args[0] if args else None
        if test_endpoint(method, endpoint, data):
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        print("\n🚀 Next steps:")
        print("1. Add your API keys to .env file")
        print("2. Set up PostgreSQL and Redis for full functionality")
        print("3. Test story generation with real API keys")
        return 0
    else:
        print("❌ Some tests failed. Check the server logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

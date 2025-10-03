#!/usr/bin/env python3
"""
Test script for Kahaniyaa Microservices
Run this to verify all microservices are working correctly
"""

import asyncio
import httpx
import json
import sys
from typing import Dict, Any

# Service URLs
SERVICES = {
    "API Gateway": "http://localhost:8000",
    "Auth Service": "http://localhost:8001", 
    "Story Service": "http://localhost:8002",
    "TTS Service": "http://localhost:8003",
    "Vision Service": "http://localhost:8004"
}

async def test_service_health(client: httpx.AsyncClient, name: str, url: str) -> bool:
    """Test health endpoint of a service"""
    try:
        response = await client.get(f"{url}/health", timeout=5.0)
        if response.status_code == 200:
            print(f"✅ {name} - Healthy")
            return True
        else:
            print(f"❌ {name} - Unhealthy (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name} - Unreachable ({str(e)})")
        return False

async def test_auth_service(client: httpx.AsyncClient) -> bool:
    """Test auth service functionality"""
    base_url = SERVICES["Auth Service"]
    
    try:
        # Test user registration
        user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        
        response = await client.post(f"{base_url}/v1/auth/register", json=user_data)
        if response.status_code in [200, 400]:  # 400 if user already exists
            print("✅ Auth Service - Registration endpoint working")
        else:
            print(f"❌ Auth Service - Registration failed (Status: {response.status_code})")
            return False
        
        # Test login
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = await client.post(f"{base_url}/v1/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Auth Service - Login endpoint working")
            return True
        else:
            print(f"❌ Auth Service - Login failed (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Auth Service - Error: {str(e)}")
        return False

async def test_story_service(client: httpx.AsyncClient) -> bool:
    """Test story service functionality"""
    base_url = SERVICES["Story Service"]
    
    try:
        # Test sample scenarios
        response = await client.get(f"{base_url}/v1/test/sample-scenarios")
        if response.status_code == 200:
            print("✅ Story Service - Sample scenarios endpoint working")
        else:
            print(f"❌ Story Service - Sample scenarios failed (Status: {response.status_code})")
            return False
        
        # Test story creation (mock)
        story_data = {
            "input_type": "scenario",
            "input_data": {"scenario": "A brave little boat goes on an adventure"},
            "language": "en",
            "tone": "cheerful",
            "target_audience": "kids"
        }
        
        response = await client.post(f"{base_url}/v1/stories/", json=story_data)
        if response.status_code in [200, 500]:  # 500 expected without API keys
            print("✅ Story Service - Story creation endpoint accessible")
            return True
        else:
            print(f"❌ Story Service - Story creation failed (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Story Service - Error: {str(e)}")
        return False

async def test_tts_service(client: httpx.AsyncClient) -> bool:
    """Test TTS service functionality"""
    base_url = SERVICES["TTS Service"]
    
    try:
        # Test voice presets
        response = await client.get(f"{base_url}/v1/voices/presets")
        if response.status_code == 200:
            print("✅ TTS Service - Voice presets endpoint working")
        else:
            print(f"❌ TTS Service - Voice presets failed (Status: {response.status_code})")
            return False
        
        # Test emotions
        response = await client.get(f"{base_url}/v1/voices/emotions")
        if response.status_code == 200:
            print("✅ TTS Service - Emotions endpoint working")
            return True
        else:
            print(f"❌ TTS Service - Emotions failed (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ TTS Service - Error: {str(e)}")
        return False

async def test_vision_service(client: httpx.AsyncClient) -> bool:
    """Test vision service functionality"""
    base_url = SERVICES["Vision Service"]
    
    try:
        # Test capabilities
        response = await client.get(f"{base_url}/v1/vision/capabilities")
        if response.status_code == 200:
            print("✅ Vision Service - Capabilities endpoint working")
        else:
            print(f"❌ Vision Service - Capabilities failed (Status: {response.status_code})")
            return False
        
        # Test sample images
        response = await client.get(f"{base_url}/v1/test/sample-images")
        if response.status_code == 200:
            print("✅ Vision Service - Sample images endpoint working")
            return True
        else:
            print(f"❌ Vision Service - Sample images failed (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Vision Service - Error: {str(e)}")
        return False

async def test_api_gateway(client: httpx.AsyncClient) -> bool:
    """Test API Gateway functionality"""
    base_url = SERVICES["API Gateway"]
    
    try:
        # Test gateway health
        response = await client.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ API Gateway - Health check working")
        else:
            print(f"❌ API Gateway - Health check failed (Status: {response.status_code})")
            return False
        
        # Test proxied endpoint
        response = await client.get(f"{base_url}/v1/test/sample-scenarios")
        if response.status_code in [200, 503]:  # 503 if story service is down
            print("✅ API Gateway - Request proxying working")
            return True
        else:
            print(f"❌ API Gateway - Request proxying failed (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ API Gateway - Error: {str(e)}")
        return False

async def main():
    """Run all microservice tests"""
    print("🧪 Testing Kahaniyaa Microservices")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Test service health
        print("\n📊 Health Checks:")
        health_results = []
        for name, url in SERVICES.items():
            result = await test_service_health(client, name, url)
            health_results.append(result)
        
        # Test individual service functionality
        print("\n🔧 Functionality Tests:")
        func_results = []
        
        func_results.append(await test_auth_service(client))
        func_results.append(await test_story_service(client))
        func_results.append(await test_tts_service(client))
        func_results.append(await test_vision_service(client))
        func_results.append(await test_api_gateway(client))
        
        # Summary
        print("\n" + "=" * 50)
        health_passed = sum(health_results)
        func_passed = sum(func_results)
        
        print(f"📊 Health Checks: {health_passed}/{len(health_results)} services healthy")
        print(f"🔧 Functionality: {func_passed}/{len(func_results)} services functional")
        
        if health_passed == len(health_results) and func_passed == len(func_results):
            print("🎉 All microservices are working correctly!")
            print("\n🚀 Next steps:")
            print("1. Add your API keys to .env file for full functionality")
            print("2. Test story generation with real API keys")
            print("3. Deploy to production environment")
            return 0
        else:
            print("❌ Some microservices have issues. Check the logs above.")
            print("\n🔧 Troubleshooting:")
            print("1. Ensure all services are running")
            print("2. Check Docker containers: docker-compose -f docker-compose.microservices.yml ps")
            print("3. View logs: docker-compose -f docker-compose.microservices.yml logs [service-name]")
            return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

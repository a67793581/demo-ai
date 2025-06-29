#!/usr/bin/env python3
"""
Image validation functionality test script
"""

import asyncio
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ai_animation.utils import ImageValidator

async def test_image_validation():
    """Test image validation functionality"""
    
    print("🧪 Starting image validation test...\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Valid image URL",
            "url": "https://httpbin.org/image/png",
            "expected": True
        },
        {
            "name": "Invalid URL format",
            "url": "not-a-url",
            "expected": False
        },
        {
            "name": "Unsupported protocol",
            "url": "ftp://example.com/image.jpg",
            "expected": False
        },
        {
            "name": "Unsupported format",
            "url": "https://example.com/image.txt",
            "expected": False
        },
        {
            "name": "Empty URL",
            "url": "",
            "expected": False
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"URL: {test_case['url']}")
        
        try:
            is_valid, error_message = await ImageValidator.validate_image_url(test_case['url'])
            print(f"Result: {'✅ Pass' if is_valid else '❌ Fail'}")
            if not is_valid:
                print(f"Error message: {error_message}")
            
            if is_valid == test_case['expected']:
                print("✅ Test passed")
            else:
                print("❌ Test failed")
                
        except Exception as e:
            print(f"❌ Test exception: {str(e)}")
        
        print("-" * 50)
    
    print("🎉 Image validation test completed!")

if __name__ == "__main__":
    asyncio.run(test_image_validation()) 
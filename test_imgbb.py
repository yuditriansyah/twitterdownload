#!/usr/bin/env python3
"""
Test script to verify ImgBB upload functionality
"""
import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

def test_imgbb_upload():
    """Test if ImgBB upload works"""
    
    if not IMGBB_API_KEY or IMGBB_API_KEY == "your_imgbb_api_key_here":
        print("❌ IMGBB_API_KEY not set or still has placeholder value")
        print("   Please get your API key from https://api.imgbb.com/")
        print("   Then update your .env file with: IMGBB_API_KEY=your_actual_key")
        return False
    
    try:
        # Create a small test image (1x1 pixel PNG)
        test_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
        
        # Convert to base64
        image_base64 = base64.b64encode(test_data).decode('utf-8')
        
        # ImgBB API endpoint
        url = "https://api.imgbb.com/1/upload"
        
        # Prepare payload
        payload = {
            'key': IMGBB_API_KEY,
            'image': image_base64,
            'name': 'test_upload.png'
        }
        
        print("🧪 Testing ImgBB upload...")
        print(f"   API Key: {IMGBB_API_KEY[:10]}...{IMGBB_API_KEY[-5:]}")
        
        # Make request
        response = requests.post(url, data=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                image_url = result['data']['url']
                delete_url = result['data'].get('delete_url', 'N/A')
                print(f"✅ Upload successful!")
                print(f"   Image URL: {image_url}")
                print(f"   Delete URL: {delete_url}")
                print(f"   File size: {result['data']['size']} bytes")
                return True
            else:
                error_message = result.get('error', {}).get('message', 'Unknown error')
                print(f"❌ ImgBB API error: {error_message}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔗 Testing ImgBB API integration...")
    success = test_imgbb_upload()
    
    if success:
        print("\n✅ ImgBB test passed! The Twitter bot should work correctly.")
    else:
        print("\n❌ ImgBB test failed.")
        print("\n📝 To get an ImgBB API key:")
        print("   1. Go to https://api.imgbb.com/")
        print("   2. Sign up for a free account")
        print("   3. Get your API key")
        print("   4. Update your .env file: IMGBB_API_KEY=your_key")

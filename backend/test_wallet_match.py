"""Test wallet matching with actual request to backend"""
import requests
import sys

# Download the same pink wallet image that's in the static data
print("📷 Downloading pink wallet image...")
response = requests.get('https://images.unsplash.com/photo-1627123424574-724758594e93?w=500')
with open('test_wallet.jpg', 'wb') as f:
    f.write(response.content)

print("🚀 Sending to backend as LOST type...")

# Send to backend exactly like Flutter does
files = {'image': open('test_wallet.jpg', 'rb')}
data = {
    'title': 'Test Wallet',
    'description': 'Testing wallet match',
    'category': 'Wallet',
    'location': 'Test Location',
    'type': 'lost',  # LOST searches for FOUND
    'latitude': '0.0',
    'longitude': '0.0'
}

try:
    response = requests.post(
        'http://192.168.1.6:5000/api/posts/create-with-matching',
        files=files,
        data=data,
        timeout=60
    )
    
    print(f"\n📥 Response Status: {response.status_code}")
    print(f"📦 Response Body:")
    import json
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 201:
        result = response.json()
        if result['matches_count'] > 0:
            print(f"\n✅ SUCCESS! Found {result['matches_count']} matches:")
            for match in result['matches']:
                print(f"\n  🎯 Match:")
                print(f"     Title: {match['title']}")
                print(f"     Similarity: {match['match_percentage']}%")
                print(f"     Location: {match['location']}")
                print(f"     Image: {match['image_url'][:60]}...")
        else:
            print(f"\n❌ FAILED: No matches found!")
            print("   This means the search returned empty results")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

import os
if os.path.exists('test_wallet.jpg'):
    os.remove('test_wallet.jpg')

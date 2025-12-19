"""
Seed Database with Test Posts
=============================
This script downloads images from the web and uploads them to the backend
to create test posts for AI matching.

Run this AFTER starting the backend: python app.py
Then run: python seed_database.py
"""

import requests
import os
import time

# Backend URL
BASE_URL = 'http://localhost:5000'

# Test posts with real Unsplash images
# These match the images shown in the Flutter home screen
TEST_POSTS = [
    {
        'title': 'Pink Quilted Wallet',
        'description': 'Found this beautiful pink wallet in Central Park near the fountain',
        'category': 'Wallet',
        'location': 'Central Park, NY',
        'type': 'found',
        'latitude': '40.7829',
        'longitude': '-73.9654',
        'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=500',
    },
    {
        'title': 'Brown Teddy Bear',
        'description': 'Lost my child\'s favorite teddy bear at the library reading area',
        'category': 'Other',
        'location': 'Main Street Library',
        'type': 'lost',
        'latitude': '40.7580',
        'longitude': '-73.9855',
        'image_url': 'https://images.unsplash.com/photo-1519897831810-a9a01aceccd1?w=500',
    },
    {
        'title': 'Leather Travel Pouch',
        'description': 'Found this brown leather bag at the airport terminal near gate B4',
        'category': 'Bag',
        'location': 'JFK Airport Terminal 4',
        'type': 'found',
        'latitude': '40.6413',
        'longitude': '-73.7781',
        'image_url': 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=500',
    },
    {
        'title': 'Blue Backpack',
        'description': 'Found this blue backpack at the gym locker area',
        'category': 'Bag',
        'location': 'City Fitness Gym',
        'type': 'found',
        'latitude': '40.7484',
        'longitude': '-73.9857',
        'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500',
    },
    {
        'title': 'iPhone with Red Case',
        'description': 'Lost my iPhone 13 with a red silicone case at the coffee shop',
        'category': 'Phone',
        'location': 'Starbucks Times Square',
        'type': 'lost',
        'latitude': '40.7580',
        'longitude': '-73.9855',
        'image_url': 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=500',
    },
]


def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f'{BASE_URL}/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running!")
            print(f"   🤖 AI Model: {data.get('ai_model', 'Unknown')}")
            print(f"   💻 Device: {data.get('device', 'Unknown')}")
            return True
    except requests.exceptions.ConnectionError:
        pass
    
    print("❌ Backend is not running!")
    print("   Start it with: python app.py")
    return False


def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
    return False


def create_post(post_data, image_path):
    """Upload post to backend"""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'title': post_data['title'],
                'description': post_data['description'],
                'category': post_data['category'],
                'location': post_data['location'],
                'type': post_data['type'],
                'latitude': post_data['latitude'],
                'longitude': post_data['longitude'],
            }
            
            response = requests.post(
                f'{BASE_URL}/api/posts/create-with-matching',
                files=files,
                data=data,
                timeout=60  # AI processing can take time
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                return None
                
    except Exception as e:
        print(f"   ❌ Upload failed: {e}")
        return None


def seed_database():
    """Main seeding function"""
    print("\n" + "=" * 60)
    print("🌱 SEEDING DATABASE WITH TEST POSTS")
    print("=" * 60)
    
    if not check_backend():
        return
    
    print("\n📥 Downloading and uploading images...\n")
    
    created_posts = []
    
    for i, post in enumerate(TEST_POSTS, 1):
        print(f"[{i}/{len(TEST_POSTS)}] {post['title']} ({post['type'].upper()})")
        
        # Download image
        filename = f"temp_seed_{i}.jpg"
        print(f"   📷 Downloading image...")
        
        if not download_image(post['image_url'], filename):
            print(f"   ⏭️  Skipping...")
            continue
        
        # Upload to backend
        print(f"   🚀 Uploading to backend...")
        print(f"   🤖 AI processing (may take 2-5 seconds)...")
        
        result = create_post(post, filename)
        
        if result:
            created_posts.append({
                'id': result['post_id'],
                'title': post['title'],
                'type': post['type'],
                'matches': result['matches_count']
            })
            print(f"   ✅ Created! Post ID: {result['post_id'][:8]}...")
            print(f"   📊 Matches found: {result['matches_count']}")
        
        # Clean up temp file
        if os.path.exists(filename):
            os.remove(filename)
        
        print()
        time.sleep(1)  # Small delay between uploads
    
    # Summary
    print("=" * 60)
    print("📊 SEEDING COMPLETE!")
    print("=" * 60)
    print(f"\n✅ Created {len(created_posts)} posts:\n")
    
    for p in created_posts:
        type_emoji = "🔴" if p['type'] == 'lost' else "🟢"
        print(f"   {type_emoji} {p['title']} ({p['type'].upper()}) - {p['matches']} matches")
    
    print(f"\n📋 View all posts: {BASE_URL}/api/posts")
    print(f"🏥 Health check: {BASE_URL}/api/health")
    
    # Show matching instructions
    print("\n" + "=" * 60)
    print("🎯 HOW TO TEST AI MATCHING:")
    print("=" * 60)
    print("""
In the Flutter app, create a new post with:

1️⃣ TO MATCH THE PINK WALLET (Found):
   - Upload similar pink/quilted wallet image
   - Type: LOST
   - Category: Wallet
   → Should match with ~80-95% similarity!

2️⃣ TO MATCH THE TEDDY BEAR (Lost):
   - Upload similar teddy bear/stuffed toy image
   - Type: FOUND
   - Category: Other
   → Should match with ~75-90% similarity!

3️⃣ TO MATCH THE LEATHER BAG (Found):
   - Upload similar brown leather bag image
   - Type: LOST
   - Category: Bag
   → Should match with ~70-85% similarity!

4️⃣ TO MATCH THE BLUE BACKPACK (Found):
   - Upload similar blue backpack image
   - Type: LOST
   - Category: Bag
   → Should match with ~80-95% similarity!

5️⃣ TO MATCH THE IPHONE (Lost):
   - Upload similar iPhone/phone image
   - Type: FOUND
   - Category: Phone
   → Should match with ~75-90% similarity!

Remember: 
- Lost searches for Found (and vice versa)
- Same/similar images = high match %
- Different images = low/no match
""")
    print("=" * 60)


if __name__ == '__main__':
    seed_database()

"""
Seed Vector Database with Static Posts
=======================================
Creates embeddings for the 5 static posts using fixed IDs
"""

import sys
import os
import uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService
from services.vector_db_service import VectorDBService
import requests
from PIL import Image
import io

# Initialize services
print("🚀 Initializing AI and Vector DB services...")
ai_service = AIService()
vector_db = VectorDBService()

# Static posts with Unsplash images - use UUID strings
STATIC_POSTS = [
    {
        'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, 'pink-wallet-001')),
        'key': 'pink-wallet-001',
        'title': 'Pink Quilted Wallet',
        'category': 'Wallet',
        'location': 'Central Park, NY',
        'type': 'found',
        'image_url': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=500',
    },
    {
        'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, 'teddy-bear-002')),
        'key': 'teddy-bear-002',
        'title': 'Brown Teddy Bear',
        'category': 'Other',
        'location': 'Main Street Library',
        'type': 'lost',
        'image_url': 'https://images.unsplash.com/photo-1519897831810-a9a01aceccd1?w=500',
    },
    {
        'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, 'leather-bag-003')),
        'key': 'leather-bag-003',
        'title': 'Leather Travel Pouch',
        'category': 'Bag',
        'location': 'JFK Airport Terminal 4',
        'type': 'found',
        'image_url': 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=500',
    },
    {
        'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, 'blue-backpack-004')),
        'key': 'blue-backpack-004',
        'title': 'Blue Backpack',
        'category': 'Bag',
        'location': 'City Fitness Gym',
        'type': 'found',
        'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500',
    },
    {
        'id': str(uuid.uuid5(uuid.NAMESPACE_DNS, 'iphone-red-005')),
        'key': 'iphone-red-005',
        'title': 'iPhone with Red Case',
        'category': 'Phone',
        'location': 'Starbucks Times Square',
        'type': 'lost',
        'image_url': 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=500',
    },
]

print("\n" + "="*60)
print("🌱 SEEDING VECTOR DB WITH STATIC POSTS")
print("="*60 + "\n")

for i, post in enumerate(STATIC_POSTS, 1):
    print(f"[{i}/{len(STATIC_POSTS)}] {post['title']} ({post['type'].upper()})")
    
    try:
        # Download image
        print(f"   📷 Downloading from Unsplash...")
        response = requests.get(post['image_url'], timeout=30)
        
        if response.status_code != 200:
            print(f"   ❌ Failed to download image")
            continue
        
        # Save temporarily
        temp_file = f"temp_{post['id']}.jpg"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        # Generate embedding
        print(f"   🤖 Generating CLIP embedding...")
        embedding = ai_service.generate_embedding(temp_file)
        print(f"   ✅ Embedding: {len(embedding)} dimensions")
        
        # Store in vector DB
        print(f"   💾 Storing in vector database...")
        vector_db.upsert_embedding(
            point_id=post['id'],  # UUID string
            embedding=embedding,
            payload={
                'post_id': post['key'],  # Use key for post_db lookup
                'post_type': post['type'],
                'category': post['category'],
                'location': post['location'],
                'title': post['title'],
                'image_url': post['image_url']
            }
        )
        print(f"   ✅ Stored with vector ID: {post['id'][:8]}...")
        print(f"   ✅ Post lookup key: {post['key']}")
        
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()

# Show results
print("="*60)
print("📊 SEEDING COMPLETE!")
print("="*60)
print(f"\n✅ 5 static posts seeded in vector database")
print(f"🔍 Posts can now be matched via /api/posts/create-with-matching")
print(f"\n💡 Test by uploading a wallet photo as 'LOST' to match the pink wallet")
print("="*60 + "\n")

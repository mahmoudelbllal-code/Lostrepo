"""Test vector search directly"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService
from services.vector_db_service import VectorDBService

print("🚀 Initializing services...")
ai_service = AIService()
vector_db = VectorDBService()

# Download and test with wallet image
import requests
print("\n📷 Downloading test wallet image...")
response = requests.get('https://images.unsplash.com/photo-1627123424574-724758594e93?w=500')
with open('test_wallet.jpg', 'wb') as f:
    f.write(response.content)

print("🤖 Generating embedding...")
embedding = ai_service.generate_embedding('test_wallet.jpg')
print(f"✅ Embedding: {len(embedding)} dimensions")

# Test search as LOST (should find FOUND wallets)
print("\n🔍 Searching as LOST (looking for FOUND)...")
matches = vector_db.search_similar(
    embedding=embedding,
    post_type='lost',  # Searches for opposite = 'found'
    top_k=10,
    min_similarity=0.60
)

print(f"\n📊 Found {len(matches)} matches:")
for match in matches:
    print(f"\n  ✅ Match:")
    print(f"     Post ID: {match['post_id']}")
    print(f"     Similarity: {match['similarity']:.2%}")
    print(f"     Payload: {match['payload']}")

# Also test as FOUND
print("\n\n🔍 Searching as FOUND (looking for LOST)...")
matches2 = vector_db.search_similar(
    embedding=embedding,
    post_type='found',
    top_k=10,
    min_similarity=0.60
)

print(f"\n📊 Found {len(matches2)} matches:")
for match in matches2:
    print(f"\n  ✅ Match:")
    print(f"     Post ID: {match['post_id']}")
    print(f"     Similarity: {match['similarity']:.2%}")
    print(f"     Payload: {match['payload']}")

os.remove('test_wallet.jpg')
print("\n✅ Test complete!")

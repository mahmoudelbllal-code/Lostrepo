"""
Check what's in the Qdrant Cloud database
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')

client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

print("=" * 60)
print("🔍 Checking Cloud Database Contents")
print("=" * 60)

# Get all points
points, _ = client.scroll(
    collection_name="lost_found_items",
    limit=20,
    with_payload=True,
    with_vectors=False
)

print(f"\n📊 Total points: {len(points)}")
print("\n" + "=" * 60)

for i, point in enumerate(points, 1):
    print(f"\n{i}. Point ID: {point.id}")
    print(f"   Post Type: {point.payload.get('post_type', 'N/A')}")
    print(f"   Category: {point.payload.get('category', 'N/A')}")
    print(f"   Title: {point.payload.get('title', 'N/A')}")
    print(f"   Image URL: {point.payload.get('image_url', 'N/A')}")

print("\n" + "=" * 60)

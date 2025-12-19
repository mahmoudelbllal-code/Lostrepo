"""
Migrate Local Qdrant Data to Cloud
===================================
This script migrates all embeddings and posts from local Qdrant to Qdrant Cloud
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔄 Migrating Local Qdrant to Cloud")
print("=" * 60)

# Get cloud credentials
qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')

if not qdrant_url or not qdrant_api_key:
    print("❌ Error: Cloud credentials not found in .env file")
    exit(1)

try:
    # Connect to local Qdrant
    print("\n📂 Connecting to local Qdrant...")
    local_client = QdrantClient(path="./qdrant_data")
    
    # Connect to cloud Qdrant
    print("☁️  Connecting to Qdrant Cloud...")
    cloud_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    
    collection_name = "lost_found_items"
    
    # Check if local collection exists
    local_collections = local_client.get_collections().collections
    local_collection_names = [col.name for col in local_collections]
    
    if collection_name not in local_collection_names:
        print(f"\n❌ Local collection '{collection_name}' not found")
        print("Nothing to migrate!")
        exit(0)
    
    # Get local collection info
    local_info = local_client.get_collection(collection_name)
    print(f"\n📊 Local collection info:")
    print(f"   Points: {local_info.points_count}")
    
    if local_info.points_count == 0:
        print("\n⚠️  Local collection is empty - nothing to migrate")
        exit(0)
    
    # Check if cloud collection exists
    cloud_collections = cloud_client.get_collections().collections
    cloud_collection_names = [col.name for col in cloud_collections]
    
    if collection_name not in cloud_collection_names:
        print(f"\n🆕 Creating collection in cloud...")
        from qdrant_client.models import Distance, VectorParams
        cloud_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=512,
                distance=Distance.COSINE
            )
        )
        print("✅ Collection created in cloud")
    
    # Get all points from local
    print(f"\n📥 Fetching all points from local database...")
    local_points, _ = local_client.scroll(
        collection_name=collection_name,
        limit=1000,
        with_payload=True,
        with_vectors=True
    )
    
    print(f"✅ Retrieved {len(local_points)} points")
    
    if len(local_points) == 0:
        print("\n⚠️  No points to migrate")
        exit(0)
    
    # Upload to cloud
    print(f"\n☁️  Uploading {len(local_points)} points to cloud...")
    from qdrant_client.models import PointStruct
    
    cloud_points = []
    for point in local_points:
        cloud_points.append(
            PointStruct(
                id=point.id,
                vector=point.vector,
                payload=point.payload
            )
        )
    
    cloud_client.upsert(
        collection_name=collection_name,
        points=cloud_points
    )
    
    print("✅ Upload complete!")
    
    # Verify
    cloud_info = cloud_client.get_collection(collection_name)
    print(f"\n📊 Cloud collection info:")
    print(f"   Points: {cloud_info.points_count}")
    
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print(f"\n✨ {local_info.points_count} embeddings migrated to cloud")
    print("🔗 Your data is now in Qdrant Cloud")
    
except Exception as e:
    print(f"\n❌ Migration failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

"""
Test Qdrant Cloud Connection
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

print("=" * 60)
print("🧪 Testing Qdrant Cloud Connection")
print("=" * 60)

# Get credentials
qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')

if not qdrant_url or not qdrant_api_key:
    print("❌ Error: QDRANT_URL and QDRANT_API_KEY not found in .env file")
    print("\nCreate a .env file with:")
    print("QDRANT_URL=your-cluster-url")
    print("QDRANT_API_KEY=your-api-key")
    exit(1)

print(f"📍 URL: {qdrant_url}")
print(f"🔑 API Key: {qdrant_api_key[:20]}...")

try:
    # Connect to Qdrant Cloud
    print("\n🔌 Connecting to Qdrant Cloud...")
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )
    
    # Get collections
    print("📊 Fetching collections...")
    collections = client.get_collections()
    
    print("\n✅ Connection successful!")
    print(f"\n📦 Collections found: {len(collections.collections)}")
    
    if collections.collections:
        for collection in collections.collections:
            print(f"   - {collection.name}")
            
            # Get collection info
            info = client.get_collection(collection.name)
            print(f"     Points: {info.points_count}")
    else:
        print("   No collections found (empty database)")
    
    print("\n" + "=" * 60)
    print("✅ Qdrant Cloud is ready to use!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nPlease check:")
    print("1. URL is correct")
    print("2. API key is valid")
    print("3. Internet connection is working")
    exit(1)

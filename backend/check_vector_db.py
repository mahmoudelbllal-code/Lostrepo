"""Check what's actually in vector DB"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.vector_db_service import VectorDBService

vdb = VectorDBService()
points = vdb.client.scroll(collection_name='lost_found_items', limit=10)[0]

print(f"\n{'='*60}")
print(f"VECTOR DB CONTENTS")
print(f"{'='*60}\n")

for p in points:
    print(f"Vector ID: {p.id}")
    print(f"  Post ID: {p.payload.get('post_id')}")
    print(f"  Category: [{p.payload.get('category')}]")
    print(f"  Post Type: {p.payload.get('post_type')}")
    print(f"  Title: {p.payload.get('title')}")
    print()

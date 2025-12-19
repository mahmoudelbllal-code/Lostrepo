"""
Vector Database Service - Handles embedding storage and similarity search using Qdrant
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue


class VectorDBService:
    def __init__(self):
        """Initialize Qdrant client (local mode)"""
        self.collection_name = "lost_found_items"
        
        # Initialize Qdrant in local mode (file-based storage)
        self.client = QdrantClient(path="./qdrant_data")
        
        # Create collection if it doesn't exist
        self._create_collection_if_not_exists()
        
        print(f"✅ Qdrant Vector DB initialized (collection: {self.collection_name})")
    
    def _create_collection_if_not_exists(self):
        """Create collection with proper configuration"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=512,  # CLIP ViT-B/32 embedding size
                        distance=Distance.COSINE  # Cosine similarity
                    )
                )
                print(f"✅ Created new collection: {self.collection_name}")
            else:
                print(f"✅ Collection already exists: {self.collection_name}")
                
        except Exception as e:
            raise Exception(f"Failed to create collection: {str(e)}")
    
    def upsert_embedding(self, point_id, embedding, payload):
        """
        Store or update an embedding in the vector database
        
        Args:
            point_id (str): Unique identifier for the point
            embedding (list): 512-dimensional embedding vector
            payload (dict): Metadata to store with the embedding
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )
                ]
            )
        except Exception as e:
            raise Exception(f"Failed to upsert embedding: {str(e)}")
    
    def search_similar(self, embedding, post_type, top_k=10, min_similarity=0.60):
        """
        Search for similar items in the vector database
        
        Args:
            embedding (list): Query embedding vector
            post_type (str): Type of the query post ('lost' or 'found')
            top_k (int): Number of results to return
            min_similarity (float): Minimum similarity threshold (0-1)
        
        Returns:
            list: List of matching posts with similarity scores
        """
        try:
            # Search for opposite type (lost searches found, found searches lost)
            opposite_type = 'found' if post_type == 'lost' else 'lost'
            
            # Create filter for post type
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="post_type",
                        match=MatchValue(value=opposite_type)
                    )
                ]
            )
            
            # Perform search using query_points (newer Qdrant API)
            try:
                # Use the correct method based on Qdrant version
                search_results = self.client.query_points(
                    collection_name=self.collection_name,
                    query=embedding,
                    limit=top_k,
                    query_filter=search_filter,
                    score_threshold=min_similarity,
                    with_payload=True
                ).points
            except AttributeError:
                # Fallback for older versions - use search method
                search_results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=embedding,
                    limit=top_k,
                    query_filter=search_filter,
                    score_threshold=min_similarity,
                    with_payload=True
                )
            
            # Format results
            matches = []
            for result in search_results:
                matches.append({
                    'post_id': result.id,
                    'similarity': result.score,
                    'payload': result.payload
                })
            
            return matches
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
    
    def delete_embedding(self, point_id):
        """Delete an embedding from the vector database"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[point_id]
            )
        except Exception as e:
            raise Exception(f"Failed to delete embedding: {str(e)}")
    
    def get_collection_info(self):
        """Get information about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                'name': self.collection_name,
                'vectors_count': info.vectors_count,
                'points_count': info.points_count,
                'status': info.status
            }
        except Exception as e:
            return {'error': str(e)}

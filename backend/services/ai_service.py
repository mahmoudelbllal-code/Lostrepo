"""
AI Service - Handles image embedding generation using CLIP model
"""

import torch
from PIL import Image
import clip


class AIService:
    def __init__(self):
        """Initialize CLIP model for image embeddings"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🤖 Loading CLIP model on {self.device}...")
        
        # Load pretrained CLIP model
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.model.eval()  # Set to evaluation mode
        
        print(f"✅ CLIP model loaded successfully")
    
    def generate_embedding(self, image_path):
        """
        Generate 512-dimensional embedding vector for an image
        
        Args:
            image_path (str): Path to image file
        
        Returns:
            list: 512-dimensional embedding vector
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
            
            # Generate embedding
            with torch.no_grad():
                image_features = self.model.encode_image(image_input)
                # Normalize to unit length for cosine similarity
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            # Convert to list
            embedding = image_features.cpu().numpy().flatten().tolist()
            
            return embedding
            
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
    
    def compute_similarity(self, embedding1, embedding2):
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1 (list): First embedding vector
            embedding2 (list): Second embedding vector
        
        Returns:
            float: Similarity score (0-1)
        """
        import numpy as np
        
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        return float(similarity)

    def predict_category(self, image_embedding, categories):
        """
        Predict the category of an image using Zero-Shot classification
        
        Args:
            image_embedding (list): Image embedding vector
            categories (list): List of category names (e.g. ['Wallet', 'Phone'])
            
        Returns:
            tuple: (best_category, confidence_score)
        """
        try:
            # Tokenize categories
            # Use 'a photo of a X' prompt engineering for better accuracy
            text_inputs = torch.cat([clip.tokenize(f"a photo of a {c}") for c in categories]).to(self.device)
            
            # Encode text
            with torch.no_grad():
                text_features = self.model.encode_text(text_inputs)
                text_features /= text_features.norm(dim=-1, keepdim=True)
            
            # Convert image embedding back to tensor if needed
            if isinstance(image_embedding, list):
                image_features = torch.tensor(image_embedding).to(self.device)
            else:
                image_features = image_embedding
                
            # Ensure shape is (1, 512)
            if len(image_features.shape) == 1:
                image_features = image_features.unsqueeze(0)
            
            # Compute similarity (dot product since normalized)
            # Softmax to get probabilities
            similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            values, indices = similarity[0].topk(1)
            
            best_idx = indices[0].item()
            confidence = values[0].item()
            
            return categories[best_idx], confidence
            
        except Exception as e:
            print(f"⚠️ Classification error: {e}")
            return categories[0], 0.0

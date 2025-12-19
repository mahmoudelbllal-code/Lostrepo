"""
Storage Service - Handles image upload to Firebase or local storage
"""

import os
import shutil


class StorageService:
    def __init__(self):
        """Initialize storage service"""
        self.use_firebase = False  # Set to True when Firebase is configured
        self.local_storage_path = 'temp_uploads'
        
        # Create local storage directory if it doesn't exist
        os.makedirs(self.local_storage_path, exist_ok=True)
        
        if self.use_firebase:
            try:
                import firebase_admin
                from firebase_admin import credentials, storage
                
                # Initialize Firebase
                if not firebase_admin._apps:
                    cred = credentials.Certificate('firebase-credentials.json')
                    firebase_admin.initialize_app(cred, {
                        'storageBucket': 'your-project-id.appspot.com'
                    })
                
                self.bucket = storage.bucket()
                print("✅ Firebase Storage initialized")
            except Exception as e:
                print(f"⚠️  Firebase not configured, using local storage: {e}")
                self.use_firebase = False
    
    def upload_image(self, file_path, post_id):
        """
        Upload image to Firebase Storage or local storage
        
        Args:
            file_path (str): Path to local file
            post_id (str): Unique post ID
        
        Returns:
            str: URL of uploaded image
        """
        if self.use_firebase:
            return self._upload_to_firebase(file_path, post_id)
        else:
            return self._upload_to_local(file_path, post_id)
    
    def _upload_to_firebase(self, file_path, post_id):
        """Upload to Firebase Storage"""
        try:
            filename = os.path.basename(file_path)
            blob_path = f"posts/{post_id}/{filename}"
            
            blob = self.bucket.blob(blob_path)
            blob.upload_from_filename(file_path)
            blob.make_public()
            
            return blob.public_url
            
        except Exception as e:
            raise Exception(f"Firebase upload failed: {str(e)}")
    
    def _upload_to_local(self, file_path, post_id):
        """Save to local storage and return URL"""
        try:
            filename = os.path.basename(file_path)
            
            # Copy to permanent location
            destination = os.path.join(self.local_storage_path, filename)
            if file_path != destination:
                shutil.copy2(file_path, destination)
            
            # Return local URL
            return f"http://localhost:5000/uploads/{filename}"
            
        except Exception as e:
            raise Exception(f"Local storage failed: {str(e)}")
    
    def delete_image(self, image_url):
        """Delete image from storage"""
        if self.use_firebase:
            # Extract blob path from URL and delete
            pass
        else:
            # Delete from local storage
            try:
                filename = image_url.split('/')[-1]
                file_path = os.path.join(self.local_storage_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete image: {e}")

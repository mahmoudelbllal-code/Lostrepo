from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

from services.ai_service import AIService
from services.storage_service import StorageService
from services.vector_db_service import VectorDBService

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize services
ai_service = AIService()
storage_service = StorageService()
vector_db_service = VectorDBService()

# In-memory storage (replace with MongoDB later)
posts_db = {}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Flask backend is running',
        'ai_model': 'CLIP ViT-B/32',
        'device': ai_service.device,
        'vector_db': 'Qdrant (local)',
        'total_posts': len(posts_db)
    }), 200


@app.route('/api/posts/create-with-matching', methods=['POST'])
def create_post_with_matching():
    """
    Create a new post and find matching items using AI
    
    Form Data:
        - image (file): Image of lost/found item
        - title (string): Item title
        - description (string): Description
        - category (string): Category (Wallet, Phone, Bag, etc.)
        - location (string): Location text
        - type (string): "lost" or "found"
        - latitude (float, optional): Latitude coordinate
        - longitude (float, optional): Longitude coordinate
    
    Returns:
        JSON with post_id, matches_count, and matches array
    """
    try:
        print("\n" + "="*60)
        print("📥 Received new post creation request")
        print("="*60)
        
        # Validate image file
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, webp'}), 400
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        post_type = request.form.get('type', 'lost').lower()
        
        # Validate required fields
        if not all([title, description, category, location]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if post_type not in ['lost', 'found']:
            return jsonify({'error': 'Type must be "lost" or "found"'}), 400
        
        # Get coordinates
        try:
            latitude = float(request.form.get('latitude', 0.0))
            longitude = float(request.form.get('longitude', 0.0))
        except ValueError:
            latitude = 0.0
            longitude = 0.0
        
        # Generate unique ID
        post_id = str(uuid.uuid4())
        filename = secure_filename(f"{post_id}_{file.filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        print(f"📝 Post Details:")
        print(f"   Title: {title}")
        print(f"   Type: {post_type}")
        print(f"   Category: {category}")
        print(f"   Location: {location}")
        
        # Save file temporarily
        file.save(file_path)
        print(f"💾 Saved temporary file: {filename}")
        
        # Step 1: Generate AI embedding
        print(f"🤖 Generating AI embedding using CLIP...")
        embedding = ai_service.generate_embedding(file_path)
        print(f"✅ Embedding generated: {len(embedding)} dimensions")
        
        # Step 2: Upload to storage
        print(f"☁️  Uploading image to storage...")
        image_url = storage_service.upload_image(file_path, post_id)
        print(f"✅ Image uploaded: {image_url[:50]}...")
        
        # Step 3: Create post object
        post_data = {
            'id': post_id,
            'title': title,
            'description': description,
            'category': category,
            'location': location,
            'post_type': post_type,
            'image_url': image_url,
            'coordinates': {
                'latitude': latitude,
                'longitude': longitude
            },
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Store in database
        posts_db[post_id] = post_data
        print(f"💾 Post saved to database")
        
        # Step 4: Store embedding in vector database
        print(f"🔍 Storing embedding in vector database...")
        vector_db_service.upsert_embedding(
            point_id=post_id,
            embedding=embedding,
            payload={
                'post_id': post_id,
                'post_type': post_type,
                'category': category,
                'location': location,
                'title': title,
                'image_url': image_url
            }
        )
        print(f"✅ Embedding stored in vector DB")
        
        # Step 5: Search for matches
        print(f"🔎 Searching for similar items...")
        matches = vector_db_service.search_similar(
            embedding=embedding,
            post_type=post_type,
            top_k=10,
            min_similarity=0.60  # 60% minimum similarity
        )
        
        # Step 6: Format matches with full post details
        matching_results = []
        for match in matches:
            match_post = posts_db.get(match['post_id'])
            if match_post:
                # Calculate time ago
                created_at = datetime.fromisoformat(match_post['created_at'])
                time_diff = datetime.now() - created_at
                
                if time_diff.days > 0:
                    time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
                elif time_diff.seconds >= 3600:
                    hours = time_diff.seconds // 3600
                    time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
                else:
                    minutes = time_diff.seconds // 60
                    time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                
                matching_results.append({
                    'id': match['post_id'],
                    'title': match_post['title'],
                    'description': match_post['description'],
                    'category': match_post['category'],
                    'location': match_post['location'],
                    'distance': '2km away',  # TODO: Calculate real distance
                    'image_url': match_post['image_url'],
                    'post_type': match_post['post_type'],
                    'match_percentage': round(match['similarity'] * 100, 1),
                    'time_ago': time_ago,
                    'finder_name': 'User',  # TODO: Add user system
                    'is_verified': False
                })
        
        print(f"✨ Found {len(matching_results)} matches")
        print("="*60 + "\n")
        
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({
            'success': True,
            'post_id': post_id,
            'message': 'Post created successfully',
            'matches_count': len(matching_results),
            'matches': matching_results
        }), 201
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get post details by ID"""
    post = posts_db.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post), 200
@app.route('/', methods=['GET'])
def start():
    """Base endpoint to verify API is running"""
    return jsonify({
        'message': 'Lost & Found AI Backend is running',
        'endpoints': {
            '/api/health': 'Health check',
            '/api/posts/create-with-matching': 'Create post with AI matching (POST)',
            '/api/posts/<post_id>': 'Get post details by ID (GET)',
            '/api/posts': 'Get all posts with optional filters (GET)'
        }
    }), 200
@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    """Get all posts with optional filters"""
    post_type = request.args.get('type')  # lost, found
    category = request.args.get('category')
    
    posts = list(posts_db.values())
    
    # Apply filters
    if post_type:
        posts = [p for p in posts if p['post_type'] == post_type.lower()]
    if category:
        posts = [p for p in posts if p['category'].lower() == category.lower()]
    
    # Sort by created_at (newest first)
    posts.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({
        'posts': posts,
        'count': len(posts)
    }), 200


@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files for local testing"""
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Lost & Found AI Backend")
    print("="*60)
    print(f"📍 Server: http://localhost:5000")
    print(f"🤖 AI Model: CLIP ViT-B/32")
    print(f"💻 Device: {ai_service.device}")
    print(f"🗄️  Vector DB: Qdrant (local)")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

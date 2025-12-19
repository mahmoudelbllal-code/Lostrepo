/// Post Entity - Domain Layer
class Post {
  final String id;
  final String userId;
  final String title;
  final String description;
  final String category;
  final String postType; // 'lost' or 'found'
  final String imageUrl;
  final String? location;
  final DateTime createdAt;
  final DateTime? updatedAt;

  const Post({
    required this.id,
    required this.userId,
    required this.title,
    required this.description,
    required this.category,
    required this.postType,
    required this.imageUrl,
    this.location,
    required this.createdAt,
    this.updatedAt,
  });

  Post copyWith({
    String? id,
    String? userId,
    String? title,
    String? description,
    String? category,
    String? postType,
    String? imageUrl,
    String? location,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Post(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      title: title ?? this.title,
      description: description ?? this.description,
      category: category ?? this.category,
      postType: postType ?? this.postType,
      imageUrl: imageUrl ?? this.imageUrl,
      location: location ?? this.location,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}

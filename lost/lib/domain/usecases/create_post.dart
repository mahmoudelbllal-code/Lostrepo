import '../entities/post.dart';
import '../repositories/post_repository.dart';
import '../../core/errors/failures.dart';

/// Use Case: Create a new post (Lost or Found)
class CreatePostUseCase {
  final PostRepository repository;

  CreatePostUseCase(this.repository);

  Future<Either<Failure, Post>> call({
    required String title,
    required String description,
    required String category,
    required String postType,
    required String imagePath,
    String? location,
  }) async {
    return await repository.createPost(
      title: title,
      description: description,
      category: category,
      postType: postType,
      imagePath: imagePath,
      location: location,
    );
  }
}

import '../entities/post.dart';
import '../repositories/post_repository.dart';
import '../../core/errors/failures.dart';

/// Use Case: Get all posts
class GetAllPostsUseCase {
  final PostRepository repository;

  GetAllPostsUseCase(this.repository);

  Future<Either<Failure, List<Post>>> call() async {
    return await repository.getAllPosts();
  }
}

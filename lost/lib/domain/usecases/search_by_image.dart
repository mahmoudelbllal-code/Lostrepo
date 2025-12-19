import '../entities/search_result.dart';
import '../repositories/post_repository.dart';
import '../../core/errors/failures.dart';

/// Use Case: Search posts by uploading an image
class SearchByImageUseCase {
  final PostRepository repository;

  SearchByImageUseCase(this.repository);

  Future<Either<Failure, List<SearchResult>>> call(String imagePath) async {
    return await repository.searchByImage(imagePath);
  }
}

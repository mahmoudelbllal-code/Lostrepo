import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/errors/exceptions.dart';
import '../models/post_model.dart';
import '../models/search_result_model.dart';

/// Remote Data Source for Post operations
abstract class PostRemoteDataSource {
  Future<PostModel> createPost({
    required String title,
    required String description,
    required String category,
    required String postType,
    required String imagePath,
    String? location,
  });

  Future<PostModel> getPostById(String postId);
  Future<List<PostModel>> getAllPosts();
  Future<List<PostModel>> getUserPosts(String userId);
  Future<List<SearchResultModel>> searchByImage(String imagePath);
  Future<PostModel> updatePost(PostModel post);
  Future<void> deletePost(String postId);
}

/// Implementation of PostRemoteDataSource
class PostRemoteDataSourceImpl implements PostRemoteDataSource {
  final ApiClient apiClient;

  PostRemoteDataSourceImpl({required this.apiClient});

  @override
  Future<PostModel> createPost({
    required String title,
    required String description,
    required String category,
    required String postType,
    required String imagePath,
    String? location,
  }) async {
    try {
      // First upload the image
      final uploadResponse = await apiClient.postMultipart(
        ApiConstants.uploadEndpoint,
        filePath: imagePath,
      );

      final imageUrl = uploadResponse['image_url'] as String;

      // Then create the post
      final response = await apiClient.post(
        ApiConstants.postsEndpoint,
        body: {
          'title': title,
          'description': description,
          'category': category,
          'post_type': postType,
          'image_url': imageUrl,
          if (location != null) 'location': location,
        },
      );

      return PostModel.fromJson(response);
    } catch (e) {
      throw ServerException('Failed to create post: $e');
    }
  }

  @override
  Future<PostModel> getPostById(String postId) async {
    try {
      final response = await apiClient.get(
        '${ApiConstants.postsEndpoint}/$postId',
      );
      return PostModel.fromJson(response);
    } catch (e) {
      throw ServerException('Failed to get post: $e');
    }
  }

  @override
  Future<List<PostModel>> getAllPosts() async {
    try {
      final response = await apiClient.get(ApiConstants.postsEndpoint);
      final List<dynamic> postsJson = response['posts'] as List<dynamic>;
      return postsJson
          .map((json) => PostModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      throw ServerException('Failed to get posts: $e');
    }
  }

  @override
  Future<List<PostModel>> getUserPosts(String userId) async {
    try {
      final response = await apiClient.get(
        '${ApiConstants.postsEndpoint}?user_id=$userId',
      );
      final List<dynamic> postsJson = response['posts'] as List<dynamic>;
      return postsJson
          .map((json) => PostModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      throw ServerException('Failed to get user posts: $e');
    }
  }

  @override
  Future<List<SearchResultModel>> searchByImage(String imagePath) async {
    try {
      final response = await apiClient.postMultipart(
        ApiConstants.searchEndpoint,
        filePath: imagePath,
      );

      final List<dynamic> resultsJson = response['results'] as List<dynamic>;
      return resultsJson
          .map(
            (json) => SearchResultModel.fromJson(json as Map<String, dynamic>),
          )
          .toList();
    } catch (e) {
      throw ServerException('Failed to search by image: $e');
    }
  }

  @override
  Future<PostModel> updatePost(PostModel post) async {
    try {
      final response = await apiClient.put(
        '${ApiConstants.postsEndpoint}/${post.id}',
        body: post.toJson(),
      );
      return PostModel.fromJson(response);
    } catch (e) {
      throw ServerException('Failed to update post: $e');
    }
  }

  @override
  Future<void> deletePost(String postId) async {
    try {
      await apiClient.delete('${ApiConstants.postsEndpoint}/$postId');
    } catch (e) {
      throw ServerException('Failed to delete post: $e');
    }
  }
}

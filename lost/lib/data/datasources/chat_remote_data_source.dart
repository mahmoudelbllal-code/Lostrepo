import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/errors/exceptions.dart';
import '../models/chat_message_model.dart';

/// Remote Data Source for Chat operations
abstract class ChatRemoteDataSource {
  Future<String> startChat({
    required String userId1,
    required String userId2,
    required String postId,
  });

  Future<List<ChatMessageModel>> getChatMessages(String chatId);

  Future<ChatMessageModel> sendMessage({
    required String chatId,
    required String senderId,
    required String message,
  });

  Future<void> markAsRead(String chatId, String userId);
}

/// Implementation of ChatRemoteDataSource
class ChatRemoteDataSourceImpl implements ChatRemoteDataSource {
  final ApiClient apiClient;

  ChatRemoteDataSourceImpl({required this.apiClient});

  @override
  Future<String> startChat({
    required String userId1,
    required String userId2,
    required String postId,
  }) async {
    try {
      final response = await apiClient.post(
        ApiConstants.chatStartEndpoint,
        body: {'user_id_1': userId1, 'user_id_2': userId2, 'post_id': postId},
      );
      return response['chat_id'] as String;
    } catch (e) {
      throw ServerException('Failed to start chat: $e');
    }
  }

  @override
  Future<List<ChatMessageModel>> getChatMessages(String chatId) async {
    try {
      final response = await apiClient.get(
        '${ApiConstants.chatEndpoint}/$chatId',
      );
      final List<dynamic> messagesJson = response['messages'] as List<dynamic>;
      return messagesJson
          .map(
            (json) => ChatMessageModel.fromJson(json as Map<String, dynamic>),
          )
          .toList();
    } catch (e) {
      throw ServerException('Failed to get chat messages: $e');
    }
  }

  @override
  Future<ChatMessageModel> sendMessage({
    required String chatId,
    required String senderId,
    required String message,
  }) async {
    try {
      final response = await apiClient.post(
        '${ApiConstants.chatEndpoint}/$chatId/messages',
        body: {'sender_id': senderId, 'message': message},
      );
      return ChatMessageModel.fromJson(response);
    } catch (e) {
      throw ServerException('Failed to send message: $e');
    }
  }

  @override
  Future<void> markAsRead(String chatId, String userId) async {
    try {
      await apiClient.post(
        '${ApiConstants.chatEndpoint}/$chatId/read',
        body: {'user_id': userId},
      );
    } catch (e) {
      throw ServerException('Failed to mark as read: $e');
    }
  }
}

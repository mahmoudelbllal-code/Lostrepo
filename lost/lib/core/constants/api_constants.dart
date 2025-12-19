/// API Configuration Constants
class ApiConstants {
  // Base URL - Update this with your Flask backend URL
  static const String baseUrl = 'http://localhost:5000/api';

  // API Endpoints
  static const String uploadEndpoint = '/upload';
  static const String searchEndpoint = '/search';
  static const String postsEndpoint = '/posts';
  static const String chatStartEndpoint = '/chat/start';
  static const String chatEndpoint = '/chat';

  // Timeout durations
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);

  // Headers
  static const Map<String, String> headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
}

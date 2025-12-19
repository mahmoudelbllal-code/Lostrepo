import 'dart:convert';
import 'package:http/http.dart' as http;
import '../constants/api_constants.dart';
import '../errors/exceptions.dart';

/// HTTP Client for API calls to Flask backend
class ApiClient {
  final http.Client client;

  ApiClient({http.Client? client}) : client = client ?? http.Client();

  /// Generic GET request
  Future<Map<String, dynamic>> get(String endpoint) async {
    try {
      final url = Uri.parse('${ApiConstants.baseUrl}$endpoint');
      final response = await client
          .get(url, headers: ApiConstants.headers)
          .timeout(ApiConstants.receiveTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw NetworkException('Failed to connect to server: $e');
    }
  }

  /// Generic POST request
  Future<Map<String, dynamic>> post(
    String endpoint, {
    Map<String, dynamic>? body,
  }) async {
    try {
      final url = Uri.parse('${ApiConstants.baseUrl}$endpoint');
      final response = await client
          .post(
            url,
            headers: ApiConstants.headers,
            body: body != null ? jsonEncode(body) : null,
          )
          .timeout(ApiConstants.receiveTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw NetworkException('Failed to connect to server: $e');
    }
  }

  /// POST request with multipart (for image upload)
  Future<Map<String, dynamic>> postMultipart(
    String endpoint, {
    required String filePath,
    Map<String, String>? fields,
  }) async {
    try {
      final url = Uri.parse('${ApiConstants.baseUrl}$endpoint');
      final request = http.MultipartRequest('POST', url);

      // Add file
      request.files.add(await http.MultipartFile.fromPath('image', filePath));

      // Add fields
      if (fields != null) {
        request.fields.addAll(fields);
      }

      final streamedResponse = await request.send().timeout(
        ApiConstants.receiveTimeout,
      );
      final response = await http.Response.fromStream(streamedResponse);

      return _handleResponse(response);
    } catch (e) {
      throw NetworkException('Failed to upload image: $e');
    }
  }

  /// Generic PUT request
  Future<Map<String, dynamic>> put(
    String endpoint, {
    Map<String, dynamic>? body,
  }) async {
    try {
      final url = Uri.parse('${ApiConstants.baseUrl}$endpoint');
      final response = await client
          .put(
            url,
            headers: ApiConstants.headers,
            body: body != null ? jsonEncode(body) : null,
          )
          .timeout(ApiConstants.receiveTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw NetworkException('Failed to connect to server: $e');
    }
  }

  /// Generic DELETE request
  Future<Map<String, dynamic>> delete(String endpoint) async {
    try {
      final url = Uri.parse('${ApiConstants.baseUrl}$endpoint');
      final response = await client
          .delete(url, headers: ApiConstants.headers)
          .timeout(ApiConstants.receiveTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw NetworkException('Failed to connect to server: $e');
    }
  }

  /// Handle HTTP response
  Map<String, dynamic> _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) {
        return {};
      }
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else if (response.statusCode == 400) {
      throw ServerException(
        'Bad Request: ${response.body}',
        statusCode: response.statusCode,
      );
    } else if (response.statusCode == 401) {
      throw ServerException('Unauthorized', statusCode: response.statusCode);
    } else if (response.statusCode == 404) {
      throw ServerException('Not Found', statusCode: response.statusCode);
    } else if (response.statusCode == 500) {
      throw ServerException(
        'Internal Server Error',
        statusCode: response.statusCode,
      );
    } else {
      throw ServerException(
        'Unexpected error: ${response.statusCode}',
        statusCode: response.statusCode,
      );
    }
  }

  /// Dispose client
  void dispose() {
    client.close();
  }
}

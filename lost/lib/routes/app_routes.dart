import 'package:flutter/material.dart';
import '../presentation/screens/welcome_screen.dart';
import '../presentation/screens/login_screen.dart';
import '../presentation/screens/signup_screen.dart';
import '../presentation/screens/home_screen.dart';
import '../presentation/screens/search_screen.dart';
import '../presentation/screens/profile_screen.dart';
import '../presentation/screens/settings_screen.dart';
import '../presentation/screens/forgot_password_screen.dart';
import '../presentation/screens/verification_screen.dart';
import '../presentation/screens/new_password_screen.dart';
import '../presentation/screens/notifications_screen.dart';
import '../presentation/screens/chat_screen.dart';
import '../presentation/screens/create_post_screen.dart';
import '../presentation/screens/ai_matching_results_screen.dart';

/// App Routes Configuration
class AppRoutes {
  static const String welcome = '/';
  static const String home = '/home';
  static const String search = '/search';
  static const String createPost = '/create-post';
  static const String postDetail = '/post-detail';
  static const String profile = '/profile';
  static const String settingsRoute = '/settings';
  static const String chat = '/chat';
  static const String login = '/login';
  static const String signup = '/signup';
  static const String forgotPassword = '/forgot-password';
  static const String verification = '/verification';
  static const String newPassword = '/new-password';
  static const String notifications = '/notifications';
  static const String aiMatchingResults = '/ai-matching-results';

  static Route<dynamic> onGenerateRoute(RouteSettings settings) {
    switch (settings.name) {
      case welcome:
        return MaterialPageRoute(builder: (_) => const WelcomeScreen());

      case home:
        return MaterialPageRoute(builder: (_) => const HomeScreen());

      case search:
        return MaterialPageRoute(builder: (_) => const SearchScreen());

      case createPost:
        return MaterialPageRoute(builder: (_) => const CreatePostScreen());

      case postDetail:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(child: Text('Post Detail Screen - Coming Soon')),
          ),
        );

      case aiMatchingResults:
        final args = settings.arguments as Map<String, dynamic>?;
        return MaterialPageRoute(
          builder: (_) => AIMatchingResultsScreen(postData: args),
        );

      case profile:
        return MaterialPageRoute(builder: (_) => const ProfileScreen());

      case '/settings':
        return MaterialPageRoute(builder: (_) => const SettingsScreen());

      case chat:
        return MaterialPageRoute(builder: (_) => const ChatScreen());

      case login:
        return MaterialPageRoute(builder: (_) => const LoginScreen());

      case signup:
        return MaterialPageRoute(builder: (_) => const SignUpScreen());

      case forgotPassword:
        return MaterialPageRoute(builder: (_) => const ForgotPasswordScreen());

      case verification:
        return MaterialPageRoute(builder: (_) => const VerificationScreen());

      case newPassword:
        return MaterialPageRoute(builder: (_) => const NewPasswordScreen());

      case notifications:
        return MaterialPageRoute(builder: (_) => const NotificationsScreen());

      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(child: Text('Route not found: ${settings.name}')),
          ),
        );
    }
  }
}

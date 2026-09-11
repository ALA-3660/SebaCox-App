import 'user.dart';

/// Authentication state stages as specified in Phase 2:
/// UNKNOWN -> CHECKING_SESSION -> UNAUTHENTICATED or AUTHENTICATED
enum AuthStatus {
  unknown,
  checkingSession,
  unauthenticated,
  authenticated,
}

class AuthState {
  final AuthStatus status;
  final User? user;
  final String? errorMessage;
  final bool isLoading;

  const AuthState({
    required this.status,
    this.user,
    this.errorMessage,
    this.isLoading = false,
  });

  factory AuthState.unknown() => const AuthState(status: AuthStatus.unknown);
  factory AuthState.checkingSession() => const AuthState(status: AuthStatus.checkingSession, isLoading: true);
  factory AuthState.unauthenticated({String? error}) => AuthState(
        status: AuthStatus.unauthenticated,
        errorMessage: error,
      );
  factory AuthState.authenticated(User user) => AuthState(
        status: AuthStatus.authenticated,
        user: user,
      );

  AuthState copyWith({
    AuthStatus? status,
    User? user,
    String? errorMessage,
    bool? isLoading,
  }) {
    return AuthState(
      status: status ?? this.status,
      user: user ?? this.user,
      errorMessage: errorMessage,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}

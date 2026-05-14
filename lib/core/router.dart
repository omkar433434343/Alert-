import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/models/models.dart';
import '../core/auth/auth_provider.dart';
import '../features/splash/splash_screen.dart';
import '../features/auth/role_select_screen.dart';
import '../features/auth/login_screen.dart';
import '../features/asha/dashboard/asha_dashboard.dart';
import '../features/asha/patients/patient_list_screen.dart';
import '../features/asha/patients/patient_form_screen.dart';
import '../features/asha/patients/patient_detail_screen.dart';
import '../features/asha/patients/patient_chat_screen.dart';
import '../features/asha/triage/triage_form_screen.dart';
import '../features/asha/triage/voice_triage_screen.dart';
import '../features/profile/profile_screen.dart';
import '../features/asha/asha_shell.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final auth = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/splash',
    redirect: (context, state) {
      final loggedIn = auth.isLoggedIn;
      final onAuth =
          state.matchedLocation.startsWith('/login') ||
          state.matchedLocation == '/role' ||
          state.matchedLocation == '/splash';

      if (!loggedIn && !onAuth) return '/role';
      if (loggedIn &&
          (state.matchedLocation == '/role' ||
              state.matchedLocation.startsWith('/login'))) {
        return '/asha';
      }
      return null;
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      GoRoute(path: '/role', builder: (_, __) => const RoleSelectScreen()),
      GoRoute(
        path: '/login/:role',
        builder: (_, __) => const LoginScreen(role: 'asha'),
      ),

      // ASHA Shell Route
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) =>
            AshaShell(navigationShell: navigationShell),
        branches: [
          StatefulShellBranch(
            routes: [
              GoRoute(path: '/asha', builder: (_, __) => const AshaDashboard()),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/asha/patients',
                builder: (_, __) => const PatientListScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            routes: [
              GoRoute(
                path: '/asha/triage',
                builder: (_, state) => TriageFormScreen(
                  autoVoice: state.uri.queryParameters['autoVoice'] == 'true',
                ),
              ),
            ],
          ),
        ],
      ),

      // Other ASHA routes (pushed on top)
      GoRoute(
        path: '/asha/patients/new',
        builder: (_, __) => const PatientFormScreen(),
      ),
      GoRoute(
        path: '/asha/patients/edit',
        builder: (_, state) =>
            PatientFormScreen(editPatient: state.extra as PatientModel),
      ),
      GoRoute(
        path: '/asha/patients/detail',
        builder: (_, state) =>
            PatientDetailScreen(patient: state.extra as PatientModel),
      ),
      GoRoute(
        path: '/asha/patients/chat',
        builder: (_, state) =>
            PatientChatScreen(patient: state.extra as PatientModel),
      ),
      GoRoute(
        path: '/asha/triage/voice',
        builder: (_, __) => const VoiceTriageScreen(),
      ),
      GoRoute(path: '/asha/profile', builder: (_, __) => const ProfileScreen()),

    ],
  );
});

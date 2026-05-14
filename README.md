# Alert+

Alert+ is a Flutter mobile app built for frontline and district health workflows.
It provides role-based experiences for ASHA workers and THO officers with offline-first behavior, triage flows, patient tracking, and outbreak visibility.

## Highlights

- Role-based login and navigation for ASHA and THO
- Patient registration, edit, details, and role-wise views
- Triage workflow with voice triage support
- AI suggestion integration for triage records
- Offline queueing and cached reads for unstable connectivity
- Outbreak map view and district-level monitoring
- Multi-language support (English, Hindi, Kannada)

## Tech Stack

- Flutter (Dart)
- State management: Riverpod
- Routing: go_router
- Networking: Dio
- Storage/security: flutter_secure_storage
- Offline/connectivity: connectivity_plus, local queue/cache utilities
- Mapping: flutter_map + OpenStreetMap tiles

## Project Structure

```text
lib/
  core/
    api/            # API client + endpoint constants
    auth/           # Auth state provider
    i18n/           # Localizations and locale provider
    offline/        # Offline cache and sync queue
    router.dart     # App routes and role guards
    theme/          # App theme and colors
  features/
    auth/           # Role select + login
    splash/         # App startup flow
    asha/           # ASHA dashboards, patients, triage
    tho/            # THO dashboards, patients, outbreaks, review
  shared/
    widgets/        # Reusable UI widgets
```

## Prerequisites

- Flutter SDK 3.11+
- Dart SDK (bundled with Flutter)
- Android Studio / Xcode toolchains for device builds

## Setup

```bash
flutter pub get
```

## Run

```bash
flutter run
```

## API Configuration

Base API URL is set in `lib/core/api/endpoints.dart`:

- `https://alert-plus-full.onrender.com`

Update it there if you want to point to a local or staging backend.

## Quality Checks

```bash
flutter analyze
flutter test
```

## Notes

- The app is designed to continue working during intermittent network conditions.
- Pending writes are queued and synced when connectivity returns.

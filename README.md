# Alert+

Alert+ is an offline-first, AI-assisted rural healthcare coordination platform for ASHA workers and THO officers. Built with Flutter, it supports multilingual triage, frontline patient workflows, and district-level outbreak monitoring in low-connectivity environments.

The platform is designed for practical field use: capture data at the point of care, continue operations without stable internet, and synchronize safely when connectivity returns.

## Core Features

- **Role-based workflows:** Dedicated experiences for ASHA and THO users with guarded routing and role-specific screens.
- **Multilingual accessibility:** Localized interface support for English, Hindi, and Kannada.
- **Voice-assisted triage capture:** Faster symptom intake through voice-enabled triage flow.
- **AI-assisted symptom analysis:** Clinical suggestion support integrated into triage record workflows.
- **Outbreak hotspot visualization:** Map-based outbreak view for district-level awareness and monitoring.
- **Offline workflow continuity:** Cached reads and queued writes for reliable operation in unstable networks.

## Problems Addressed

- **Poor rural connectivity:** Enables care workflows to continue even when mobile data is unreliable.
- **Delayed healthcare response:** Streamlines triage capture and review to reduce response lag.
- **Outbreak visibility gaps:** Improves situational awareness with map-based outbreak markers.
- **Language barriers in field operations:** Reduces friction through multilingual UI support.
- **Frontline triage complexity:** Simplifies symptom collection with guided and voice-assisted flows.

## Tech Stack

- **Framework:** Flutter (Dart)
- **State Management:** Riverpod
- **Navigation:** go_router
- **Networking:** Dio
- **Secure Local Storage:** flutter_secure_storage
- **Connectivity & Offline Utilities:** connectivity_plus, local cache/queue modules
- **Maps:** flutter_map + OpenStreetMap tiles

## Architecture Overview

- **Feature-first structure:** Organized by domain areas (auth, ASHA, THO, shared, core).
- **Reactive state management:** Riverpod providers coordinate auth, routing, and data flow.
- **Role-based routing:** Guarded navigation redirects users into role-specific app shells.
- **Offline queue synchronization:** Pending write operations are queued locally and synced when online.

## Offline-First Design

Alert+ is built to remain functional during network interruptions:

- **Queued writes:** Form submissions and updates are stored locally when offline.
- **Cached reads:** Recently fetched records are available for local access.
- **Automatic sync recovery:** Queued operations are retried when connectivity is restored.

## Project Structure

```text
lib/
  core/
    api/            # API client and endpoint definitions
    auth/           # Authentication state providers
    i18n/           # Localization maps and locale provider
    offline/        # Cache and offline sync queue
    router.dart     # Role-aware app routing
    theme/          # Design tokens and theme setup
  features/
    splash/         # Startup and session routing
    auth/           # Role selection and login
    asha/           # ASHA dashboards, patients, triage
    tho/            # THO dashboards, outbreaks, triage review
  shared/
    widgets/        # Reusable UI components
    utils/          # Shared utility helpers
```

## Getting Started

### Prerequisites

- Flutter SDK 3.11+
- Dart SDK (bundled with Flutter)
- Android Studio and/or Xcode toolchain

### Installation

```bash
flutter pub get
```

### Run

```bash
flutter run
```

### Quality Checks

```bash
flutter analyze
flutter test
```

## API Configuration

Set backend endpoints in `lib/core/api/endpoints.dart`.

Current base URL:

- `https://alert-plus-full.onrender.com`

## Hackathon Focus

Alert+ is built around practical AI for social good:

- Expanding rural healthcare accessibility through mobile-first workflows
- Enabling resilient care operations in connectivity-constrained areas
- Supporting frontline decision workflows with AI-assisted triage context

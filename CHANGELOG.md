# Changelog

All notable changes to this project will be documented here.

## [1.0.0] - 2026-03-22

### Added
- **Habit Tracking Core**:
  - Daily and Weekly habit frequency support.
  - Habit categories for better organization (Health, Work, Personal, etc.).
  - Description field for habits.
  - Hard delete with Trash storage and restoration functionality.
- **Analytics Dashboard**:
  - Real-time streak tracking and visualization.
  - Completion rate donut charts.
  - Weekly activity heatmaps and metrics.
  - General performance stats.
- **Goals System**:
  - Creation of streak-based and completion-based goals.
  - Automatic goal progress synchronization when marking habits.
  - Celebration notifications on goal completion.
- **Modern UI & Theme System**:
  - Dynamic Dark and Light mode switching.
  - SF Pro Display typography integration.
  - Glassmorphic design elements and modern layouts.
  - Sidebar-based navigation flow.
- **Profile Management**:
  - Customizable profile name and email.
  - Circular avatar cropping and upload system using OpenCV/PIL.
  - Persistent profile data storage.
- **Notifications**:
  - Daily reminder scheduling.
  - System tray notifications and in-app alerts.
- **Data Layer**:
  - SQLite database integration for local, private data storage.
  - Migration scripts and database initialization logic.
- **Build System**:
  - PyInstaller configuration for standalone executable generation.
  - Automated checklist for project quality and linting.

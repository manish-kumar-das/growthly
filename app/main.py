"""
Growthly Application
Main entry point
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

__version__ = "1.0.0"

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import init_db
from app.views.main_window import MainWindow


from PySide6.QtCore import Qt

def main():
    """Main application entry point"""
    # Initialize database
    init_db()

    # Set High DPI Factor Rounding Policy BEFORE creating QApplication
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Growthly")

    # Handle High DPI Scaling attributes for Qt 5 style (safe in Qt 6)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Force Fusion style for consistent cross-platform appearance
    app.setStyle("Fusion")

    # Set default font
    app.setFont(QFont("SF Pro Display", 11))

    # Simple light theme for HabitHub UI
    app.setStyleSheet("""
        QWidget {
            background-color: #F8F9FA;
            color: #212529;
        }
    """)

    # Create and show main window
    window = MainWindow()

    # FULL SCREEN MODE
    window.showMaximized()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

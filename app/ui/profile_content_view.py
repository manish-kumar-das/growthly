"""
Profile Content View — Clean Single-Page SaaS Dashboard
No scroll. Fits in one window. Minimal & professional.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QTextEdit,
    QMessageBox,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QFileDialog,
)
import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.profile_service import get_profile_service
from app.ui.crop_dialog import CropDialog
from app.utils.image_utils import get_circular_pixmap
from app.themes import get_theme_manager


def _shadow(parent=None, blur=14, y=3, alpha=10):
    s = QGraphicsDropShadowEffect(parent)
    s.setBlurRadius(blur)
    s.setOffset(0, y)
    s.setColor(QColor(0, 0, 0, alpha))
    return s


# ═══════════════════════════════════════════════════════════
#  Stat Card
# ═══════════════════════════════════════════════════════════
class StatCard(QFrame):
    def __init__(self, icon, value, label, accent, parent=None):
        super().__init__(parent)
        self.accent = accent
        self.setObjectName("statCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._default_style()
        self.setGraphicsEffect(_shadow(self, blur=12, y=3, alpha=8))

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(8)

        # Icon circle
        icon_bg = QFrame()
        icon_bg.setFixedSize(44, 44)
        icon_bg.setStyleSheet(f"""
            background-color: {accent}14;
            border-radius: 12px; border: none;
        """)
        ic_lay = QVBoxLayout(icon_bg)
        ic_lay.setContentsMargins(0, 0, 0, 0)
        ic_lay.setAlignment(Qt.AlignCenter)
        ic_lbl = QLabel(icon)
        ic_lbl.setFont(QFont("SF Pro Display", 20))
        ic_lbl.setStyleSheet("background:transparent; border:none;")
        ic_lay.addWidget(ic_lbl)
        root.addWidget(icon_bg)

        root.addStretch()

        # Value
        self.val_lbl = QLabel(value)
        self.val_lbl.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        self.val_lbl.setStyleSheet("color:#111827; background:transparent; border:none;")
        root.addWidget(self.val_lbl)

        # Label
        cap = QLabel(label.upper())
        cap.setFont(QFont("Inter", 10, QFont.DemiBold))
        cap.setStyleSheet("color:#6B7280; letter-spacing:0.6px; background:transparent; border:none;")
        root.addWidget(cap)

    def _default_style(self):
        self.setStyleSheet("""
            QFrame#statCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
        """)

    def enterEvent(self, ev):
        self.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: #FFFFFF;
                border: 1px solid {self.accent}40;
                border-radius: 16px;
            }}
        """)
        super().enterEvent(ev)

    def leaveEvent(self, ev):
        self._default_style()
        super().leaveEvent(ev)


# ═══════════════════════════════════════════════════════════
#  Main Profile View — single page, no scroll
# ═══════════════════════════════════════════════════════════
class ProfileContentView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.profile_service = get_profile_service()
        self.theme_manager = get_theme_manager()
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        colors = self.theme_manager.get_theme()
        self.setStyleSheet(f"background-color: {colors.BG_PRIMARY};")

        main = QVBoxLayout(self)
        main.setContentsMargins(40, 28, 40, 28)
        main.setSpacing(16)

        # ═══════════════════════════════════════════════
        # 1. HEADER — Avatar + Name only
        # ═══════════════════════════════════════════════
        self.header = QFrame()
        self.header.setObjectName("headerCard")
        self.header.setStyleSheet(f"""
            QFrame#headerCard {{
                background-color: {colors.BG_PRIMARY};
                border: 1px solid #E5E7EB;
                border-radius: 20px;
            }}
            QLabel {{ background:transparent; border:none; }}
        """)
        self.header.setGraphicsEffect(_shadow(self.header))

        h_lay = QHBoxLayout(self.header)
        h_lay.setContentsMargins(32, 24, 32, 24)
        h_lay.setSpacing(20)

        # Avatar — 94px Container
        self.av_container = QFrame()
        self.av_container.setFixedSize(94, 94)
        self.av_container.setStyleSheet("background: transparent; border: none;")
        self.av_container.setGraphicsEffect(_shadow(self.av_container, blur=12, y=4, alpha=15))
        
        av_l = QVBoxLayout(self.av_container)
        av_l.setContentsMargins(2, 2, 2, 2) # Padding for the border
        av_l.setAlignment(Qt.AlignCenter)
        
        self.av_label = QLabel()
        self.av_label.setFixedSize(90, 90)
        self.av_label.setAlignment(Qt.AlignCenter)
        self.av_label.setScaledContents(True)
        self.av_label.setStyleSheet("""
            background-color: #F3F4F6;
            border: 2px solid #E5E7EB;
            border-radius: 45px;
        """)
        
        self.av_icon = QLabel("👤")
        self.av_icon.setFont(QFont("SF Pro Display", 42))
        self.av_icon.setAlignment(Qt.AlignCenter)
        self.av_icon.setStyleSheet("background: transparent; border: none;")
        
        av_l.addWidget(self.av_label)
        
        # Icon overlay
        self.av_icon.setParent(self.av_label)
        self.av_icon.setGeometry(0, 0, 90, 90)
        
        # Change photo button (overlay)
        self.change_av_btn = QPushButton("📷")
        self.change_av_btn.setParent(self.av_container)
        self.change_av_btn.setFixedSize(32, 32)
        self.change_av_btn.move(62, 62)
        self.change_av_btn.setCursor(Qt.PointingHandCursor)
        self.change_av_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                border-radius: 16px;
                font-size: 14px;
                padding-bottom: 2px;
            }
            QPushButton:hover {
                background-color: #F9FAFB;
                border: 2px solid #7C3AED;
            }
        """)
        self.change_av_btn.clicked.connect(self.select_avatar)
        
        h_lay.addWidget(self.av_container)

        # Name
        self.name_header = QLabel("Loading…")
        self.name_header.setFont(QFont("SF Pro Display", 30, QFont.Bold))
        self.name_header.setStyleSheet("color:#111827; letter-spacing:-0.3px;")
        h_lay.addWidget(self.name_header, stretch=1)

        main.addWidget(self.header)

        # ═══════════════════════════════════════════════
        # 2. STAT CARDS ROW
        # ═══════════════════════════════════════════════
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(12)
        main.addLayout(self.stats_row)

        # ═══════════════════════════════════════════════
        # 3. ACCOUNT SETTINGS
        # ═══════════════════════════════════════════════
        self.form = QFrame()
        self.form.setObjectName("formCard")
        self.form.setStyleSheet(f"""
            QFrame#formCard {{
                background-color: {colors.BG_PRIMARY};
                border: 1px solid #E5E7EB;
                border-radius: 20px;
            }}
            QLabel {{ background:transparent; border:none; }}
        """)
        self.form.setGraphicsEffect(_shadow(self.form))

        f_lay = QVBoxLayout(self.form)
        f_lay.setContentsMargins(32, 28, 32, 28)
        f_lay.setSpacing(16)

        title = QLabel("Account Settings")
        title.setFont(QFont("SF Pro Display", 22, QFont.DemiBold))
        title.setStyleSheet("color:#111827;")
        f_lay.addWidget(title)

        # Input fields
        self.inputs = {}
        self.inputs["name"] = self._add_field("Full Display Name", "👤", f_lay)
        self.inputs["email"] = self._add_field("Email Address", "📧", f_lay)
        self.inputs["bio"] = self._add_field("Short Bio", "📝", f_lay, multiline=True)

        # Save button
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setFixedWidth(200)
        self.save_btn.setFixedHeight(44)
        self.save_btn.setFont(QFont("Inter", 13, QFont.Bold))
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #7C3AED, stop:1 #6D28D9);
                color: #FFFFFF; border: none; border-radius: 22px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #8B5CF6, stop:1 #7C3AED);
            }
        """)
        self.save_btn.clicked.connect(self.save_profile)
        btn_row.addWidget(self.save_btn)
        btn_row.addStretch()
        f_lay.addLayout(btn_row)

        main.addWidget(self.form)
        main.addStretch()

    def apply_theme(self):
        """Apply theme dynamically"""
        colors = self.theme_manager.get_theme()
        
        self.setStyleSheet(f"background-color: {colors.BG_PRIMARY};")
        if hasattr(self, 'header'):
            self.header.setStyleSheet(f"""
                QFrame#headerCard {{
                    background-color: {colors.BG_PRIMARY};
                    border: 1px solid #E5E7EB;
                    border-radius: 20px;
                }}
                QLabel {{ background:transparent; border:none; }}
            """)
            
        if hasattr(self, 'form'):
            self.form.setStyleSheet(f"""
                QFrame#formCard {{
                    background-color: {colors.BG_PRIMARY};
                    border: 1px solid #E5E7EB;
                    border-radius: 20px;
                }}
                QLabel {{ background:transparent; border:none; }}
            """)
            
        if hasattr(self, 'name_header'):
            self.name_header.setStyleSheet(f"color: {colors.TEXT_PRIMARY}; letter-spacing:-0.3px;")

    # ─── field builder ───────────────────────────────
    def _add_field(self, label_text, icon, parent_layout, multiline=False):
        group = QVBoxLayout()
        group.setSpacing(4)

        lbl = QLabel(label_text.upper())
        lbl.setFont(QFont("Inter", 10, QFont.Bold))
        lbl.setStyleSheet("color:#6B7280; letter-spacing:0.5px;")
        group.addWidget(lbl)

        container = QFrame()
        container.setObjectName("inputRow")
        container.setStyleSheet("""
            QFrame#inputRow {
                background-color: #FFFFFF;
                border: 1.5px solid #E5E7EB;
                border-radius: 12px;
            }
            QFrame#inputRow:hover { border: 1.5px solid #D1D5DB; }
        """)

        row = QHBoxLayout(container)
        row.setContentsMargins(12, 2, 12, 2)
        row.setSpacing(8)

        ic = QLabel(icon)
        ic.setFont(QFont("SF Pro Display", 15))
        ic.setStyleSheet("color:#9CA3AF;")
        ic.setFixedWidth(22)
        row.addWidget(ic)

        if multiline:
            container.setFixedHeight(64)
            row.setAlignment(Qt.AlignTop)
            row.setContentsMargins(12, 10, 12, 2)
            edit = QTextEdit()
            edit.setFixedHeight(48)
            edit.setStyleSheet(
                "border:none; background:transparent; font-size:14px; color:#1E293B; font-family:Inter;"
            )
        else:
            edit = QLineEdit()
            edit.setFixedHeight(40)
            edit.setStyleSheet(
                "border:none; background:transparent; font-size:14px; color:#1E293B; font-family:Inter;"
            )

        row.addWidget(edit, stretch=1)
        group.addWidget(container)
        parent_layout.addLayout(group)
        return edit

    # ─── data ────────────────────────────────────────
    def load_profile_data(self):
        profile = self.profile_service.get_profile()
        self.name_header.setText(profile["name"])
        self.inputs["name"].setText(profile["name"])
        self.inputs["email"].setText(profile["email"])
        self.inputs["bio"].setText(profile["bio"])
        self.set_avatar_image(profile.get("avatar_path"))
        self._refresh_stats()

    def set_avatar_image(self, path):
        if path and os.path.exists(path):
            pix = get_circular_pixmap(path, 90)
            if pix:
                self.av_label.setPixmap(pix)
                self.av_label.setStyleSheet("background: transparent; border: 1px solid #E5E7EB; border-radius: 45px;")
                self.av_icon.hide()
            else:
                self.av_icon.show()
                self._reset_avatar_style()
        else:
            self.av_label.clear()
            self.av_icon.show()
            self._reset_avatar_style()

    def _reset_avatar_style(self):
        self.av_label.setStyleSheet("""
            background-color: #F3F4F6;
            border: 2px solid #E5E7EB;
            border-radius: 45px;
        """)

    def select_avatar(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Profile Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            dialog = CropDialog(path, self)
            if dialog.exec():
                cropped_path = dialog.final_path
                self.profile_service.update_profile(avatar_path=cropped_path)
                self.set_avatar_image(cropped_path)
                if self.main_window and hasattr(self.main_window, "sidebar"):
                    self.main_window.sidebar.update_profile_avatar(cropped_path)

    def _refresh_stats(self):
        habits = self.habit_service.get_all_habits()

        total_habits = len(habits)
        total_xp = sum(
            len(self.habit_service.get_habit_completions(h.id)) for h in habits
        )
        best_streak = max(
            [self.streak_service.get_streak_info(h.id)["current_streak"]
             for h in habits] + [0]
        )

        # Clear previous cards
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cards = [
            ("🎯", str(total_habits), "Habits", "#10B981"),
            ("🚀", str(total_xp), "Total XP", "#7C3AED"),
            ("🔥", str(best_streak), "Best Streak", "#F59E0B"),
        ]
        for icon, val, lbl, accent in cards:
            self.stats_row.addWidget(StatCard(icon, val, lbl, accent))

    # ─── save ────────────────────────────────────────
    def save_profile(self):
        name = self.inputs["name"].text().strip()
        email = self.inputs["email"].text().strip()
        bio = self.inputs["bio"].toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error",
                                "Please provide a valid display name.")
            return

        try:
            self.profile_service.update_profile(name=name, email=email, bio=bio)
            self.name_header.setText(name)

            if self.main_window and hasattr(self.main_window, "sidebar"):
                self.main_window.sidebar.update_profile_name(name)

            orig = self.save_btn.text()
            self.save_btn.setText("✓  Saved!")
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 #10B981, stop:1 #059669);
                    color:#FFFFFF; border:none; border-radius:22px;
                }
            """)
            QTimer.singleShot(1800, lambda: self._reset_btn(orig))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

    def _reset_btn(self, text):
        self.save_btn.setText(text)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #7C3AED, stop:1 #6D28D9);
                color:#FFFFFF; border:none; border-radius:22px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #8B5CF6, stop:1 #7C3AED);
            }
        """)

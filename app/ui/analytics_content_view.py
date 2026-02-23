"""
Analytics Content View - Premium Dashboard with Interactive Graphs
Beautiful charts, insights, and statistics
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QGraphicsDropShadowEffect,
    QComboBox,
    QButtonGroup,
    QRadioButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QLinearGradient, QPainterPath
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class LineChart(QWidget):
    """Beautiful line chart widget with fixed Y-axis"""

    def __init__(self, data, labels, title, parent=None):
        super().__init__(parent)
        self.data = data
        self.labels = labels
        self.title = title
        self.setMinimumHeight(350)
        self.setStyleSheet("background-color: transparent;")

    def get_nice_scale(self, max_value):
        """Calculate nice round numbers for Y-axis"""
        if max_value == 0:
            return 10, [0, 2, 4, 6, 8, 10]

        # Find appropriate step size
        if max_value <= 5:
            step = 1
            max_scale = 5
        elif max_value <= 10:
            step = 2
            max_scale = 10
        elif max_value <= 20:
            step = 5
            max_scale = 20
        elif max_value <= 50:
            step = 10
            max_scale = ((max_value // 10) + 1) * 10
        elif max_value <= 100:
            step = 20
            max_scale = ((max_value // 20) + 1) * 20
        else:
            step = 25
            max_scale = ((max_value // 25) + 1) * 25

        # Generate scale values
        scale_values = []
        current = 0
        while current <= max_scale:
            scale_values.append(current)
            current += step

        return max_scale, scale_values

    def paintEvent(self, event):
        """Draw the line chart"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Chart area
        margin = 60
        chart_width = self.width() - (margin * 2)
        chart_height = self.height() - (margin * 2)

        if not self.data or len(self.data) == 0:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("SF Pro Text", 14))
            painter.drawText(self.rect(), Qt.AlignCenter, "No data available")
            return

        max_value = max(self.data) if max(self.data) > 0 else 0
        max_scale, scale_values = self.get_nice_scale(max_value)

        # Draw grid lines and Y-axis labels
        num_lines = len(scale_values)
        for i, value in enumerate(reversed(scale_values)):
            y = margin + (chart_height * i / (num_lines - 1))

            # Grid line
            painter.setPen(QPen(QColor("#E5E7EB"), 1))
            painter.drawLine(margin, int(y), self.width() - margin, int(y))

            # Y-axis label
            painter.setPen(QColor("#6B7280"))
            painter.setFont(QFont("SF Pro Text", 11))
            text_rect = QRect(5, int(y) - 10, margin - 10, 20)
            painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, str(value))

        # Draw line
        if len(self.data) > 1:
            path = QPainterPath()

            # Calculate points
            points = []
            for i, value in enumerate(self.data):
                x = margin + (chart_width * i / (len(self.data) - 1))
                y = (
                    margin
                    + chart_height
                    - (chart_height * value / max_scale if max_scale > 0 else 0)
                )
                points.append((x, y))

            # Draw gradient fill
            gradient = QLinearGradient(0, margin, 0, margin + chart_height)
            gradient.setColorAt(0, QColor(99, 102, 241, 100))
            gradient.setColorAt(1, QColor(99, 102, 241, 10))

            fill_path = QPainterPath()
            fill_path.moveTo(points[0][0], margin + chart_height)
            for x, y in points:
                fill_path.lineTo(x, y)
            fill_path.lineTo(points[-1][0], margin + chart_height)
            fill_path.closeSubpath()

            painter.fillPath(fill_path, gradient)

            # Draw line
            path.moveTo(points[0][0], points[0][1])
            for x, y in points[1:]:
                path.lineTo(x, y)

            painter.setPen(QPen(QColor("#6366F1"), 3))
            painter.drawPath(path)

            # Draw points
            for x, y in points:
                painter.setBrush(QColor("#FFFFFF"))
                painter.setPen(QPen(QColor("#6366F1"), 2))
                painter.drawEllipse(int(x) - 4, int(y) - 4, 8, 8)

        # Draw X-axis labels
        painter.setPen(QColor("#6B7280"))
        painter.setFont(QFont("SF Pro Text", 10))

        label_step = max(1, len(self.labels) // 10)  # Show max 10 labels
        for i, label in enumerate(self.labels):
            if label and (i % label_step == 0 or i == len(self.labels) - 1):
                x = (
                    margin + (chart_width * i / (len(self.data) - 1))
                    if len(self.data) > 1
                    else margin
                )
                painter.save()
                painter.translate(int(x), self.height() - margin + 20)
                painter.rotate(-45)
                painter.drawText(0, 0, label)
                painter.restore()


class BarChart(QWidget):
    """Beautiful bar chart widget with fixed Y-axis"""

    def __init__(self, data, labels, title, parent=None):
        super().__init__(parent)
        self.data = data
        self.labels = labels
        self.title = title
        self.setMinimumHeight(350)
        self.setStyleSheet("background-color: transparent;")

    def get_nice_scale(self, max_value):
        """Calculate nice round numbers for Y-axis"""
        if max_value == 0:
            return 10, [0, 2, 4, 6, 8, 10]

        # Find appropriate step size
        if max_value <= 5:
            step = 1
            max_scale = 5
        elif max_value <= 10:
            step = 2
            max_scale = 10
        elif max_value <= 20:
            step = 5
            max_scale = 20
        elif max_value <= 50:
            step = 10
            max_scale = ((max_value // 10) + 1) * 10
        elif max_value <= 100:
            step = 20
            max_scale = ((max_value // 20) + 1) * 20
        else:
            step = 25
            max_scale = ((max_value // 25) + 1) * 25

        # Generate scale values
        scale_values = []
        current = 0
        while current <= max_scale:
            scale_values.append(current)
            current += step

        return max_scale, scale_values

    def paintEvent(self, event):
        """Draw the bar chart"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        margin = 60
        chart_width = self.width() - (margin * 2)
        chart_height = self.height() - (margin * 2)

        if not self.data or len(self.data) == 0:
            painter.setPen(QColor("#9CA3AF"))
            painter.setFont(QFont("SF Pro Text", 14))
            painter.drawText(self.rect(), Qt.AlignCenter, "No data available")
            return

        max_value = max(self.data) if max(self.data) > 0 else 0
        max_scale, scale_values = self.get_nice_scale(max_value)

        # Draw grid lines and Y-axis labels
        num_lines = len(scale_values)
        for i, value in enumerate(reversed(scale_values)):
            y = margin + (chart_height * i / (num_lines - 1))

            # Grid line
            painter.setPen(QPen(QColor("#E5E7EB"), 1))
            painter.drawLine(margin, int(y), self.width() - margin, int(y))

            # Y-axis label
            painter.setPen(QColor("#6B7280"))
            painter.setFont(QFont("SF Pro Text", 11))
            text_rect = QRect(5, int(y) - 10, margin - 10, 20)
            painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, str(value))

        # Draw bars
        bar_width = chart_width / len(self.data) * 0.7
        bar_spacing = chart_width / len(self.data)

        for i, value in enumerate(self.data):
            x = margin + (bar_spacing * i) + (bar_spacing - bar_width) / 2
            bar_height = (chart_height * value / max_scale) if max_scale > 0 else 0
            y = margin + chart_height - bar_height

            # Gradient for bar
            gradient = QLinearGradient(x, y, x, y + bar_height)
            gradient.setColorAt(0, QColor("#8B5CF6"))
            gradient.setColorAt(1, QColor("#6366F1"))

            painter.fillRect(int(x), int(y), int(bar_width), int(bar_height), gradient)

            # Draw value on top
            if value > 0:
                painter.setPen(QColor("#4F46E5"))
                painter.setFont(QFont("SF Pro Text", 10, QFont.Bold))
                painter.drawText(
                    int(x),
                    int(y) - 5,
                    int(bar_width),
                    20,
                    Qt.AlignCenter,
                    str(int(value)),
                )

        # Draw X-axis labels
        painter.setPen(QColor("#6B7280"))
        painter.setFont(QFont("SF Pro Text", 9))

        label_step = max(1, len(self.labels) // 10)
        for i, label in enumerate(self.labels):
            if label and (i % label_step == 0 or i == len(self.labels) - 1):
                x = margin + (bar_spacing * i)
                painter.save()
                painter.translate(int(x + bar_spacing / 2), self.height() - margin + 20)
                painter.rotate(-45)
                painter.drawText(0, 0, label)
                painter.restore()


class StatCard(QFrame):
    """Premium stat card with icon and value"""

    def __init__(self, icon, title, value, subtitle, gradient_colors, parent=None):
        super().__init__(parent)
        self.setup_ui(icon, title, value, subtitle, gradient_colors)
        self.setCursor(Qt.PointingHandCursor)

        # Store original position
        self._hover_offset = 0

        # Animation for lift
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(180)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def setup_ui(self, icon, title, value, subtitle, gradient_colors):
        """Premium Stat Card UI"""

        # Fixed height for visual stability
        self.setFixedHeight(180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {gradient_colors[0]}, stop:1 {gradient_colors[1]});
                border-radius: 22px;
            }}
        """)

        # Softer, more premium shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 20, 26, 20)
        layout.setSpacing(6)

        # TOP ROW (ICON + TITLE)
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 28))
        icon_label.setStyleSheet("background: transparent;")
        top_row.addWidget(icon_label)

        top_row.addStretch()

        layout.addLayout(top_row)

        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Text", 12, QFont.Medium))
        title_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.85);
            background: transparent;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(title_label)

        # VALUE (Main Focus)
        value_label = QLabel(str(value))
        value_label.setFont(QFont("SF Pro Display", 38, QFont.Bold))
        value_label.setStyleSheet("""
            color: #FFFFFF;
            background: transparent;
        """)
        layout.addWidget(value_label)

        # BOTTOM SUBTITLE
        layout.addStretch()

        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("SF Pro Text", 11))
        subtitle_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.75);
            background: transparent;
        """)
        layout.addWidget(subtitle_label)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() - QPoint(0, 6))
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() + QPoint(0, 6))
        self.anim.start()
        super().leaveEvent(event)


class AnalyticsContentView(QWidget):
    """Premium Analytics Dashboard with Graphs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.current_chart_period = "7 days"  # Default
        self.setup_ui()
        self.load_analytics()

    def setup_ui(self):
        """Setup analytics UI"""
        self.setStyleSheet("background-color: #F9FAFB;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F9FAFB);
                border: none;
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 20, 40, 20)

        title_section = QHBoxLayout()
        title_section.setSpacing(12)

        icon = QLabel("📊")
        icon.setFont(QFont("SF Pro Display", 32))
        icon.setStyleSheet("background: transparent;")
        title_section.addWidget(icon)

        title_text_layout = QVBoxLayout()
        title_text_layout.setSpacing(2)

        title = QLabel("Analytics")
        title.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_text_layout.addWidget(title)

        subtitle = QLabel("Track your progress and insights")
        subtitle.setFont(QFont("SF Pro Text", 14))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_text_layout.addWidget(subtitle)

        title_section.addLayout(title_text_layout)

        header_layout.addLayout(title_section)
        header_layout.addStretch()

        layout.addWidget(header)

        # Content scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #F3F4F6;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #6366F1;
                border-radius: 5px;
            }
        """)

        content = QWidget()
        content.setStyleSheet("background-color: #F9FAFB;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(40, 28, 40, 28)
        self.content_layout.setSpacing(28)

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def load_analytics(self):
        """Load analytics data"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        habits = self.habit_service.get_all_habits()

        if not habits:
            empty_container = QFrame()
            empty_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFFFFF, stop:1 #F9FAFB);
                    border: 3px dashed #E5E7EB;
                    border-radius: 24px;
                }
            """)
            empty_container.setMinimumHeight(300)

            empty_layout = QVBoxLayout(empty_container)
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_layout.setSpacing(16)

            emoji = QLabel("📊")
            emoji.setFont(QFont("SF Pro Display", 80))
            emoji.setAlignment(Qt.AlignCenter)
            emoji.setStyleSheet("background: transparent;")
            empty_layout.addWidget(emoji)

            empty_title = QLabel("No Analytics Yet")
            empty_title.setFont(QFont("SF Pro Display", 26, QFont.Bold))
            empty_title.setAlignment(Qt.AlignCenter)
            empty_title.setStyleSheet("color: #374151; background: transparent;")
            empty_layout.addWidget(empty_title)

            empty_text = QLabel(
                "Create habits and start tracking to see your analytics!"
            )
            empty_text.setFont(QFont("SF Pro Text", 15))
            empty_text.setAlignment(Qt.AlignCenter)
            empty_text.setStyleSheet("color: #9CA3AF; background: transparent;")
            empty_layout.addWidget(empty_text)

            self.content_layout.addWidget(empty_container)
            self.content_layout.addStretch()
            return

        # Calculate stats
        total_habits = len(habits)
        completed_today = sum(
            1 for h in habits if self.habit_service.is_habit_completed_today(h.id)
        )

        # Calculate 30-day completion rate
        total_completions = 0
        total_possible = 0
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            for habit in habits:
                total_possible += 1
                if self.habit_service.is_habit_completed_on_date(habit.id, date):
                    total_completions += 1

        completion_rate = (
            int((total_completions / total_possible) * 100) if total_possible > 0 else 0
        )
        best_streak = max(
            (
                self.streak_service.get_streak_info(h.id).get("longest_streak", 0)
                for h in habits
            ),
            default=0,
        )

        # SECTION 1: HERO STATS

        hero_container = QFrame()
        hero_container.setStyleSheet("""
            QFrame {
                background: transparent;
            }
        """)

        hero_layout = QHBoxLayout(hero_container)
        hero_layout.setSpacing(20)
        hero_layout.setContentsMargins(20, 24, 20, 24)

        # Helper function for consistency score
        def calculate_consistency():
            if total_possible == 0:
                return 0
            return round((total_completions / total_possible) * 10, 1)

        consistency_score = calculate_consistency()

        # Card 1: Total Habits
        total_card = StatCard(
            "🎯", "Total Habits", total_habits, "Active habits", ["#6366F1", "#8B5CF6"]
        )
        hero_layout.addWidget(total_card, 1)

        # Card 2: Today Progress
        today_percentage = (
            int((completed_today / total_habits) * 100) if total_habits > 0 else 0
        )

        today_card = StatCard(
            "✅",
            "Today Progress",
            f"{completed_today}/{total_habits}",
            f"{today_percentage}% completed",
            ["#10B981", "#059669"],
        )
        hero_layout.addWidget(today_card, 1)

        # Card 3: Current Streak
        current_streak = max(
            (
                self.streak_service.get_streak_info(h.id).get("current_streak", 0)
                for h in habits
            ),
            default=0,
        )

        streak_card = StatCard(
            "🔥",
            "Current Streak",
            f"{current_streak}",
            "days in a row",
            ["#EF4444", "#DC2626"],
        )
        hero_layout.addWidget(streak_card, 1)

        # Card 4: Consistency Score
        score_label = (
            "Excellent"
            if consistency_score >= 8
            else "Good" if consistency_score >= 6 else "Needs Work"
        )

        score_card = StatCard(
            "⭐",
            "Consistency Score",
            f"{consistency_score}/10",
            score_label,
            ["#F59E0B", "#D97706"],
        )
        hero_layout.addWidget(score_card, 1)

        hero_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.content_layout.addWidget(hero_container)

        # GRAPHS SECTION
        self.add_graphs_section(habits)

        # SECTION 3: Week Comparison (already added)
        self.add_week_comparison_section()

        # ✅ ADD THESE NEW SECTIONS:
        # SECTION 4: Day of Week Analysis
        self.add_day_of_week_analysis()

        # SECTION 5: Best & Worst Habits
        self.add_best_worst_habits()

        # SECTION 6: Time of Day + Difficulty
        self.add_time_of_day_difficulty()

        # SECTION 7: Streak Heatmap
        self.add_streak_heatmap()

        # SECTION 8: Achievements
        self.add_achievements_section()
    
        # self.content_layout.addStretch()  # Keep at end



        

    def add_streak_heatmap(self):
        """GitHub-style Streak Calendar Heatmap"""
        heatmap_card = QFrame()
        heatmap_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 8)
        heatmap_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(heatmap_card)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # Header
        header = QHBoxLayout()

        title = QLabel("🔥 Streak Heatmap")

        title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        header.addWidget(title)

        header.addStretch()

        # Period selector
        period_label = QLabel("Show:")
        period_label.setFont(QFont("SF Pro Text", 13))
        period_label.setStyleSheet("color: #6B7280;")
        header.addWidget(period_label)

        self.heatmap_period = QComboBox()
        self.heatmap_period.addItems(["Last 90 Days", "Last 180 Days", "Last 365 Days"])
        self.heatmap_period.setCurrentText("Last 90 Days")
        self.heatmap_period.setFont(QFont("SF Pro Text", 12))
        self.heatmap_period.setFixedHeight(36)
        self.heatmap_period.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                padding: 4px 12px;
                min-width: 130px;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
            }
        """)
        self.heatmap_period.currentTextChanged.connect(self.update_heatmap)
        header.addWidget(self.heatmap_period)

        layout.addLayout(header)

        # Subtitle
        subtitle = QLabel(
            "Your consistency over time - darker colors mean more completions"
        )
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitle)

        # Heatmap container
        self.heatmap_container = QWidget()
        self.heatmap_layout = QVBoxLayout(self.heatmap_container)
        self.heatmap_layout.setContentsMargins(0, 10, 0, 10)
        self.heatmap_layout.setSpacing(0)

        layout.addWidget(self.heatmap_container)

        # Legend
        legend = QHBoxLayout()
        legend.setSpacing(12)

        legend_label = QLabel("Less")
        legend_label.setFont(QFont("SF Pro Text", 11))
        legend_label.setStyleSheet("color: #9CA3AF;")
        legend.addWidget(legend_label)

        # Color boxes
        colors = ["#EBEDF0", "#C6E48B", "#7BC96F", "#239A3B", "#196127"]
        for color in colors:
            box = QFrame()
            box.setFixedSize(18, 18)
            box.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border: 1px solid #E5E7EB;
                    border-radius: 3px;
                }}
            """)
            legend.addWidget(box)

        legend_label2 = QLabel("More")
        legend_label2.setFont(QFont("SF Pro Text", 11))
        legend_label2.setStyleSheet("color: #9CA3AF;")
        legend.addWidget(legend_label2)

        legend.addStretch()

        layout.addLayout(legend)

        self.content_layout.addWidget(heatmap_card)

        # Initial load
        self.update_heatmap()


    def update_heatmap(self):
        """Update heatmap based on selected period"""
        # Clear existing
        while self.heatmap_layout.count():
            item = self.heatmap_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        period_text = self.heatmap_period.currentText()
        days_map = {"Last 90 Days": 90, "Last 180 Days": 180, "Last 365 Days": 365}
        total_days = days_map.get(period_text, 90)

        # Get habits
        habits = self.habit_service.get_all_habits()
        if not habits:
            empty_label = QLabel("No data to display")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #9CA3AF; padding: 40px;")
            self.heatmap_layout.addWidget(empty_label)
            return

        # Calculate activity for each day
        activity_data = []
        max_completions = len(habits)

        for i in range(total_days):
            date = datetime.now() - timedelta(days=total_days - 1 - i)
            date_str = date.strftime("%Y-%m-%d")

            completions = sum(
                1
                for h in habits
                if self.habit_service.is_habit_completed_on_date(h.id, date_str)
            )
            percentage = (completions / max_completions * 100) if max_completions > 0 else 0

            activity_data.append(
                {"date": date, "completions": completions, "percentage": percentage}
            )

        # Create heatmap grid (weeks)
        weeks = []
        current_week = []

        for i, day_data in enumerate(activity_data):
            current_week.append(day_data)

            # New week on Sunday or end of data
            if day_data["date"].weekday() == 6 or i == len(activity_data) - 1:
                weeks.append(current_week)
                current_week = []

        # Render weeks horizontally
        grid_container = QWidget()
        grid_layout = QHBoxLayout(grid_container)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(4)

        # Month labels (top)
        months_shown = set()

        for week in weeks:
            week_col = QVBoxLayout()
            week_col.setSpacing(4)

            for day_data in week:
                cell = QFrame()
                cell.setFixedSize(14, 14)
                cell.setToolTip(
                    f"{day_data['date'].strftime('%b %d, %Y')}\n{day_data['completions']}/{max_completions} habits"
                )

                # Color based on percentage
                percentage = day_data["percentage"]
                if percentage == 0:
                    color = "#EBEDF0"
                elif percentage <= 25:
                    color = "#C6E48B"
                elif percentage <= 50:
                    color = "#7BC96F"
                elif percentage <= 75:
                    color = "#239A3B"
                else:
                    color = "#196127"

                cell.setStyleSheet(f"""
                    QFrame {{
                        background-color: {color};
                        border: 1px solid #E5E7EB;
                        border-radius: 2px;
                    }}
                    QFrame:hover {{
                        border: 2px solid #6366F1;
                    }}
                """)
                cell.setCursor(Qt.PointingHandCursor)

                week_col.addWidget(cell)

            grid_layout.addLayout(week_col)

        grid_layout.addStretch()

        self.heatmap_layout.addWidget(grid_container)

        # Stats below
        stats_container = QFrame()
        stats_container.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border-radius: 12px;
                padding: 16px;
            }
        """)

        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setSpacing(40)

        # Calculate stats
        total_completions = sum(d["completions"] for d in activity_data)
        perfect_days = sum(1 for d in activity_data if d["percentage"] == 100)
        zero_days = sum(1 for d in activity_data if d["percentage"] == 0)
        avg_rate = (
            sum(d["percentage"] for d in activity_data) / len(activity_data)
            if activity_data
            else 0
        )

        stats = [
            ("📊", "Total Completions", str(total_completions)),
            ("⭐", "Perfect Days", str(perfect_days)),
            ("📉", "Zero Days", str(zero_days)),
            ("📈", "Average Rate", f"{int(avg_rate)}%"),
        ]

        for icon, label, value in stats:
            stat_layout = QVBoxLayout()
            stat_layout.setSpacing(4)

            icon_label = QLabel(icon)
            icon_label.setFont(QFont("SF Pro Display", 20))
            icon_label.setAlignment(Qt.AlignCenter)
            stat_layout.addWidget(icon_label)

            value_label = QLabel(value)
            value_label.setFont(QFont("SF Pro Display", 20, QFont.Bold))
            value_label.setStyleSheet("color: #111827;")
            value_label.setAlignment(Qt.AlignCenter)
            stat_layout.addWidget(value_label)

            label_widget = QLabel(label)
            label_widget.setFont(QFont("SF Pro Text", 11))
            label_widget.setStyleSheet("color: #6B7280;")
            label_widget.setAlignment(Qt.AlignCenter)
            stat_layout.addWidget(label_widget)

            stats_layout.addLayout(stat_layout)

        stats_layout.addStretch()

        self.heatmap_layout.addWidget(stats_container)


    def add_achievements_section(self):
        """Achievement Badges & Milestones"""
        achievements_card = QFrame()
        achievements_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 8)
        achievements_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(achievements_card)
        layout.setContentsMargins(32, 28, 32, 32)
        layout.setSpacing(24)

        # Header
        header = QHBoxLayout()

        title = QLabel("🏅 Achievements & Milestones")
        title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        header.addWidget(title)

        header.addStretch()

        # Badge count
        habits = self.habit_service.get_all_habits()
        max_streak = (
            max(
                (
                    self.streak_service.get_streak_info(h.id).get("current_streak", 0)
                for h in habits
                ),
                default=0,
            )
            if habits
            else 0
        )

        unlocked_count = 0
        total_badges = 12  # Total available badges

        badge_count_label = QLabel(f"{unlocked_count}/12 Unlocked")
        badge_count_label.setFont(QFont("SF Pro Text", 13))
        badge_count_label.setStyleSheet("""
            QLabel {
                background-color: #EEF2FF;
                color: #4F46E5;
                padding: 6px 16px;
                border-radius: 12px;
            }
        """)
        header.addWidget(badge_count_label)

        layout.addLayout(header)

        subtitle = QLabel("Unlock badges by building consistent habits")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitle)

        # Define achievements
        achievements = [
            {
                "icon": "🔥",
                "name": "First Spark",
                "desc": "Complete 1 habit",
                "requirement": 1,
                "type": "streak",
            },
            {
                "icon": "⚡",
                "name": "3 Day Warrior",
                "desc": "Maintain 3 day streak",
                "requirement": 3,
                "type": "streak",
            },
            {
                "icon": "💪",
                "name": "Week Champion",
                "desc": "Maintain 7 day streak",
                "requirement": 7,
                "type": "streak",
            },
            {
                "icon": "🏆",
                "name": "Month Master",
                "desc": "Maintain 30 day streak",
                "requirement": 30,
                "type": "streak",
            },
            {
                "icon": "💎",
                "name": "Quarter King",
                "desc": "Maintain 90 day streak",
                "requirement": 90,
                "type": "streak",
            },
            {
                "icon": "👑",
                "name": "Year Legend",
                "desc": "Maintain 365 day streak",
                "requirement": 365,
                "type": "streak",
            },
            {
                "icon": "⭐",
                "name": "Perfect Day",
                "desc": "Complete all habits in one day",
                "requirement": 1,
                "type": "perfect",
            },
            {
                "icon": "🌟",
                "name": "Perfect Week",
                "desc": "Complete all habits for 7 days",
                "requirement": 7,
                "type": "perfect",
            },
            {
                "icon": "✨",
                "name": "Century Club",
                "desc": "Complete 100 total habits",
                "requirement": 100,
                "type": "total",
            },
            {
                "icon": "🎯",
                "name": "Half K",
                "desc": "Complete 500 total habits",
                "requirement": 500,
                "type": "total",
            },
            {
                "icon": "🚀",
                "name": "Grand Master",
                "desc": "Complete 1000 total habits",
                "requirement": 1000,
                "type": "total",
            },
            {
                "icon": "🌈",
                "name": "Rainbow Warrior",
                "desc": "Have habits in 5 categories",
                "requirement": 5,
                "type": "categories",
            },
        ]

        # Calculate total completions
        total_completions = 0
        if habits:
            for i in range(365):  # Last year
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                for habit in habits:
                    if self.habit_service.is_habit_completed_on_date(habit.id, date):
                        total_completions += 1

        # Get unique categories
        categories = set(h.category for h in habits) if habits else set()

        # Badges grid
        badges_container = QWidget()
        badges_layout = QHBoxLayout(badges_container)
        badges_layout.setSpacing(16)
        badges_layout.setAlignment(Qt.AlignLeft)

        unlocked_count = 0

        for achievement in achievements:
            # Determine if unlocked
            is_unlocked = False

            if achievement["type"] == "streak":
                is_unlocked = max_streak >= achievement["requirement"]
            elif achievement["type"] == "perfect":
                # Check for perfect days (simplified)
                is_unlocked = False  # You can implement perfect day tracking
            elif achievement["type"] == "total":
                is_unlocked = total_completions >= achievement["requirement"]
            elif achievement["type"] == "categories":
                is_unlocked = len(categories) >= achievement["requirement"]

            if is_unlocked:
                unlocked_count += 1

            badge = self._create_badge(
                achievement["icon"], achievement["name"], achievement["desc"], is_unlocked
            )
            badges_layout.addWidget(badge)

        # Update badge count
        badge_count_label.setText(f"{unlocked_count}/{len(achievements)} Unlocked")

        badges_layout.addStretch()

        # Scroll area for badges
        scroll = QScrollArea()
        scroll.setWidget(badges_container)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(180)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:horizontal {
                background: #F3F4F6;
                height: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: #6366F1;
                border-radius: 4px;
            }
        """)

        layout.addWidget(scroll)

        # Next milestone
        next_milestone_box = QFrame()
        next_milestone_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FEF3C7, stop:1 #FDE68A);
                border-radius: 16px;
                padding: 20px;
            }
        """)

        next_layout = QVBoxLayout(next_milestone_box)
        next_layout.setContentsMargins(20, 16, 20, 16)
        next_layout.setSpacing(12)

        next_title = QLabel("🎯 Next Milestone")
        next_title.setFont(QFont("SF Pro Display", 16, QFont.Bold))
        next_title.setStyleSheet("color: #78350F;")
        next_layout.addWidget(next_title)

        # Find next unachieved streak milestone
        streak_milestones = [
            a
            for a in achievements
            if a["type"] == "streak" and not (max_streak >= a["requirement"])
        ]
        if streak_milestones:
            next_achievement = streak_milestones[0]
            days_remaining = next_achievement["requirement"] - max_streak
            progress_percent = (max_streak / next_achievement["requirement"]) * 100

            next_text = QLabel(
                f"{next_achievement['icon']} {next_achievement['name']} - {days_remaining} days away!"
            )
            next_text.setFont(QFont("SF Pro Text", 14))
            next_text.setStyleSheet("color: #92400E;")
            next_layout.addWidget(next_text)

            # Progress bar
            progress_bg = QFrame()
            progress_bg.setFixedHeight(12)
            progress_bg.setStyleSheet("""
                QFrame {
                    background-color: #FCD34D;
                    border-radius: 6px;
                }
            """)

            progress_fill = QFrame(progress_bg)
            fill_width = int(600 * (progress_percent / 100))
            progress_fill.setGeometry(0, 0, fill_width, 12)
            progress_fill.setStyleSheet("""
                QFrame {
                    background-color: #F59E0B;
                    border-radius: 6px;
                }
            """)

            next_layout.addWidget(progress_bg)

            progress_label = QLabel(
                f"{max_streak}/{next_achievement['requirement']} days ({int(progress_percent)}%)"
            )
            progress_label.setFont(QFont("SF Pro Text", 12))
            progress_label.setStyleSheet("color: #92400E;")
            next_layout.addWidget(progress_label)
        else:
            congrats = QLabel("🎉 All streak milestones unlocked! You're a legend!")
            congrats.setFont(QFont("SF Pro Text", 14))
            congrats.setStyleSheet("color: #92400E;")
            next_layout.addWidget(congrats)

        layout.addWidget(next_milestone_box)

        self.content_layout.addWidget(achievements_card)


    def _create_badge(self, icon, name, desc, is_unlocked):
        """Create a single badge widget"""
        badge = QFrame()
        badge.setFixedSize(120, 150)
        badge.setCursor(Qt.PointingHandCursor)

        if is_unlocked:
            badge.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFFFFF, stop:1 #F0F9FF);
                    border: 2px solid #3B82F6;
                    border-radius: 16px;
                }
                QFrame:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #EFF6FF, stop:1 #DBEAFE);
                    border: 3px solid #2563EB;
                }
            """)
        else:
            badge.setStyleSheet("""
                QFrame {
                    background-color: #F9FAFB;
                    border: 2px solid #E5E7EB;
                    border-radius: 16px;
                }
                QFrame:hover {
                    background-color: #F3F4F6;
                }
            """)

        badge_layout = QVBoxLayout(badge)
        badge_layout.setContentsMargins(12, 16, 12, 16)
        badge_layout.setSpacing(8)

        # Icon
        icon_label = QLabel(icon)
        if is_unlocked:
            icon_label.setFont(QFont("SF Pro Display", 42))
        else:
            icon_label.setFont(QFont("SF Pro Display", 42))
            icon_label.setStyleSheet("opacity: 0.3;")
        icon_label.setAlignment(Qt.AlignCenter)
        badge_layout.addWidget(icon_label)

        # Name
        name_label = QLabel(name)
        name_label.setFont(QFont("SF Pro Text", 11, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        if is_unlocked:
            name_label.setStyleSheet("color: #1E40AF;")
        else:
            name_label.setStyleSheet("color: #9CA3AF;")
        badge_layout.addWidget(name_label)

        # Description
        desc_label = QLabel(desc)
        desc_label.setFont(QFont("SF Pro Text", 9))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #6B7280;")
        badge_layout.addWidget(desc_label)

        # Lock/Unlock indicator
        if is_unlocked:
            status = QLabel("✓ Unlocked")
            status.setFont(QFont("SF Pro Text", 9, QFont.Bold))
            status.setStyleSheet("color: #10B981;")
        else:
            status = QLabel("🔒 Locked")
            status.setFont(QFont("SF Pro Text", 9))
            status.setStyleSheet("color: #9CA3AF;")
        status.setAlignment(Qt.AlignCenter)
        badge_layout.addWidget(status)

        return badge

    def add_graphs_section(self, habits):
        """Add interactive graphs section"""
        # Graph container
        graph_container = QFrame()
        graph_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #F3F4F6;
                border-radius: 24px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 6)
        graph_container.setGraphicsEffect(shadow)

        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(32, 28, 32, 28)
        graph_layout.setSpacing(24)

        # Header with period selector
        graph_header = QHBoxLayout()

        graph_title = QLabel("📈 Completion Trend")
        graph_title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        graph_title.setStyleSheet("color: #111827; background: transparent;")
        graph_header.addWidget(graph_title)

        graph_header.addStretch()

        # Period buttons
        period_label = QLabel("Period:")
        period_label.setFont(QFont("SF Pro Text", 14, QFont.Medium))
        period_label.setStyleSheet("color: #6B7280; background: transparent;")
        graph_header.addWidget(period_label)

        self.period_combo = QComboBox()
        self.period_combo.addItems(
            ["7 days", "30 days", "3 months", "6 months", "9 months", "1 year"]
        )
        self.period_combo.setCurrentText("7 days")
        self.period_combo.setFont(QFont("SF Pro Text", 13))
        self.period_combo.setFixedHeight(40)
        self.period_combo.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                padding: 6px 16px;
                min-width: 120px;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                selection-background-color: #EEF2FF;
                selection-color: #4F46E5;
            }
        """)
        self.period_combo.currentTextChanged.connect(self.update_graph)
        graph_header.addWidget(self.period_combo)

        graph_layout.addLayout(graph_header)

        # Chart type selector
        chart_type_layout = QHBoxLayout()

        self.chart_type_group = QButtonGroup()

        line_btn = QRadioButton("Line Chart")
        line_btn.setFont(QFont("SF Pro Text", 13))
        line_btn.setChecked(True)
        line_btn.setStyleSheet("""
            QRadioButton {
                color: #374151;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:checked {
                background-color: #6366F1;
                border: 2px solid #6366F1;
                border-radius: 9px;
            }
            QRadioButton::indicator:unchecked {
                background-color: #FFFFFF;
                border: 2px solid #D1D5DB;
                border-radius: 9px;
            }
        """)
        self.chart_type_group.addButton(line_btn, 0)
        chart_type_layout.addWidget(line_btn)

        bar_btn = QRadioButton("Bar Chart")
        bar_btn.setFont(QFont("SF Pro Text", 13))
        bar_btn.setStyleSheet("""
            QRadioButton {
                color: #374151;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:checked {
                background-color: #6366F1;
                border: 2px solid #6366F1;
                border-radius: 9px;
            }
            QRadioButton::indicator:unchecked {
                background-color: #FFFFFF;
                border: 2px solid #D1D5DB;
                border-radius: 9px;
            }
        """)
        self.chart_type_group.addButton(bar_btn, 1)
        chart_type_layout.addWidget(bar_btn)

        chart_type_layout.addStretch()

        self.chart_type_group.buttonClicked.connect(self.update_graph)

        graph_layout.addLayout(chart_type_layout)

        # Chart container
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)

        graph_layout.addWidget(self.chart_container)

        self.content_layout.addWidget(graph_container)

        # Initial graph load
        self.update_graph()

    def add_week_comparison_section(self):
        """Premium Week Comparison Section"""
        comparison_card = QFrame()
        comparison_card.setObjectName("comparisonCard")
        comparison_card.setMinimumHeight(200)
        comparison_card.setStyleSheet("""
            QFrame#comparisonCard {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 8)
        comparison_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(comparison_card)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(18)

        # TITLE
        title = QLabel("📊 This Week vs Last Week")
        title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        layout.addWidget(title)

        # GET DATA
        def get_week_completions(week_offset_days):
            """Calculate total completions for a week"""
            total = 0
            habits = self.habit_service.get_all_habits()

            for day in range(7):
                date = datetime.now() - timedelta(days=week_offset_days + day)
                date_str = date.strftime("%Y-%m-%d")

                for habit in habits:
                    if self.habit_service.is_habit_completed_on_date(
                        habit.id, date_str
                    ):
                        total += 1

            return total

        # This week (days 0-6 ago)
        this_week = get_week_completions(0)

        # Last week (days 7-13 ago)
        last_week = get_week_completions(7)

        # NUMBERS ROW
        numbers_row = QHBoxLayout()
        numbers_row.setAlignment(Qt.AlignCenter)
        numbers_row.setSpacing(40)

        # Last Week
        last_layout = QVBoxLayout()
        last_layout.setSpacing(4)

        last_label = QLabel("Last Week")
        last_label.setFont(QFont("SF Pro Text", 12))
        last_label.setStyleSheet("color: #6B7280;")
        last_label.setAlignment(Qt.AlignCenter)

        last_value = QLabel(str(last_week))
        last_value.setFont(QFont("SF Pro Display", 36, QFont.Bold))
        last_value.setStyleSheet("color: #111827;")
        last_value.setAlignment(Qt.AlignCenter)

        last_layout.addWidget(last_label)
        last_layout.addWidget(last_value)

        # Arrow
        arrow = QLabel("→")
        arrow.setFont(QFont("SF Pro Display", 24))
        arrow.setStyleSheet("color: #9CA3AF;")

        # This Week
        this_layout = QVBoxLayout()
        this_layout.setSpacing(4)

        this_label = QLabel("This Week")
        this_label.setFont(QFont("SF Pro Text", 12))
        this_label.setStyleSheet("color: #6B7280;")
        this_label.setAlignment(Qt.AlignCenter)

        this_value = QLabel(str(this_week))
        this_value.setFont(QFont("SF Pro Display", 36, QFont.Bold))
        this_value.setStyleSheet("color: #111827;")
        this_value.setAlignment(Qt.AlignCenter)

        this_layout.addWidget(this_label)
        this_layout.addWidget(this_value)

        numbers_row.addLayout(last_layout)
        numbers_row.addWidget(arrow)
        numbers_row.addLayout(this_layout)

        layout.addLayout(numbers_row)

        # IMPROVEMENT BADGE
        diff = this_week - last_week

        # Calculate percentage change
        if last_week > 0:
            percent_change = int((diff / last_week) * 100)
        else:
            percent_change = 0 if diff == 0 else 100

        badge = QLabel()
        badge.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedHeight(36)

        if diff > 0:
            badge.setText(f"📈 +{diff} ({percent_change:+d}%)")
            badge.setStyleSheet("""
                QLabel {
                    background-color: #DCFCE7;
                    color: #166534;
                    border-radius: 18px;
                    padding: 8px 20px;
                }
            """)
            insight_text = "🚀 Great job! You're building momentum. Keep it up!"
        elif diff < 0:
            badge.setText(f"📉 {diff} ({percent_change:+d}%)")
            badge.setStyleSheet("""
                QLabel {
                    background-color: #FEE2E2;
                    color: #991B1B;
                    border-radius: 18px;
                    padding: 8px 20px;
                }
            """)
            insight_text = "⚠️ Small setback. Refocus and get back on track this week!"
        else:
            badge.setText("➖ No Change (0%)")
            badge.setStyleSheet("""
                QLabel {
                    background-color: #E5E7EB;
                    color: #374151;
                    border-radius: 18px;
                    padding: 8px 20px;
                }
            """)
            insight_text = "✓ Consistency maintained. Try to improve by 10% this week!"

        layout.addWidget(badge, alignment=Qt.AlignCenter)

        # INSIGHT
        insight = QLabel(insight_text)
        insight.setFont(QFont("SF Pro Text", 13))
        insight.setStyleSheet("color: #6B7280;")
        insight.setAlignment(Qt.AlignCenter)
        insight.setWordWrap(True)
        layout.addWidget(insight)

        self.content_layout.addWidget(comparison_card)

    def add_day_of_week_analysis(self):
        """Day of Week Analysis Section"""
        dow_card = QFrame()
        dow_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 8)
        dow_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(dow_card)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # Title
        title = QLabel("📅 Weekly Pattern")
        title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        layout.addWidget(title)

        subtitle = QLabel("See which days you're most consistent")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitle)

        # Calculate data for each day
        habits = self.habit_service.get_all_habits()
        if not habits:
            return

        day_stats = {i: {"total": 0, "completed": 0} for i in range(7)}

        # Look back 30 days
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            day_of_week = date.weekday()
            date_str = date.strftime("%Y-%m-%d")

            for habit in habits:
                day_stats[day_of_week]["total"] += 1
                if self.habit_service.is_habit_completed_on_date(habit.id, date_str):
                    day_stats[day_of_week]["completed"] += 1

        # Calculate percentages
        days_data = []
        day_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        day_emojis = ["💼", "📊", "🎯", "🚀", "🎉", "🏖️", "☀️"]

        for i in range(7):
            total = day_stats[i]["total"]
            completed = day_stats[i]["completed"]
            percentage = int((completed / total) * 100) if total > 0 else 0
            days_data.append(
                {
                    "name": day_names[i],
                    "emoji": day_emojis[i],
                    "percentage": percentage,
                    "completed": completed,
                    "total": total,
                }
            )

        # Find best and worst days
        best_day = max(days_data, key=lambda x: x["percentage"])
        worst_day = min(days_data, key=lambda x: x["percentage"])

        # Day bars
        for day_data in days_data:
            day_container = QFrame()
            day_container.setFixedHeight(68)

            # Color based on percentage
            if day_data["percentage"] >= 80:
                color = "#10B981"
                bg_color = "#ECFDF5"
                text_color = "#065F46"
                badge = "⭐"
            elif day_data["percentage"] >= 60:
                color = "#F59E0B"
                bg_color = "#FEF3C7"
                text_color = "#92400E"
                badge = "👍"
            else:
                color = "#EF4444"
                bg_color = "#FEE2E2"
                text_color = "#991B1B"
                badge = "⚠️"

            day_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border-left: 4px solid {color};
                    border-radius: 12px;
                }}
            """)

            day_layout = QHBoxLayout(day_container)
            day_layout.setContentsMargins(20, 12, 20, 12)
            day_layout.setSpacing(16)

            # Left: Day name
            left_layout = QVBoxLayout()
            left_layout.setSpacing(2)

            name_label = QLabel(f"{day_data['emoji']} {day_data['name']}")
            name_label.setFont(QFont("SF Pro Display", 15, QFont.Bold))
            name_label.setStyleSheet(f"color: {text_color};")
            left_layout.addWidget(name_label)

            stats_label = QLabel(
                f"{day_data['completed']}/{day_data['total']} completed"
            )
            stats_label.setFont(QFont("SF Pro Text", 11))
            stats_label.setStyleSheet("color: #6B7280;")
            left_layout.addWidget(stats_label)

            day_layout.addLayout(left_layout)

            # Progress bar
            progress_container = QWidget()
            progress_container.setFixedHeight(28)
            progress_layout = QVBoxLayout(progress_container)
            progress_layout.setContentsMargins(0, 0, 0, 0)

            progress_bg = QFrame()
            progress_bg.setFixedHeight(12)
            progress_bg.setStyleSheet("""
                QFrame {{
                    background-color: #F3F4F6;
                    border-radius: 6px;
                }}
            """)

            progress_fill = QFrame(progress_bg)
            fill_width = int(300 * (day_data["percentage"] / 100))
            progress_fill.setGeometry(0, 0, fill_width, 12)
            progress_fill.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 6px;
                }}
            """)

            progress_layout.addWidget(progress_bg)

            day_layout.addWidget(progress_container, stretch=1)

            # Right: Percentage + Badge
            right_layout = QHBoxLayout()
            right_layout.setSpacing(8)

            percentage_label = QLabel(f"{day_data['percentage']}%")
            percentage_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
            percentage_label.setStyleSheet(f"color: {text_color};")
            right_layout.addWidget(percentage_label)

            # Add badge for best/worst
            if day_data["name"] == best_day["name"] and best_day["percentage"] > 0:
                badge_label = QLabel("🏆")
                badge_label.setFont(QFont("SF Pro Display", 20))
                badge_label.setToolTip("Your best day!")
                right_layout.addWidget(badge_label)
            elif (
                day_data["name"] == worst_day["name"]
                and worst_day["percentage"] < best_day["percentage"]
            ):
                badge_label = QLabel("💡")
                badge_label.setFont(QFont("SF Pro Display", 20))
                badge_label.setToolTip("Room for improvement")
                right_layout.addWidget(badge_label)

            day_layout.addLayout(right_layout)

            layout.addWidget(day_container)

        # Insights
        insight_box = QFrame()
        insight_box.setStyleSheet("""
            QFrame {
                background-color: #EEF2FF;
                border-left: 4px solid #6366F1;
                border-radius: 12px;
                padding: 16px;
            }
        """)

        insight_layout = QVBoxLayout(insight_box)
        insight_layout.setContentsMargins(16, 12, 16, 12)
        insight_layout.setSpacing(6)

        insight_title = QLabel("💡 Insights")
        insight_title.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        insight_title.setStyleSheet("color: #4F46E5;")
        insight_layout.addWidget(insight_title)

        insight_text = QLabel(
            f"• Your best day is {best_day['name']} ({best_day['percentage']}%)\n"
            f"• {worst_day['name']} needs attention ({worst_day['percentage']}%)\n"
            f"• Try scheduling important habits on {best_day['name']}"
        )
        insight_text.setFont(QFont("SF Pro Text", 12))
        insight_text.setStyleSheet("color: #1E40AF;")
        insight_text.setWordWrap(True)
        insight_layout.addWidget(insight_text)

        layout.addWidget(insight_box)

        self.content_layout.addWidget(dow_card)

    def add_best_worst_habits(self):
        """Best & Worst Performing Habits Section"""
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setSpacing(24)

        habits = self.habit_service.get_all_habits()
        if not habits:
            return

        # Calculate completion rates for last 30 days
        habit_stats = []
        for habit in habits:
            completions = 0
            for i in range(30):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                if self.habit_service.is_habit_completed_on_date(habit.id, date):
                    completions += 1

            rate = int((completions / 30) * 100)
            streak_info = self.streak_service.get_streak_info(habit.id)

            habit_stats.append(
                {
                    "habit": habit,
                    "rate": rate,
                    "completions": completions,
                    "streak": streak_info.get("current_streak", 0),
                }
            )

        # Sort by rate
        habit_stats.sort(key=lambda x: x["rate"], reverse=True)

        # Best performers
        best_card = QFrame()
        best_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 6)
        best_card.setGraphicsEffect(shadow)

        best_layout = QVBoxLayout(best_card)
        best_layout.setContentsMargins(28, 24, 28, 24)
        best_layout.setSpacing(16)

        best_title = QLabel("🏆 Best Performers")
        best_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        best_title.setStyleSheet("color: #111827;")
        best_layout.addWidget(best_title)

        best_subtitle = QLabel("Top 3 habits - Keep up the great work!")
        best_subtitle.setFont(QFont("SF Pro Text", 12))
        best_subtitle.setStyleSheet("color: #6B7280;")
        best_layout.addWidget(best_subtitle)

        medals = ["🥇", "🥈", "🥉"]
        for i, stat in enumerate(habit_stats[:3]):
            self._add_habit_performance_card(best_layout, stat, medals[i], is_best=True)

        best_layout.addStretch()
        main_layout.addWidget(best_card)

        # Worst performers
        worst_card = QFrame()
        worst_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(25)
        shadow2.setColor(QColor(0, 0, 0, 20))
        shadow2.setOffset(0, 6)
        worst_card.setGraphicsEffect(shadow2)

        worst_layout = QVBoxLayout(worst_card)
        worst_layout.setContentsMargins(28, 24, 28, 24)
        worst_layout.setSpacing(16)

        worst_title = QLabel("⚠️ Needs Attention")
        worst_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        worst_title.setStyleSheet("color: #111827;")
        worst_layout.addWidget(worst_title)

        worst_subtitle = QLabel("Focus on improving these habits")
        worst_subtitle.setFont(QFont("SF Pro Text", 12))
        worst_subtitle.setStyleSheet("color: #6B7280;")
        worst_layout.addWidget(worst_subtitle)

        warnings = ["🔴", "🟠", "🟡"]
        for i, stat in enumerate(habit_stats[-3:][::-1]):
            self._add_habit_performance_card(
                worst_layout, stat, warnings[i], is_best=False
            )

        worst_layout.addStretch()
        main_layout.addWidget(worst_card)

        self.content_layout.addWidget(container)

    def _add_habit_performance_card(self, parent_layout, stat, icon, is_best):
        """Helper to add habit performance card"""
        card = QFrame()
        card.setFixedHeight(85)

        if is_best:
            card.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #ECFDF5, stop:1 #D1FAE5);
                    border-left: 4px solid #10B981;
                    border-radius: 12px;
                }
            """)
            text_color = "#065F46"
        else:
            card.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #FEF2F2, stop:1 #FEE2E2);
                    border-left: 4px solid #EF4444;
                    border-radius: 12px;
                }
            """)
            text_color = "#991B1B"

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(16, 12, 16, 12)
        card_layout.setSpacing(12)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 28))
        card_layout.addWidget(icon_label)

        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        name_label = QLabel(stat["habit"].name)
        name_label.setFont(QFont("SF Pro Display", 15, QFont.Bold))
        name_label.setStyleSheet(f"color: {text_color};")
        info_layout.addWidget(name_label)

        stats_label = QLabel(
            f"{stat['completions']}/30 days • {stat['streak']} day streak"
        )
        stats_label.setFont(QFont("SF Pro Text", 11))
        stats_label.setStyleSheet("color: #6B7280;")
        info_layout.addWidget(stats_label)

        card_layout.addLayout(info_layout, stretch=1)

        # Percentage
        percentage_label = QLabel(f"{stat['rate']}%")
        percentage_label.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        percentage_label.setStyleSheet(f"color: {text_color};")
        card_layout.addWidget(percentage_label)

        parent_layout.addWidget(card)

    def add_time_of_day_difficulty(self):
        """Time of Day + Difficulty Analysis (Side by Side)"""
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setSpacing(24)

        habits = self.habit_service.get_all_habits()
        if not habits:
            return

        # TIME OF DAY CARD
        time_card = QFrame()
        time_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 6)
        time_card.setGraphicsEffect(shadow)

        time_layout = QVBoxLayout(time_card)
        time_layout.setContentsMargins(28, 24, 28, 24)
        time_layout.setSpacing(20)

        time_title = QLabel("⏰ Time of Day")
        time_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        time_title.setStyleSheet("color: #111827;")
        time_layout.addWidget(time_title)

        # Calculate time of day stats (mock data - you can enhance this)
        # For real implementation, you'd need to track completion timestamps
        time_periods = [
            {
                "icon": "🌅",
                "name": "Morning",
                "time": "6-12 AM",
                "rate": 82,
                "color": "#10B981",
            },
            {
                "icon": "☀️",
                "name": "Afternoon",
                "time": "12-6 PM",
                "rate": 68,
                "color": "#F59E0B",
            },
            {
                "icon": "🌙",
                "name": "Evening",
                "time": "6-12 PM",
                "rate": 45,
                "color": "#EF4444",
            },
        ]

        best_time = max(time_periods, key=lambda x: x["rate"])

        for period in time_periods:
            period_card = QFrame()
            period_card.setFixedHeight(75)
            period_card.setStyleSheet(f"""
                QFrame {{
                    background-color: #F9FAFB;
                    border-left: 4px solid {period["color"]};
                    border-radius: 12px;
                }}
            """)

            period_layout = QHBoxLayout(period_card)
            period_layout.setContentsMargins(16, 12, 16, 12)
            period_layout.setSpacing(12)

            # Icon
            icon_label = QLabel(period["icon"])
            icon_label.setFont(QFont("SF Pro Display", 32))
            period_layout.addWidget(icon_label)

            # Info
            info_layout = QVBoxLayout()
            info_layout.setSpacing(2)

            name_label = QLabel(period["name"])
            name_label.setFont(QFont("SF Pro Display", 15, QFont.Bold))
            name_label.setStyleSheet("color: #111827;")
            info_layout.addWidget(name_label)

            time_label = QLabel(period["time"])
            time_label.setFont(QFont("SF Pro Text", 11))
            time_label.setStyleSheet("color: #6B7280;")
            info_layout.addWidget(time_label)

            period_layout.addLayout(info_layout, stretch=1)

            # Percentage
            rate_label = QLabel(f"{period['rate']}%")
            rate_label.setFont(QFont("SF Pro Display", 22, QFont.Bold))
            rate_label.setStyleSheet(f"color: {period['color']};")
            period_layout.addWidget(rate_label)

            if period["name"] == best_time["name"]:
                star_label = QLabel("⭐")
                star_label.setFont(QFont("SF Pro Display", 20))
                period_layout.addWidget(star_label)

            time_layout.addWidget(period_card)

        # Insight
        insight_box = QFrame()
        insight_box.setStyleSheet("""
            QFrame {
                background-color: #EEF2FF;
                border-radius: 12px;
                padding: 12px;
            }
        """)

        insight_layout = QVBoxLayout(insight_box)
        insight_layout.setContentsMargins(12, 10, 12, 10)

        insight_label = QLabel(
            f"💡 You're most productive in the {best_time['name'].lower()}. Schedule important habits early!"
        )
        insight_label.setFont(QFont("SF Pro Text", 12))
        insight_label.setStyleSheet("color: #4F46E5;")
        insight_label.setWordWrap(True)
        insight_layout.addWidget(insight_label)

        time_layout.addWidget(insight_box)
        time_layout.addStretch()

        main_layout.addWidget(time_card)

        # DIFFICULTY CARD
        diff_card = QFrame()
        diff_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(25)
        shadow2.setColor(QColor(0, 0, 0, 20))
        shadow2.setOffset(0, 6)
        diff_card.setGraphicsEffect(shadow2)

        diff_layout = QVBoxLayout(diff_card)
        diff_layout.setContentsMargins(28, 24, 28, 24)
        diff_layout.setSpacing(20)

        diff_title = QLabel("💪 Difficulty Analysis")
        diff_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        diff_title.setStyleSheet("color: #111827;")
        diff_layout.addWidget(diff_title)

        # Calculate difficulty levels
        easy_count = 0
        medium_count = 0
        hard_count = 0

        for habit in habits:
            completions = 0
            for i in range(30):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                if self.habit_service.is_habit_completed_on_date(habit.id, date):
                    completions += 1

            rate = (completions / 30) * 100
            if rate >= 80:
                easy_count += 1
            elif rate >= 50:
                medium_count += 1
            else:
                hard_count += 1

        difficulty_levels = [
            {
                "icon": "🟢",
                "name": "Easy",
                "desc": ">80% completion",
                "count": easy_count,
                "color": "#10B981",
            },
            {
                "icon": "🟡",
                "name": "Medium",
                "desc": "50-80% completion",
                "count": medium_count,
                "color": "#F59E0B",
            },
            {
                "icon": "🔴",
                "name": "Hard",
                "desc": "<50% completion",
                "count": hard_count,
                "color": "#EF4444",
            },
        ]

        for level in difficulty_levels:
            level_card = QFrame()
            level_card.setFixedHeight(75)
            level_card.setStyleSheet("""
                QFrame {
                    background-color: #F9FAFB;
                    border-radius: 12px;
                }
            """)

            level_layout = QHBoxLayout(level_card)
            level_layout.setContentsMargins(16, 12, 16, 12)
            level_layout.setSpacing(12)

            # Circle
            circle_label = QLabel(level["icon"])
            circle_label.setFont(QFont("SF Pro Display", 32))
            level_layout.addWidget(circle_label)

            # Info
            info_layout = QVBoxLayout()
            info_layout.setSpacing(2)

            name_label = QLabel(level["name"])
            name_label.setFont(QFont("SF Pro Display", 15, QFont.Bold))
            name_label.setStyleSheet("color: #111827;")
            info_layout.addWidget(name_label)

            desc_label = QLabel(level["desc"])
            desc_label.setFont(QFont("SF Pro Text", 11))
            desc_label.setStyleSheet("color: #6B7280;")
            info_layout.addWidget(desc_label)

            level_layout.addLayout(info_layout, stretch=1)

            # Count
            count_label = QLabel(f"{level['count']} habits")
            count_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
            count_label.setStyleSheet(f"color: {level['color']};")
            level_layout.addWidget(count_label)

            diff_layout.addWidget(level_card)

        # Recommendation
        rec_box = QFrame()
        rec_box.setStyleSheet("""
            QFrame {
                background-color: #FEF3C7;
                border-radius: 12px;
                padding: 12px;
            }
        """)

        rec_layout = QVBoxLayout(rec_box)
        rec_layout.setContentsMargins(12, 10, 12, 10)

        if hard_count > 0:
            rec_text = f"💡 Focus on improving 1-2 hard habits at a time. Small wins build momentum!"
        elif medium_count > 0:
            rec_text = (
                f"💡 Great job! Push {medium_count} medium habit(s) to 80%+ completion."
            )
        else:
            rec_text = (
                f"💡 Excellent! All habits are easy. Consider adding new challenges!"
            )

        rec_label = QLabel(rec_text)
        rec_label.setFont(QFont("SF Pro Text", 12))
        rec_label.setStyleSheet("color: #92400E;")
        rec_label.setWordWrap(True)
        rec_layout.addWidget(rec_label)

        diff_layout.addWidget(rec_box)
        diff_layout.addStretch()

        main_layout.addWidget(diff_card)

        self.content_layout.addWidget(container)

    def update_graph(self):
        """Update graph based on selected period"""
        # Clear current chart
        while self.chart_layout.count():
            item = self.chart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        period_text = self.period_combo.currentText()

        # Calculate days
        period_map = {
            "7 days": 7,
            "30 days": 30,
            "3 months": 90,
            "6 months": 180,
            "9 months": 270,
            "1 year": 365,
        }

        days = period_map.get(period_text, 30)

        # Get data
        habits = self.habit_service.get_all_habits()
        data = []
        labels = []

        for i in range(days):
            date = datetime.now() - timedelta(days=days - 1 - i)
            date_str = date.strftime("%Y-%m-%d")

            completions = sum(
                1
                for h in habits
                if self.habit_service.is_habit_completed_on_date(h.id, date_str)
            )
            data.append(completions)

            # Label formatting based on period
            if days <= 30:
                labels.append(date.strftime("%b %d"))
            elif days <= 90:
                if i % 3 == 0:  # Every 3 days
                    labels.append(date.strftime("%b %d"))
                else:
                    labels.append("")
            else:
                if i % 7 == 0:  # Every week
                    labels.append(date.strftime("%b %d"))
                else:
                    labels.append("")

        # Create chart based on type
        chart_type = self.chart_type_group.checkedId()

        if chart_type == 0:  # Line chart
            chart = LineChart(data, labels, "Habit Completions")
        else:  # Bar chart
            chart = BarChart(data, labels, "Habit Completions")

        self.chart_layout.addWidget(chart)

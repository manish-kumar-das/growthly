# 🎯 Habit Tracker (Growthly)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.5%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)

A powerful, elegant, and modern desktop application for tracking daily habits, achieving goals, and building consistency.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [Roadmap](#-roadmap)

</div>

---

## ✨ Features

- ✅ **Track Daily & Weekly Habits** - Efficiently manage your routines with categories and detailed descriptions.
- 🔥 **Advanced Streak Tracking** - Monitor your consistency with real-time streak calculations and visual indicators.
- 🎯 **Goal Management** - Set specific targets for streaks or total completions. Growthly tracks your progress automatically.
- 📊 **Analytics Dashboard** - Visualize your progress with completion rate charts, weekly activity logs, and habit distribution donut charts.
- 🌗 **Premium Theme System** - Seamlessly switch between Light and Dark modes with a modern, theme-aware UI.
- 👤 **Profile Customization** - Personalized user experience with professional-grade circular avatar cropping and profile editing.
- 🔔 **Smart Notifications** - Custom daily reminders and goal completion alerts to keep you on track.
- 🗑️ **Trash & Restore** - Safely delete habits with the ability to restore them from the trash if you change your mind.
- 🎨 **Modern Design** - Premium aesthetic featuring SF Pro typography, elegant layouts, and smooth micro-interactions.
- 💾 **Local & Private** - Your data stays on your machine in a secure SQLite database.

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/manish-kumar-das/habit-tracker.git
cd habit-tracker
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

---

## 📖 Usage

### Adding & Managing Habits
1. Click **"➕ Add New Habit"** to create a habit with category and frequency.
2. Organise habits into **Categories** (e.g., Health, Work, Mindset).
3. Easily **Edit** or **Delete** habits. Deleted habits can be recovered from the Trash.

### Tracking Progress
- **Check** the box next to a habit to complete it for today.
- Use the **Analytics** tab to view deep-dive statistics of your performance.
- Track your **Goals** to stay motivated and hit new milestones.

### Customization
- Toggle between **Dark and Light mode** using the theme switch on the dashboard.
- Update your **Profile** and avatar from the Profile section for a personalized experience.
- Configure notification times in settings (Reminders).

---

## 🗂️ Project Structure
```
habit-tracker/
├── app/
│   ├── views/           # UI components (Windows, Dialogs, Content Views)
│   ├── themes/          # Modern theme system (Dark/Light schemas)
│   ├── widgets/         # Custom, reusable UI elements
│   ├── models/          # Data models (Habit, Goal, Profile)
│   ├── services/        # Business logic (HabitService, GoalService, etc.)
│   ├── db/              # Database interaction layer
│   ├── utils/           # Helper functions & Image processing
│   └── assets/          # Icons, fonts, and static assets
├── data/                # Database and user profile storage
├── docs/                # Extended documentation and roadmap
├── main.py              # Application entry point
├── requirements.txt     # Dependencies
└── README.md
```

---

## 🛠️ Tech Stack

- **GUI:** PySide6 (Qt for Python)
- **Database:** SQLite
- **Styling:** Dynamic Theme Engine
- **Image Processing:** OpenCV/PIL for avatar cropping

---

## 🗺️ Roadmap

**Recently Completed (v1.0.0):**
- [x] Full Dark Mode support
- [x] Goal tracking system
- [x] Analytics dashboard with charts
- [x] Profile management and avatar cropping
- [x] Categories and habit management
- [x] Daily reminders and notification engine

**Coming Soon:**
- [ ] Data Export/Import (CSV, JSON)
- [ ] Calendar heatmap view
- [ ] Weekly/Monthly trend analysis
- [ ] Desktop widgets
- [ ] Multi-user support

---

## 🤝 Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## 🐛 Bug Reports

Found a bug? Please open an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- Your environment (OS, Python version)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Manish Kumar Das**
- GitHub: [@manish-kumar-das](https://github.com/manish-kumar-das)
- Email: [manishkumardas7890@gmail.com](mailto:manishkumardas7890@gmail.com)

---

## 🙏 Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython/)
- Inspired by the power of consistent daily habits
- Thanks to the Python and Qt communities

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a star on GitHub!

---

<div align="center">

**Made with ❤️ and Python**

*Track your habits. Build consistency. Achieve your goals.*

</div>

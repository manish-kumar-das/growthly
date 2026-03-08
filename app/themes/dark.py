"""
Dark Theme Colors
OLED-friendly dark interface for nighttime use
Based on the dark mode design in your screenshot
"""
from .base_theme import BaseTheme


class DarkTheme(BaseTheme):
    """
    Dark mode color palette
    Optimized for low-light environments and OLED screens
    """
    
    # ===== BACKGROUNDS =====
    BG_PRIMARY = "#1A1F2E"           # Main background (dark blue-gray)
    BG_CARD = "#242933"              # Card backgrounds (elevated)
    BG_SIDEBAR = "#1E1B2E"           # Sidebar (purple-tinted dark)
    BG_SIDEBAR_SELECTED = "#2D1B4E"  # Selected nav item (purple)
    BG_SIDEBAR_HOVER = "#251A3D"     # Hover state
    
    # ===== TEXT COLORS =====
    TEXT_PRIMARY = "#F8F9FA"         # Main headings (bright white)
    TEXT_SECONDARY = "#B8BFCC"       # Body text (light gray)
    TEXT_TERTIARY = "#8B92A0"        # Muted labels (medium gray)
    TEXT_ON_PURPLE = "#FFFFFF"       # Text on purple backgrounds
    TEXT_ON_DARK = "#F8F9FA"         # Text on dark backgrounds
    
    # ===== PURPLE PALETTE (Brighter for dark mode) =====
    PURPLE_50 = "#2D1B4E"            # Darkest purple
    PURPLE_100 = "#3D2566"
    PURPLE_200 = "#4E3280"
    PURPLE_300 = "#6B46C1"
    PURPLE_400 = "#8B5CF6"
    PURPLE_500 = "#A78BFA"           # Primary purple (lighter)
    PURPLE_600 = "#C4B5FD"           # Lighter purple
    PURPLE_700 = "#DDD6FE"           # Lightest purple
    
    # ===== ACCENT COLORS (Brighter/More Vibrant) =====
    GREEN_50 = "#064E3B"
    GREEN_500 = "#34D399"            # Success (brighter green)
    GREEN_600 = "#6EE7B7"
    
    BLUE_50 = "#1E3A8A"
    BLUE_500 = "#60A5FA"             # Info (brighter blue)
    BLUE_600 = "#93C5FD"
    
    ORANGE_50 = "#7C2D12"
    ORANGE_500 = "#FB923C"           # Warning (brighter orange)
    ORANGE_600 = "#FDBA74"
    
    RED_50 = "#7F1D1D"
    RED_500 = "#F87171"              # Error (brighter red)
    RED_600 = "#FCA5A5"
    
    # ===== BORDERS & DIVIDERS =====
    BORDER_LIGHT = "#2D3748"         # Subtle borders
    BORDER_DEFAULT = "#374151"       # Default borders
    BORDER_STRONG = "#4B5563"        # Strong borders
    BORDER_PURPLE = "#6B46C1"        # Purple borders
    
    # ===== SHADOWS (Darker for dark mode) =====
    SHADOW_SM = "rgba(0, 0, 0, 0.3)"
    SHADOW_MD = "rgba(0, 0, 0, 0.5)"
    SHADOW_LG = "rgba(0, 0, 0, 0.7)"
    SHADOW_XL = "rgba(0, 0, 0, 0.9)"
    SHADOW_PURPLE = "rgba(139, 92, 246, 0.3)"
    
    # ===== GRADIENTS =====
    GRADIENT_PURPLE = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #A78BFA, stop:1 #8B5CF6)"
    GRADIENT_PURPLE_VIBRANT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #A78BFA, stop:1 #C084FC)"
    GRADIENT_COMPLETION = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7C3AED, stop:1 #C084FC)"
    
    # ===== SPECIAL STATES =====
    OVERLAY_LIGHT = "rgba(255, 255, 255, 0.05)"
    OVERLAY_DARK = "rgba(0, 0, 0, 0.7)"
    HOVER_OVERLAY = "rgba(167, 139, 250, 0.1)"
    PRESSED_OVERLAY = "rgba(167, 139, 250, 0.2)"
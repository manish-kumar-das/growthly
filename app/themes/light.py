"""
Light Theme Colors
Clean, bright interface for daytime use
"""
from .base_theme import BaseTheme


class LightTheme(BaseTheme):
    """
    Light mode color palette
    Optimized for bright environments and daytime use
    """
    
    # ===== BACKGROUNDS =====
    BG_PRIMARY = "#F5F7FA"           # Main app background
    BG_CARD = "#FFFFFF"              # Card backgrounds
    BG_SIDEBAR = "#7C3AED"           # Sidebar purple gradient
    BG_SIDEBAR_SELECTED = "#6D28D9"  # Selected nav item
    BG_SIDEBAR_HOVER = "#8B5CF6"     # Hover state
    
    # ===== TEXT COLORS =====
    TEXT_PRIMARY = "#0F172A"         # Main headings, important text
    TEXT_SECONDARY = "#64748B"       # Body text, descriptions
    TEXT_TERTIARY = "#94A3B8"        # Muted labels, captions
    TEXT_ON_PURPLE = "#FFFFFF"       # Text on purple backgrounds
    TEXT_ON_DARK = "#F8F9FA"         # Text on dark backgrounds
    
    # ===== PURPLE PALETTE =====
    PURPLE_50 = "#F5F3FF"
    PURPLE_100 = "#EDE9FE"
    PURPLE_200 = "#DDD6FE"
    PURPLE_300 = "#C4B5FD"
    PURPLE_400 = "#A78BFA"
    PURPLE_500 = "#8B5CF6"            # Primary purple
    PURPLE_600 = "#7C3AED"            # Darker purple
    PURPLE_700 = "#6D28D9"            # Darkest purple
    
    # ===== ACCENT COLORS =====
    GREEN_50 = "#ECFDF5"
    GREEN_500 = "#10B981"             # Success green
    GREEN_600 = "#059669"
    
    BLUE_50 = "#EFF6FF"
    BLUE_500 = "#3B82F6"              # Info blue
    BLUE_600 = "#2563EB"
    
    ORANGE_50 = "#FFF7ED"
    ORANGE_500 = "#F59E0B"            # Warning orange
    ORANGE_600 = "#D97706"
    
    RED_50 = "#FEF2F2"
    RED_500 = "#EF4444"               # Error red
    RED_600 = "#DC2626"
    
    # ===== BORDERS & DIVIDERS =====
    BORDER_LIGHT = "#E2E8F0"
    BORDER_DEFAULT = "#CBD5E1"
    BORDER_STRONG = "#94A3B8"
    BORDER_PURPLE = "#7C3AED"
    
    # ===== SHADOWS =====
    SHADOW_SM = "rgba(0, 0, 0, 0.05)"
    SHADOW_MD = "rgba(0, 0, 0, 0.1)"
    SHADOW_LG = "rgba(0, 0, 0, 0.15)"
    SHADOW_XL = "rgba(0, 0, 0, 0.25)"
    SHADOW_PURPLE = "rgba(124, 58, 237, 0.25)"
    
    # ===== GRADIENTS =====
    GRADIENT_PURPLE = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8B5CF6, stop:1 #7C3AED)"
    GRADIENT_PURPLE_VIBRANT = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8B5CF6, stop:1 #A855F7)"
    GRADIENT_COMPLETION = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667EEA, stop:1 #C084FC)"
    
    # ===== SPECIAL STATES =====
    OVERLAY_LIGHT = "rgba(255, 255, 255, 0.5)"
    OVERLAY_DARK = "rgba(0, 0, 0, 0.5)"
    HOVER_OVERLAY = "rgba(124, 58, 237, 0.05)"
    PRESSED_OVERLAY = "rgba(124, 58, 237, 0.1)"
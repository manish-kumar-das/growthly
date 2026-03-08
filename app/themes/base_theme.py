"""
Base Theme Structure
Defines the contract all themes must follow
"""


class BaseTheme:
    """
    Base class that all themes inherit from
    Ensures consistency across themes
    
    All themes must define these colors
    """
    
    # ===== BACKGROUNDS =====
    BG_PRIMARY = None       # Main app background
    BG_CARD = None          # Card backgrounds
    BG_SIDEBAR = None       # Sidebar background
    BG_SIDEBAR_SELECTED = None  # Selected navigation item
    BG_SIDEBAR_HOVER = None     # Hover state for sidebar
    
    # ===== TEXT COLORS =====
    TEXT_PRIMARY = None         # Main headings, important text
    TEXT_SECONDARY = None       # Body text, descriptions
    TEXT_TERTIARY = None        # Muted labels, captions
    TEXT_ON_PURPLE = None       # Text on purple backgrounds
    TEXT_ON_DARK = None         # Text on dark backgrounds
    
    # ===== PURPLE PALETTE =====
    PURPLE_50 = None
    PURPLE_100 = None
    PURPLE_200 = None
    PURPLE_300 = None
    PURPLE_400 = None
    PURPLE_500 = None       # Primary purple
    PURPLE_600 = None
    PURPLE_700 = None
    
    # ===== ACCENT COLORS =====
    GREEN_50 = None
    GREEN_500 = None        # Success green
    GREEN_600 = None
    
    BLUE_50 = None
    BLUE_500 = None         # Info blue
    BLUE_600 = None
    
    ORANGE_50 = None
    ORANGE_500 = None       # Warning orange
    ORANGE_600 = None
    
    RED_50 = None
    RED_500 = None          # Error red
    RED_600 = None
    
    # ===== BORDERS & DIVIDERS =====
    BORDER_LIGHT = None
    BORDER_DEFAULT = None
    BORDER_STRONG = None
    BORDER_PURPLE = None
    
    # ===== SHADOWS =====
    SHADOW_SM = None
    SHADOW_MD = None
    SHADOW_LG = None
    SHADOW_XL = None
    SHADOW_PURPLE = None
    
    # ===== GRADIENTS =====
    GRADIENT_PURPLE = None
    GRADIENT_PURPLE_VIBRANT = None
    GRADIENT_COMPLETION = None
    
    # ===== SPECIAL STATES =====
    OVERLAY_LIGHT = None
    OVERLAY_DARK = None
    HOVER_OVERLAY = None
    PRESSED_OVERLAY = None
    
    def validate(self):
        """
        Validate that all required colors are defined
        
        Returns:
            bool: True if valid, raises ValueError if not
        """
        missing = []
        for attr in dir(self):
            if not attr.startswith('_') and attr.isupper():
                if getattr(self, attr) is None:
                    missing.append(attr)
        
        if missing:
            raise ValueError(f"Theme missing colors: {', '.join(missing)}")
        
        return True
    
    def get_all_colors(self):
        """
        Get dictionary of all theme colors
        
        Returns:
            dict: {color_name: color_value}
        """
        colors = {}
        for attr in dir(self):
            if not attr.startswith('_') and attr.isupper():
                colors[attr] = getattr(self, attr)
        return colors
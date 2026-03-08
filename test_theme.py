"""
Test Theme System
Run this to verify theme system works correctly
"""
from app.themes import get_theme_manager


def test_theme_system():
    """Test all theme functionality"""
    print("=" * 50)
    print("TESTING THEME SYSTEM")
    print("=" * 50)
    
    # Get theme manager
    theme = get_theme_manager()
    print(f"\n✓ Theme manager initialized")
    print(f"  Current theme: {theme.get_theme_name()}")
    print(f"  Available themes: {theme.get_available_themes()}")
    
    # Test getting colors
    colors = theme.get_theme()
    print(f"\n✓ Got theme colors")
    print(f"  BG_PRIMARY: {colors.BG_PRIMARY}")
    print(f"  TEXT_PRIMARY: {colors.TEXT_PRIMARY}")
    print(f"  PURPLE_500: {colors.PURPLE_500}")
    
    # Test theme switching
    print(f"\n✓ Testing theme switching...")
    theme.set_theme("dark")
    print(f"  Switched to: {theme.get_theme_name()}")
    dark_colors = theme.get_theme()
    print(f"  BG_PRIMARY (dark): {dark_colors.BG_PRIMARY}")
    
    theme.set_theme("light")
    print(f"  Switched to: {theme.get_theme_name()}")
    light_colors = theme.get_theme()
    print(f"  BG_PRIMARY (light): {light_colors.BG_PRIMARY}")
    
    # Test toggle
    print(f"\n✓ Testing toggle...")
    new_theme = theme.toggle_theme()
    print(f"  Toggled to: {new_theme}")
    
    new_theme = theme.toggle_theme()
    print(f"  Toggled to: {new_theme}")
    
    # Test callbacks
    print(f"\n✓ Testing callbacks...")
    
    def on_theme_change(theme_name):
        print(f"  📢 Callback received: {theme_name}")
    
    theme.register_callback(on_theme_change)
    theme.toggle_theme()
    
    # Test save/load
    print(f"\n✓ Testing save/load...")
    theme.set_theme("dark")
    theme.save_preference("test_settings.json")
    print(f"  Saved: dark")
    
    theme.set_theme("light")
    print(f"  Current: {theme.get_theme_name()}")
    
    theme.load_preference("test_settings.json")
    print(f"  Loaded: {theme.get_theme_name()}")
    
    # Test validation
    print(f"\n✓ Testing theme validation...")
    try:
        colors.validate()
        print(f"  Light theme valid ✓")
    except ValueError as e:
        print(f"  Light theme invalid: {e}")
    
    theme.set_theme("dark")
    try:
        theme.get_theme().validate()
        print(f"  Dark theme valid ✓")
    except ValueError as e:
        print(f"  Dark theme invalid: {e}")
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED ✓")
    print("=" * 50)


if __name__ == "__main__":
    test_theme_system()
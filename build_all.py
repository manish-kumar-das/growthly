"""
Unified Build Script for Growthly
Detects platform and builds accordingly
Automatically installs PyInstaller if needed
"""
import os
import sys
import shutil
import platform
import subprocess


def check_and_install_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            print("\nPlease install manually:")
            print("  pip install pyinstaller")
            return False


def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    if not os.path.exists('requirements.txt'):
        print("⚠️  requirements.txt not found")
        return True
    
    try:
        # Check if all requirements are installed
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'check'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ All requirements satisfied")
            return True
        else:
            print("⚠️  Some requirements may be missing")
            print("\nInstalling requirements from requirements.txt...")
            
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            print("✅ Requirements installed!")
            return True
            
    except Exception as e:
        print(f"⚠️  Could not verify requirements: {e}")
        return True


def get_platform():
    """Detect current platform"""
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Darwin':
        return 'macos'
    elif system == 'Linux':
        return 'linux'
    else:
        raise Exception(f"Unsupported platform: {system}")


def clean_build():
    """Remove previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed {folder}/")
    
    for file in ['Growthly.spec']:
        if os.path.exists(file):
            os.remove(file)
            print(f"  Removed {file}")


def build_windows():
    """Build Windows executable"""
    print("🪟 Building for Windows...")
    
    import PyInstaller.__main__
    
    # Check if icon exists
    icon_path = 'app/assets/icons/icon.ico' if os.path.exists('app/assets/icons/icon.ico') else None
    
    args = [
        'main.py',
        '--name=Growthly',
        '--onefile',
        '--windowed',
        '--add-data=app;app',
        '--add-data=data;data',
        '--clean',
        '--noconfirm',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=PySide6.QtSvg',
    ]
    
    if icon_path:
        args.append(f'--icon={icon_path}')
        print(f"  Using icon: {icon_path}")
    else:
        print("  ⚠️  No icon.ico found, building without icon")
    
    PyInstaller.__main__.run(args)
    
    exe_path = 'dist/Growthly.exe'
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n✅ Windows build complete!")
        print(f"📦 Executable: {exe_path}")
        print(f"📊 Size: {size_mb:.1f} MB")
        print(f"💡 Test: {exe_path}")


def build_linux():
    """Build Linux executable"""
    print("🐧 Building for Linux...")
    
    import PyInstaller.__main__
    
    # Check if icon exists
    icon_path = 'app/assets/icons/icon.png' if os.path.exists('app/assets/icons/icon.png') else None
    
    args = [
        'main.py',
        '--name=Growthly',
        '--onefile',
        '--windowed',
        '--add-data=app:app',
        '--add-data=data:data',
        '--clean',
        '--noconfirm',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=PySide6.QtSvg',
    ]
    
    if icon_path:
        args.append(f'--icon={icon_path}')
        print(f"  Using icon: {icon_path}")
    else:
        print("  ⚠️  No icon.png found, building without icon")
    
    PyInstaller.__main__.run(args)
    
    exe_path = 'dist/Growthly'
    if os.path.exists(exe_path):
        # Make executable
        os.chmod(exe_path, 0o755)
        
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n✅ Linux build complete!")
        print(f"📦 Executable: {exe_path}")
        print(f"📊 Size: {size_mb:.1f} MB")
        print(f"💡 Test: ./{exe_path}")


def build_macos():
    """Build macOS application"""
    print("🍎 Building for macOS...")
    
    import PyInstaller.__main__
    
    # Check if icon exists
    icon_path = 'app/assets/icons/icon.icns' if os.path.exists('app/assets/icons/icon.icns') else None
    
    args = [
        'main.py',
        '--name=Growthly',
        '--onefile',
        '--windowed',
        '--add-data=app:app',
        '--add-data=data:data',
        '--osx-bundle-identifier=com.growthly.app',
        '--clean',
        '--noconfirm',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=PySide6.QtSvg',
    ]
    
    if icon_path:
        args.append(f'--icon={icon_path}')
        print(f"  Using icon: {icon_path}")
    else:
        print("  ⚠️  No icon.icns found, building without icon")
    
    PyInstaller.__main__.run(args)
    
    app_path = 'dist/Growthly.app'
    if os.path.exists(app_path):
        print("\n✅ macOS build complete!")
        print(f"📦 Application: {app_path}")
        print(f"💡 Test: open {app_path}")


def main():
    """Main build function"""
    print("=" * 70)
    print("  GROWTHLY - BUILD SCRIPT")
    print("=" * 70)
    print()
    
    # Detect platform
    current_platform = get_platform()
    print(f"🖥️  Detected platform: {current_platform.upper()}")
    print()
    
    # Check and install PyInstaller
    if not check_and_install_pyinstaller():
        sys.exit(1)
    
    print()
    
    # Check requirements
    check_requirements()
    
    print()
    
    # Verify main.py exists
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found!")
        print("Make sure you're running this script from the project root directory.")
        sys.exit(1)
    
    # Verify app directory exists
    if not os.path.exists('app'):
        print("❌ Error: app/ directory not found!")
        print("Make sure you're running this script from the project root directory.")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    print()
    
    # Build for current platform
    try:
        if current_platform == 'windows':
            build_windows()
        elif current_platform == 'linux':
            build_linux()
        elif current_platform == 'macos':
            build_macos()
        
        print()
        print("=" * 70)
        print("  BUILD SUCCESS! 🎉")
        print()
        
    except Exception as e:
        print()
        print("=" * 70)
        print("  BUILD FAILED! ❌")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("Common fixes:")
        print("  - Ensure app runs: python main.py")
        print("  - Check requirements: pip install -r requirements.txt")
        print("  - Verify project structure:")
        print("    ├── main.py")
        print("    ├── app/")
        print("    └── data/")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
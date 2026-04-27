#!/usr/bin/env python3
"""
Dependency Checker and Auto-Installer for EchoNote
Checks if all required packages are installed, and installs missing ones.
"""

import subprocess
import sys
from pathlib import Path
import importlib.util


def read_requirements(req_file="requirements.txt"):
    """Read and parse requirements.txt file."""
    req_path = Path(req_file)
    
    if not req_path.exists():
        print(f"❌ Error: {req_file} not found!")
        return []
    
    packages = []
    with open(req_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                # Handle version specifiers (e.g., "package>=1.0.0")
                package_name = line.split('>=')[0].split('<=')[0].split('==')[0].split('!=')[0].split('>')[0].split('<')[0].strip()
                packages.append((package_name, line))
    
    return packages


def check_package_installed(package_name):
    """Check if a package is installed."""
    try:
        importlib.util.find_spec(package_name)
        return True
    except (ImportError, ModuleNotFoundError):
        return False


def install_packages(packages):
    """Install missing packages using pip."""
    if not packages:
        print("✅ All dependencies are already installed!")
        return True
    
    print(f"\n📦 Installing {len(packages)} missing package(s)...\n")
    
    try:
        for package_spec in packages:
            print(f"  Installing: {package_spec}")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_spec],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"    ❌ Failed to install {package_spec}")
                print(f"       Error: {result.stderr}")
                return False
            else:
                print(f"    ✅ Successfully installed {package_spec}")
        
        print("\n✅ All dependencies installed successfully!")
        return True
    
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False


def main():
    """Main function to check and install dependencies."""
    print("=" * 60)
    print("🔍 EchoNote Dependency Checker & Installer")
    print("=" * 60)
    print()
    
    # Read requirements
    requirements = read_requirements("requirements.txt")
    
    if not requirements:
        print("❌ No dependencies found in requirements.txt")
        return 1
    
    print(f"📋 Found {len(requirements)} required package(s):\n")
    
    # Check each package
    missing_packages = []
    for package_name, package_spec in requirements:
        if check_package_installed(package_name):
            print(f"  ✅ {package_name} — Already installed")
        else:
            print(f"  ⚠️  {package_name} — NOT installed")
            missing_packages.append(package_spec)
    
    print()
    
    # If all installed, we're done
    if not missing_packages:
        print("=" * 60)
        print("✅ All dependencies are satisfied!")
        print("=" * 60)
        return 0
    
    # Ask for confirmation before installing
    print("=" * 60)
    response = input(f"Install {len(missing_packages)} missing package(s)? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("❌ Installation cancelled.")
        return 1
    
    print()
    
    # Install missing packages
    success = install_packages(missing_packages)
    
    print("=" * 60)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Meow Valley - Automatic Setup Script
Memastikan semua dependencies terinstall dengan benar untuk semua OS
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

class Setup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.os_type = platform.system()
        self.python_executable = sys.executable
        
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_step(self, step_num, text):
        """Print step message"""
        print(f"\n📍 Step {step_num}: {text}")
        print("-" * 60)
    
    def check_python_version(self):
        """Cek versi Python"""
        self.print_step(1, "Checking Python Version")
        
        version = sys.version_info
        # Don't force exit on older Python versions — only warn the user.
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("⚠️ Warning: Python 3.8+ recommended but not strictly required.")
            print(f"   Anda menggunakan: Python {version.major}.{version.minor}.{version.micro}")
        else:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")

        print(f"   Location: {self.python_executable}")
    
    def check_venv_exists(self):
        """Check if virtual environment already exists"""
        if self.venv_path.exists():
            print(f"✅ Virtual environment sudah ada di: {self.venv_path}")
            return True
        return False
    
    def create_venv(self):
        """Create virtual environment"""
        self.print_step(2, "Setting up Virtual Environment")
        
        if self.check_venv_exists():
            return
        
        print(f"📦 Creating virtual environment di: {self.venv_path}")
        try:
            subprocess.check_call(
                [self.python_executable, "-m", "venv", str(self.venv_path)]
            )
            print("✅ Virtual environment berhasil dibuat")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error saat membuat virtual environment: {e}")
            sys.exit(1)
    
    def get_pip_executable(self):
        """Get pip executable path based on OS"""
        if self.os_type == "Windows":
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:  # macOS, Linux
            return str(self.venv_path / "bin" / "pip")
    
    def get_python_executable(self):
        """Get python executable path based on OS"""
        if self.os_type == "Windows":
            return str(self.venv_path / "Scripts" / "python.exe")
        else:  # macOS, Linux
            return str(self.venv_path / "bin" / "python")
    
    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        self.print_step(3, "Upgrading pip")
        
        pip_exe = self.get_pip_executable()
        print("📦 Upgrading pip to latest version...")
        
        try:
            subprocess.check_call(
                [pip_exe, "install", "--upgrade", "pip"]
            )
            print("✅ pip upgraded successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not upgrade pip: {e}")
            print("   Continuing with current pip version...")
    
    def install_requirements(self):
        """Install requirements from file"""
        self.print_step(4, "Installing Game Dependencies")
        
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print(f"❌ Error: {requirements_file} tidak ditemukan")
            sys.exit(1)
        
        pip_exe = self.get_pip_executable()
        print(f"📦 Installing dependencies dari {requirements_file}...")
        
        try:
            subprocess.check_call(
                [pip_exe, "install", "-r", str(requirements_file)]
            )
            print("✅ Dependencies berhasil diinstall")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error saat install dependencies: {e}")
            print("\n   Coba install manual dengan:")
            print(f"   {pip_exe} install -r requirements.txt")
            sys.exit(1)
    
    def verify_imports(self):
        """Verify semua module bisa diimport"""
        self.print_step(5, "Verifying Imports")
        
        required_modules = {
            'pygame': 'pygame',
            'pytmx': 'pytmx',
            'pytmx.util_pygame': 'pytmx.util_pygame'
        }
        
        all_ok = True
        for module_name, display_name in required_modules.items():
            try:
                __import__(module_name)
                print(f"  ✅ {display_name}")
            except ImportError as e:
                print(f"  ❌ {display_name}: {e}")
                all_ok = False
        
        return all_ok
    
    def print_next_steps(self):
        """Print next steps untuk user"""
        python_exe = self.get_python_executable()
        
        self.print_header("✅ Setup Complete!")
        
        print("\n🎮 Untuk menjalankan game:\n")
        
        if self.os_type == "Windows":
            print("   Option 1 (dari root directory):")
            print(f"   python code/main.py\n")
            print("   Option 2 (setelah activate venv):")
            print(f"   venv\\Scripts\\activate")
            print(f"   cd code && python main.py")
        else:  # macOS, Linux
            print("   Option 1 (dari root directory):")
            print(f"   {python_exe} code/main.py\n")
            print("   Option 2 (setelah activate venv):")
            print(f"   source venv/bin/activate")
            print(f"   cd code && python main.py")
        
        print("\n📋 Verify installation:\n")
        print(f"   {python_exe} -c \"import pygame, pytmx; print('✅ OK')\"")
        
        print("\n" + "=" * 60)
    
    def run(self):
        """Main setup flow"""
        self.print_header("Meow Valley - Automatic Setup")
        
        print(f"\n🖥️  Operating System: {self.os_type}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        
        # Step 1: Check Python version
        self.check_python_version()
        
        # Step 2: Create virtual environment
        self.create_venv()
        
        # Step 3: Upgrade pip
        self.upgrade_pip()
        
        # Step 4: Install dependencies
        self.install_requirements()
        
        # Step 5: Verify imports
        if not self.verify_imports():
            print("\n❌ Beberapa module gagal diimport")
            print("   Coba reinstall:")
            pip_exe = self.get_pip_executable()
            print(f"   {pip_exe} install --force-reinstall pygame pytmx")
            sys.exit(1)
        
        # Print next steps
        self.print_next_steps()

def main():
    """Entry point"""
    try:
        setup = Setup()
        setup.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup dibatalkan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


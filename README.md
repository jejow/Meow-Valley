# Meow Valley 🌾

A farming simulation game built with Pygame and Tiled maps.

## 🛠️ Installation & Setup

Choose your operating system below for detailed setup instructions.

---

## macOS Setup

### Prerequisites

- macOS 10.13 or later (Intel or Apple Silicon)
- Python 3.8 or later (3.12 recommended)

### Step 1: Install System Dependencies

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install SDL2 (required for pygame)
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer

# Install Python 3.12
brew install python@3.12
```

### Step 2: Extract/Clone Project

```bash
# Option A: If you have a project archive
cd ~/Desktop
unzip Meow-Valley.zip
cd Meow-Valley

# Option B: If you have a git repository
cd ~/Desktop
git clone <your-repository-url>
cd Meow-Valley
```

### Step 3: Run Automatic Setup

```bash
# From the project root directory
python3 setup.py
```

This will automatically:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify imports
- ✅ Ready to play!

### Step 4: Run the Game

```bash
# Using the python from virtual environment
venv/bin/python code/main.py

# Or activate venv first
source venv/bin/activate
python code/main.py
```

### For Apple Silicon (M1/M2/M3) - Optimized Setup

```bash
# Install Homebrew dependencies
arch -arm64 brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer

# Run automatic setup (will create native architecture venv)
python3 setup.py

# Run game with native architecture
venv/bin/python code/main.py
```

### macOS Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'pygame'`

```bash
# Solution: Reinstall pygame
pip install pygame --force-reinstall --no-cache-dir
```

**Problem:** No sound output

```bash
# Solution: Reinstall SDL2 mixer
brew reinstall sdl2_mixer
pip install pygame --no-cache-dir
```

**Problem:** Font loading error

```bash
# Verify font file exists
ls -la font/LycheeSoda.ttf

# Check permissions
chmod 644 font/LycheeSoda.ttf
```

---

## Windows Setup

### Prerequisites

- Windows 10 or 11
- Python 3.8 or later (3.12 recommended)

### Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. **IMPORTANT**: During installation, check the box "Add Python to PATH"
3. Click "Install Now"
4. Verify installation:
   ```cmd
   python --version
   ```

### Step 2: Extract/Clone Project

```cmd
# Option A: If you have a project archive
cd Desktop
unzip Meow-Valley.zip
cd Meow-Valley

# Option B: If you have a git repository
cd Desktop
git clone <your-repository-url>
cd Meow-Valley
```

### Step 3: Run Automatic Setup

```cmd
# From the project root directory
python setup.py
```

This will automatically:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify imports
- ✅ Ready to play!

### Step 4: Run the Game

```cmd
# Using the python from virtual environment
venv\Scripts\python code\main.py

# Or activate venv first
venv\Scripts\activate
python code\main.py
```

### Windows Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'pygame'`

```cmd
# Solution 1: Reinstall pygame
pip install pygame --force-reinstall

# Solution 2: If still fails
pip install pipwin
pipwin install pygame
```

**Problem:** "Add Python to PATH" wasn't checked

```cmd
# Solution: Add to system PATH manually
# 1. Search "environment" in Windows
# 2. Click "Edit the system environment variables"
# 3. Click "Environment Variables"
# 4. Add Python install directory to PATH
```

**Problem:** PowerShell execution policy error

```powershell
# Solution: Allow script execution for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Linux Setup

### Prerequisites

- Linux (Ubuntu/Debian recommended)
- Python 3.8 or later (3.12 recommended)

### Step 1: Install System Dependencies

```bash
# Update package manager
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install SDL2 libraries
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

### Step 2: Extract/Clone Project

```bash
# Option A: If you have a project archive
cd ~/Desktop
unzip Meow-Valley.zip
cd Meow-Valley

# Option B: If you have a git repository
cd ~/Desktop
git clone <your-repository-url>
cd Meow-Valley
```

### Step 3: Run Automatic Setup

```bash
# From the project root directory
python3 setup.py
```

This will automatically:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify imports
- ✅ Ready to play!

### Step 4: Run the Game

```bash
# Using the python from virtual environment
venv/bin/python code/main.py

# Or activate venv first
source venv/bin/activate
python code/main.py
```

### Linux Troubleshooting

**Problem:** `pygame not found`

```bash
# Solution: Install system pygame package
sudo apt install python3-pygame

# OR reinstall via pip
pip install pygame --no-cache-dir -v
```

**Problem:** No audio output

```bash
# Solution: Install additional audio support
sudo apt install libpulse0 libpulse-dev
pip install pygame --no-cache-dir
```

**Problem:** Display server issues (headless systems)

```bash
# Solution: Install Xvfb for virtual display
sudo apt install xvfb
xvfb-run python3 code/main.py
```

---

## 🎮 Game Controls

| Key               | Action                      |
| ----------------- | --------------------------- |
| **W/A/S/D** | Move around                 |
| **SPACE**   | Use tool (hoe/axe/water)   |
| **Q**       | Switch tool (hoe/axe/water) |
| **LCTRL**   | Plant seed                  |
| **E**       | Switch seed (corn/tomato)   |
| **ENTER**   | Interact (sleep/shop)       |
| **ESC**     | Open/close menu (in shop)   |

These controls work identically on all platforms!

---

## 🛠️ Gameplay Mechanics

### Farming System
- **Hoe**: Till soil to prepare for planting
- **Seeds**: Plant corn or tomato with LCTRL (requires seeds in inventory)
- **Watering Can**: Water plants for growth
- **Harvesting**: Use hoe on mature plants to collect produce

### Tools & Resources
| Tool | Function | Obtained |
|------|----------|----------|
| **Hoe** | Till soil & harvest plants | Starting tool |
| **Axe** | Chop trees for wood & apples | Starting tool |
| **Watering Can** | Water crops | Starting tool |

### Inventory System
**Items (Harvestable)**:
- Wood (from trees)
- Apples (from trees)
- Corn (from crops)
- Tomato (from crops)

**Seeds (Plantable)**:
- Corn seed (cost: $4)
- Tomato seed (cost: $5)

**Selling Prices**:
- Wood: $4
- Apple: $2
- Corn: $10
- Tomato: $20

### Day/Night Cycle
- Sleep in your bed to advance to next day
- Plants grow over time based on growth speed multiplier
- Weather randomly changes each day (rain affects crop growth)

---

## 📋 Requirements

The project requires only 2 Python packages:

```
pygame==2.6.1      # 2D game engine with SDL2 backend
pytmx==3.32.5      # Tiled map format parser
```

These are specified in `requirements.txt` and installed automatically when you run:

```bash
pip install -r requirements.txt
```

---

## 🏗️ Project Structure

```
Meow-Valley/
├── code/                    # Main game source code
│   ├── main.py             # Game entry point
│   ├── level.py            # Game level/scene
│   ├── player.py           # Player character
│   ├── soil.py             # Farming mechanics
│   ├── sprites.py          # Sprite classes
│   ├── menu.py             # Shop menu UI
│   ├── sky.py              # Weather/rain system
│   ├── overlay.py          # HUD/UI elements
│   ├── support.py          # Helper functions & path resolution
│   ├── settings.py         # Game configuration
│   ├── timer.py            # Timer class
│   └── transition.py       # Transition effects
├── graphics/               # Game sprites and images
├── audio/                  # Sound effects and music
├── data/                   # Tiled map files
├── font/                   # Font files (TTF)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## ✨ Features

- 🌾 Farm simulation gameplay
- 🎨 Tiled-based map system
- 🎵 Background music and sound effects
- 🌧️ Dynamic weather system
- 🛠️ Multiple tools (hoe, axe, watering can)
- 🌱 Plant growth system
- 🎪 Shop menu
- 💤 Sleep/day transition system
- 🏠 Interactive objects (house, shop)

---

## 🔄 Cross-Platform Compatibility

This game is fully compatible with:

- ✅ **macOS** (Intel & Apple Silicon)
- ✅ **Windows** (10, 11)
- ✅ **Linux** (Ubuntu, Debian, etc.)

The codebase uses:

- `pathlib` for universal file path handling
- pygame's cross-platform graphics/audio
- No OS-specific dependencies or APIs

---

## 🚀 Quick Reference

### Quickest Setup (All Platforms)

```bash
# Simply run this from project root
python3 setup.py

# Then run the game
venv/bin/python code/main.py
```

That's it! The setup script handles:
- Creating virtual environment
- Installing all dependencies
- Verifying everything works
- Telling you how to run the game

### Verify Installation

```bash
# Check Python version
python3 --version          # Should be 3.8+

# Check installed packages
pip list | grep -E "pygame|pytmx"

# Test imports
python3 -c "import pygame, pytmx; print('✅ OK')"
```

---

## 📞 Troubleshooting Common Issues

### Issue: "No module named 'pygame' / 'pytmx'"

**Solution**:

```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "FileNotFoundError: asset files not found"

**Solution**: Ensure you're running from the project root directory:

```bash
cd path/to/Meow-Valley
python code/main.py
```

### Issue: Game window opens but no content appears

**Solution**: Update your graphics driver and try:

```bash
pip install pygame --force-reinstall --no-cache-dir
```

### Issue: "Permission denied" or "command not found"

**Solution**: Ensure virtual environment is activated:

```bash
source venv/bin/activate    # macOS/Linux
# OR
venv\Scripts\activate       # Windows
```

---

## 🎓 Learning Resources

- **Pygame Documentation**: https://www.pygame.org/docs/
- **Pytmx GitHub**: https://github.com/bitcraft/pytmx
- **Tiled Map Editor**: https://www.mapeditor.org/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html

---

## 📝 License

This project is based on the PyDew-Valley repository by clear-code-projects and customized as Meow Valley.

Original Project: https://github.com/clear-code-projects/PyDew-Valley

**Note**: To use this project with your own repository, update the git remote URL:
```bash
git remote set-url origin <your-repository-url>
```

---

## ✅ System Requirements Summary

| Operating System  | Minimum        | Recommended    |
| ----------------- | -------------- | -------------- |
| **Python**  | 3.8            | 3.12           |
| **RAM**     | 2 GB           | 4 GB+          |
| **Storage** | 500 MB         | 1 GB           |
| **macOS**   | 10.13 (Sierra) | 11+ (Big Sur+) |
| **Windows** | 10             | 11             |
| **Linux**   | Any modern     | Ubuntu 20.04+  |

---

---

## 🔧 Recent Fixes & Updates

### Bug Fixes
- ✅ Fixed AttributeError in tree sprite handling during day transition
- ✅ Improved sprite collision detection
- ✅ Optimized plant growth system

### Known Issues & Workarounds
- None currently reported

---

## 📚 Development Notes

### Code Architecture
- **MVC Pattern**: Model (soil layer, sprites) - View (display) - Controller (player input)
- **Sprite Groups**: Organized by type (trees, collision, interaction, etc.)
- **Camera System**: Dynamic camera follows player
- **Event System**: Timer-based events for actions

### Future Features (Potential)
- [ ] More crop varieties
- [ ] Animal husbandry
- [ ] Quest system
- [ ] Multiplayer support
- [ ] Expanded UI customization

---

**Last Updated**: November 4, 2025

**Status**: ✅ Ready to Play!

**Repository**: https://github.com/jejow/Meow-Valley

Enjoy your farming simulation! 🌾✨

---

*For additional platform-specific help, check the troubleshooting sections above.*

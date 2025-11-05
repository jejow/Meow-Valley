# Menu Features - Meow Valley

## Fitur Baru yang Ditambahkan

### 1. Main Menu
Main menu akan muncul saat game pertama kali dijalankan dengan opsi:
- **New Game**: Memulai game baru
- **Load Game**: Memuat save game yang tersimpan
- **Settings**: Mengatur volume musik dan sound effect
- **Quit**: Keluar dari game

**Kontrol:**
- Tombol ↑/↓: Navigasi menu
- Enter/Space: Pilih opsi
- ESC: Kembali (di submenu)

### 2. Pause Menu
Tekan ESC saat bermain untuk membuka pause menu dengan opsi:
- **Resume**: Melanjutkan permainan
- **Save Game**: Menyimpan progress game
- **Settings**: Mengatur audio settings
- **Main Menu**: Kembali ke main menu (otomatis save)

**Kontrol:**
- ESC: Buka/tutup pause menu
- ↑/↓: Navigasi menu
- Enter/Space: Pilih opsi

### 3. Settings Menu
Menu pengaturan audio dengan fitur:
- **Music Volume**: Mengatur volume musik background (0-100%)
- **Sound Volume**: Mengatur volume sound effects (0-100%)
- **Back**: Kembali ke menu sebelumnya

**Kontrol:**
- ↑/↓: Pilih setting
- ←/→: Adjust volume (pada Music/Sound Volume)
- Enter/Space: Konfirmasi (pada Back)
- ESC: Kembali

### 4. Save/Load System
Game secara otomatis menyimpan progress dengan fitur:
- **Manual Save**: Tekan F5 saat bermain atau pilih "Save Game" di pause menu
- **Auto Save**: Game otomatis save saat:
  - Keluar dari game (tutup window)
  - Kembali ke main menu dari pause menu
  - Sebelum kembali ke main menu

**Data yang Disimpan:**
- Posisi player
- Jumlah uang
- Item inventory
- Seed inventory
- Status cuaca
- Soil grid (tanah yang sudah diolah)
- Plants (tanaman yang sedang tumbuh)

File save disimpan di: `saves/savegame.json`

### 5. Notification System
Sistem notifikasi untuk memberi feedback kepada player:
- Muncul di bagian atas tengah layar
- Fade out effect setelah 2 detik
- Menampilkan pesan seperti:
  - "Game saved!"
  - "Game loaded successfully!"
  - "No save file found!"
  - dll

## Cara Menggunakan

### Memulai Game Baru
1. Jalankan `main.py`
2. Pilih "New Game" di main menu
3. Game dimulai dengan state default

### Memuat Save Game
1. Jalankan `main.py`
2. Pilih "Load Game" di main menu
3. Game akan memuat progress terakhir yang disimpan

### Menyimpan Game
- **Cara 1**: Tekan F5 saat bermain
- **Cara 2**: Tekan ESC → pilih "Save Game"
- **Cara 3**: Otomatis saat keluar game

### Mengatur Audio
1. Dari main menu atau pause menu, pilih "Settings"
2. Gunakan arrow keys untuk adjust volume
3. Pilih "Back" untuk menyimpan settings

## Struktur File Baru

```
code/
├── main.py           # Updated dengan menu system
├── menu.py           # Updated dengan MainMenu, SettingsMenu, PauseMenu, Notification
├── game_state.py     # NEW - Save/load functionality
└── ...

saves/                # NEW - Folder untuk save files
└── savegame.json    # Save file
```

## Technical Details

### Game States
- `main_menu`: Tampilan main menu
- `playing`: Sedang bermain
- `paused`: Game di-pause
- `settings`: Settings menu (dari main menu)
- `settings_from_pause`: Settings menu (dari pause menu)

### Keyboard Shortcuts
- **ESC**: Pause/Resume game
- **F5**: Quick save
- **Arrow Keys**: Navigasi menu
- **Enter/Space**: Konfirmasi pilihan

## Notes

- Save file menggunakan format JSON untuk mudah dibaca dan diedit
- Settings audio langsung berlaku saat diubah
- Game tidak bisa di-pause saat shop menu aktif
- Auto-save memastikan progress tidak hilang

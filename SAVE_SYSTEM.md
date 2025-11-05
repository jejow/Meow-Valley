# Save System Documentation

## Overview
Sistem save/load game yang komprehensif untuk Meow Valley yang menyimpan setiap detail permainan.

## Data Yang Disimpan

### 1. Player Data
- **Posisi & Movement**
  - `pos`: Posisi player (x, y)
  - `direction`: Arah gerakan player
  - `status`: Status animasi player (e.g., 'down_idle', 'up_axe')
  - `frame_index`: Frame animasi saat ini

- **Inventory & Economy**
  - `money`: Jumlah uang player
  - `item_inventory`: Inventory item (wood, apple, corn, tomato)
  - `seed_inventory`: Inventory benih (corn, tomato)

- **Tools & Seeds**
  - `selected_tool`: Tool yang sedang dipilih
  - `selected_seed`: Seed yang sedang dipilih
  - `tool_index`: Index tool dalam array
  - `seed_index`: Index seed dalam array

- **State**
  - `sleep`: Status tidur player
  - `timers`: State dari semua timer (tool use, tool switch, seed use, seed switch)

### 2. Level Data
- **Weather & Environment**
  - `raining`: Status hujan (true/false)
  - `sky_color`: Warna langit saat ini [R, G, B]

- **Farming System**
  - `soil_grid`: Grid tanah yang sudah dicangkul
    - Menyimpan status setiap tile: 'F' (Farmable), 'X' (Hoed), 'W' (Watered), 'P' (Planted)
  - `water_tiles`: Posisi semua water tiles di tanah
  - `plants`: Semua tanaman dengan detail:
    - `plant_type`: Jenis tanaman (corn/tomato)
    - `pos`: Posisi tanaman
    - `age`: Umur tanaman (untuk growth stage)
    - `harvestable`: Status siap panen
    - `soil_pos`: Posisi soil tile tempat tanaman ditanam

- **Trees & Resources**
  - `trees`: State semua pohon:
    - `pos`: Posisi pohon
    - `health`: Health points pohon
    - `alive`: Status hidup pohon
    - `apple_count`: Jumlah apel di pohon

- **Transition & Time**
  - `transition`: State transisi tidur
    - `color`: Warna overlay transisi
    - `speed`: Kecepatan transisi

### 3. Meta Data
- `save_time`: Timestamp saat save (pygame ticks)
- `version`: Versi save system

## Cara Menggunakan

### Menyimpan Game
1. **Auto-save**: Game otomatis tersimpan saat:
   - Keluar dari game (tombol X)
   - Kembali ke main menu dari pause menu
   - Kembali ke main menu dengan ESC

2. **Manual save**: 
   - Tekan `F5` saat bermain
   - Pilih "Save Game" dari pause menu (tekan ESC)

### Load Game
1. Pilih "Load Game" dari main menu
2. Game akan restore semua state yang tersimpan
3. Notifikasi akan muncul jika berhasil/gagal

## Lokasi Save File
Save file disimpan di: `../saves/savegame.json`

## Fitur Khusus

### Timer Restoration
Timer player (tool use, seed switch, etc) di-restore dengan mempertimbangkan waktu yang telah berlalu, sehingga cooldown tetap konsisten.

### Plant Growth Preservation
Setiap tanaman disimpan dengan umur exact-nya, sehingga stage pertumbuhan tetap sama saat di-load.

### Tree State Management
Pohon yang sudah rusak atau mati akan tetap dalam kondisi yang sama saat di-load, termasuk jumlah apel yang tersisa.

### Weather Continuity
Status cuaca (hujan/tidak) tetap preserved, termasuk kondisi water tiles di tanah.

### Sky Transition
Warna langit disimpan, sehingga time of day visual tetap konsisten.

## Error Handling
- Jika load gagal, game akan menampilkan notifikasi error
- Traceback detail di-print ke console untuk debugging
- Auto-fallback ke new game jika save file corrupt/tidak ada

## Compatibility
- Save version: 1.0
- Compatible dengan game version: Current
- Save file format: JSON (human-readable)

## Tips
1. Gunakan multiple save slots dengan meng-copy save file
2. Backup save file secara manual untuk keamanan
3. Save file dapat di-edit manual jika diperlukan (hati-hati!)

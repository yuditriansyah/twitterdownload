# Social Media Downloader

Script untuk mengunduh gambar dari Twitter, Instagram, dan Pinterest, lalu menguploadnya ke ImgBB (untuk Twitter & Pinterest) dan Supabase (untuk Instagram).

## Fitur

- Download gambar dari tweets
- Upload gambar Twitter ke ImgBB
- Download gambar dari profil Instagram publik
- Upload gambar Instagram ke Supabase Storage
- Download gambar dari Pinterest search
- Upload gambar Pinterest ke ImgBB
- Menghindari duplikasi dengan melacak ID/file yang sudah diproses
- Penanganan rate limit dan error

## Pengaturan

1. Clone repository ini
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Buat file `.env` (lihat `.env.example` sebagai contoh)

### Konfigurasi Twitter

Untuk mengunduh dari Twitter, Anda memerlukan:
- Twitter API Bearer Token
- ImgBB API Key (gratis dari https://api.imgbb.com/)

Tambahkan ke file `.env`:
```
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
IMGBB_API_KEY=your_imgbb_api_key
TARGET_USERNAME=username_to_monitor
```

### Konfigurasi Instagram

Untuk mengunduh dari Instagram, gunakan:
```
IG_USERNAME=username_target              # Username yang ingin diunduh postnya
IG_LOGIN_USERNAME=username_anda          # Username login Instagram Anda (opsional)
IG_LOGIN_PASSWORD=password_anda          # Password login Instagram Anda (opsional)
MAX_POSTS=10                             # Jumlah post terbaru yang diunduh
```

### Konfigurasi Pinterest

Untuk mengunduh dari Pinterest:
```
IMGBB_API_KEY=your_imgbb_api_key          # API key untuk upload (opsional)
```

Pinterest scraper tersedia dalam 2 versi:
- **Selenium version** (`pin.py`): Lebih banyak gambar, butuh ChromeDriver
- **Simple version** (`pin_simple.py`): Tanpa Selenium, lebih mudah setup

## Mendapatkan ImgBB API Key

1. Kunjungi https://api.imgbb.com/
2. Daftar akun gratis
3. Dapatkan API key Anda
4. Tambahkan ke file `.env`: `IMGBB_API_KEY=your_key`

## Penggunaan

### Twitter Downloader

```bash
python main.py
```

### Instagram Downloader

```bash
python ig.py
```

Atau gunakan script pembantu yang memeriksa kredensial:

```bash
./run_instagram.sh
```

## Penggunaan

### Twitter Downloader

```bash
python main.py
```

### Instagram Downloader

```bash
python ig.py
```

Atau gunakan script pembantu yang memeriksa kredensial:

```bash
./run_instagram.sh
```

## Mengatasi Rate Limit Instagram

Instagram memiliki kebijakan rate limit yang ketat. Jika menerima error "Please wait a few minutes before you try again", lihat panduan troubleshooting di [INSTAGRAM_TROUBLESHOOTING.md](INSTAGRAM_TROUBLESHOOTING.md).

## Tools Bantuan

- `debug.py` - Periksa koneksi Twitter API
- `check_rate_limit.py` - Periksa status rate limit Twitter
- `test_twitter.py` - Test konektivitas Twitter API dan deteksi tweet dengan gambar
- `test_imgbb.py` - Test fungsi upload ImgBB
- `test_upload.py` - Test fungsi upload Supabase (untuk Instagram)
- `test_speed.py` - Test optimisasi kecepatan Twitter bot
- `run_instagram.sh` - Pemeriksaan kredensial dan menjalankan script Instagram
- `run_pinterest.py` - Menu interaktif untuk Pinterest scraper

## Output Files

- `processed_ids.txt` - Daftar ID tweet yang sudah diproses
- `uploaded_images.txt` - Daftar URL gambar yang berhasil diupload ke ImgBB
- `processed_instagram_files.txt` - Daftar file Instagram yang sudah diproses

## Troubleshooting

### Error: "Header value must be str or bytes, not <class 'bool'>"

Error ini sudah diperbaiki dengan mengganti Supabase dengan ImgBB untuk Twitter uploads.

### ImgBB API Issues

Jika mengalami masalah dengan ImgBB:
1. Pastikan API key valid
2. Cek limit upload (gratis: 100 uploads/jam)
3. Ukuran file maksimal: 32MB

### Instagram Rate Limiting

Lihat panduan lengkap di [INSTAGRAM_TROUBLESHOOTING.md](INSTAGRAM_TROUBLESHOOTING.md) untuk mengatasi masalah rate limit Instagram.
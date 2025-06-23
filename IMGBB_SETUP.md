# ImgBB Setup Guide

## Cara Mendapatkan ImgBB API Key

ImgBB adalah layanan hosting gambar gratis yang menyediakan API untuk upload.

### Langkah-langkah:

1. **Kunjungi ImgBB API**
   - Buka https://api.imgbb.com/

2. **Daftar Akun**
   - Klik "Sign up" jika belum punya akun
   - Atau login jika sudah punya akun

3. **Dapatkan API Key**
   - Setelah login, Anda akan melihat API key di dashboard
   - Copy API key tersebut

4. **Update File .env**
   ```
   IMGBB_API_KEY=your_actual_api_key_here
   ```

### Keuntungan ImgBB:

- ✅ **Gratis** - Tidak perlu bayar
- ✅ **Mudah Setup** - Hanya perlu API key
- ✅ **Reliable** - Service yang stabil
- ✅ **Unlimited Storage** - Tanpa batas penyimpanan
- ✅ **Direct Links** - URL langsung untuk gambar

### Batasan:

- 🔸 **Rate Limit**: 100 uploads per jam untuk akun gratis
- 🔸 **File Size**: Maksimal 32MB per file
- 🔸 **File Types**: Support JPG, PNG, GIF, BMP, WebP

### Testing:

Setelah mendapatkan API key, test dengan:

```bash
python test_imgbb.py
```

Jika berhasil, Anda akan melihat:
```
✅ Upload successful!
   Image URL: https://i.ibb.co/xxxxxx/test_upload.png
```

### Menggunakan Twitter Bot:

Setelah setup ImgBB, jalankan Twitter bot:

```bash
python main.py
```

Bot akan:
1. Monitor tweets dari user yang ditentukan
2. Download gambar dari tweets
3. Upload ke ImgBB
4. Simpan URL hasil upload di `uploaded_images.txt`

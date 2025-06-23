#!/bin/bash

# Script untuk membantu menjalankan ig.py dengan kredensi login

# Pastikan .env sudah berisi kredensi yang benar
if [ ! -f .env ]; then
    echo "❌ File .env tidak ditemukan. Membuat contoh file..."
    cp .env.example .env
    echo "✅ File .env dibuat. Silakan edit file ini dan masukkan kredensi login Instagram."
    echo "   Lalu jalankan script ini kembali."
    exit 1
fi

# Periksa apakah kredensi login sudah diatur
if ! grep -q "IG_LOGIN_USERNAME=" .env || ! grep -q "IG_LOGIN_PASSWORD=" .env; then
    echo "⚠️ Kredensi login Instagram belum diatur di file .env."
    echo "   Silakan edit file .env dan tambahkan:"
    echo "   IG_LOGIN_USERNAME=username_anda"
    echo "   IG_LOGIN_PASSWORD=password_anda"
    exit 1
fi

# Cek apakah username kosong
IG_USERNAME=$(grep "IG_LOGIN_USERNAME=" .env | cut -d "=" -f2)
if [ -z "$IG_USERNAME" ] || [ "$IG_USERNAME" = "your_instagram_username" ]; then
    echo "⚠️ Username Instagram belum diatur dengan benar di file .env."
    echo "   Silakan edit file .env dan tambahkan username Instagram yang valid."
    exit 1
fi

# Jalankan script Instagram dengan waktu tunggu yang lebih lama
echo "🔄 Menjalankan script Instagram dengan login dan waktu tunggu yang lebih lama..."
echo "ℹ️ Menggunakan akun: $IG_USERNAME"
echo ""

# Jalankan script Python
python ig.py

echo ""
echo "💡 Jika masih mengalami rate limit, coba tunggu beberapa jam sebelum menjalankan script lagi."
echo "   Atau gunakan akun Instagram lain di file .env."

#!/usr/bin/env python3
"""
Test dan jalankan Pinterest scraper
"""
import os

def test_selenium_version():
    """Test apakah versi Selenium bisa jalan"""
    print("🧪 Testing Selenium version...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome_test")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        driver.quit()
        print("✅ Selenium version available!")
        return True
        
    except Exception as e:
        print(f"❌ Selenium version not working: {e}")
        return False

def show_menu():
    """Tampilkan menu pilihan"""
    print("\n" + "="*50)
    print("🎨 Pinterest Image Downloader")
    print("="*50)
    print("Pilih metode download:")
    print("1. Selenium version (lebih banyak gambar, butuh ChromeDriver)")
    print("2. Simple version (tanpa Selenium, lebih mudah)")
    print("3. Test dependencies")
    print("4. Exit")
    print("="*50)

def main():
    """Main function"""
    while True:
        show_menu()
        choice = input("Pilihan Anda (1-4): ").strip()
        
        if choice == "1":
            # Test Selenium dulu
            if test_selenium_version():
                print("\n🚀 Menjalankan Selenium version...")
                os.system("python pin.py")
            else:
                print("\n❌ Selenium tidak tersedia. Coba simple version instead.")
                
        elif choice == "2":
            print("\n🚀 Menjalankan Simple version...")
            os.system("python pin_simple.py")
            
        elif choice == "3":
            print("\n🔍 Testing dependencies...")
            
            # Test basic dependencies
            try:
                import requests
                print("✅ requests: OK")
            except ImportError:
                print("❌ requests: Missing")
            
            try:
                from PIL import Image
                print("✅ Pillow (PIL): OK")
            except ImportError:
                print("❌ Pillow (PIL): Missing")
            
            try:
                from dotenv import load_dotenv
                print("✅ python-dotenv: OK")
            except ImportError:
                print("❌ python-dotenv: Missing")
            
            # Test ImgBB config
            from dotenv import load_dotenv
            load_dotenv()
            imgbb_key = os.getenv("IMGBB_API_KEY")
            if imgbb_key and imgbb_key != "your_imgbb_api_key_here":
                print("✅ ImgBB API key: Configured")
            else:
                print("⚠️ ImgBB API key: Not configured (local save only)")
            
            # Test Selenium
            test_selenium_version()
            
        elif choice == "4":
            print("👋 Selamat tinggal!")
            break
            
        else:
            print("❌ Pilihan tidak valid!")
        
        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()

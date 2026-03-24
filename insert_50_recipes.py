import requests
import json
import time

API_URL = "http://127.0.0.1:8000/recipes"

print("=" * 60)
print("📝 MULAI MENGINPUT 50 RESEP KE DATABASE")
print("=" * 60)

# Baca file JSON
try:
    with open("recipes_50.json", "r", encoding="utf-8") as f:
        recipes = json.load(f)
    print(f"✅ File recipes_50.json ditemukan. Total resep: {len(recipes)}")
except FileNotFoundError:
    print("❌ File recipes_50.json tidak ditemukan!")
    print("   Pastikan file berada di folder yang sama dengan script ini.")
    exit()

# Cek koneksi ke API
try:
    response = requests.get("http://127.0.0.1:8000/")
    if response.status_code != 200:
        print("❌ API tidak merespon. Pastikan server berjalan di http://127.0.0.1:8000")
        exit()
    print("✅ Koneksi ke API berhasil")
except:
    print("❌ Tidak dapat terhubung ke API. Jalankan 'uvicorn app.main:app --reload' dulu")
    exit()

print("\n" + "-" * 60)
print("🔄 MULAI INPUT DATA...")
print("-" * 60)

success_count = 0
fail_count = 0

for i, recipe in enumerate(recipes, 1):
    try:
        # Kirim POST request
        response = requests.post(API_URL, json=recipe)
        
        if response.status_code == 201:
            print(f"✅ [{i:2}/50] {recipe['judul'][:35]:35} ... OK")
            success_count += 1
        else:
            print(f"❌ [{i:2}/50] {recipe['judul'][:35]:35} ... GAGAL (Status: {response.status_code})")
            fail_count += 1
            if response.text:
                print(f"      Error: {response.text[:100]}")
                
    except Exception as e:
        print(f"❌ [{i:2}/50] {recipe['judul'][:35]:35} ... ERROR: {str(e)[:50]}")
        fail_count += 1
    
    # Jeda sedikit agar tidak overload API
    time.sleep(0.1)

print("\n" + "=" * 60)
print(f"📊 HASIL INPUT DATA")
print("=" * 60)
print(f"✅ Berhasil : {success_count} resep")
print(f"❌ Gagal   : {fail_count} resep")
print(f"📁 Total   : {len(recipes)} resep")
print("=" * 60)

if success_count == len(recipes):
    print("🎉 SELAMAT! Semua 50 resep berhasil ditambahkan!")
    print("   Buka http://127.0.0.1:8000/docs untuk melihat hasilnya.")
else:
    print("⚠️ Ada beberapa resep yang gagal. Cek error di atas.")
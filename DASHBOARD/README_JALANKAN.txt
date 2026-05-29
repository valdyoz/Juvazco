FINAL JUVAZCO MARKETPLACE CLEAN
=================================

FITUR:
- Dashboard utama mirip marketplace, tapi desain sendiri.
- Search produk di atas.
- Banner foto1.png, foto2.png, foto3.png geser otomatis tiap 2 detik.
- Produk tampil dari upload admin.
- Customer bisa lihat produk tanpa login.
- Jika tambah keranjang / checkout, harus login customer.
- Register hanya tampilan, tidak bisa dipakai.
- Login admin otomatis masuk Dashboard Admin Juvazco.
- Login user otomatis bisa checkout.
- Seller random: JUAN, ZICO, RIVALDY, AZIZ.
- Foto seller ada di static/PHOTO_ADMIN.
- Customer service hanya ada untuk akun customer.
- Chat seller di detail produk ada tapi disabled / tidak bisa diklik.
- Tidak ada label toko, diskon, video, dan alamat produk.

LOGIN:
Admin    : adminjuvazco / unesa
Customer : user1 / user1
Customer : user2 / user2

CARA RUNNING:
1. Extract ZIP ke folder baru.
2. Buka terminal di folder yang ada manage.py.
3. Jalankan:

   python -m pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver

4. Buka:
   http://127.0.0.1:8000/

FOLDER FOTO:
- Banner utama: static/background_images/foto1.png foto2.png foto3.png
- Foto seller: static/PHOTO_ADMIN/juan.png zico.png rivaldy.png aziz.png
- Produk admin: di-upload dari dashboard admin, tersimpan ke folder media/product_images/

KALAU MAU RESET DATABASE:
   CTRL + C
   Remove-Item db.sqlite3 -ErrorAction SilentlyContinue
   Get-ChildItem shop\migrations\*.py | Where-Object {$_.Name -ne "__init__.py"} | Remove-Item -Force
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver

"""
File ini untuk data alamat/wilayah Indonesia dan data seller.

Dipakai oleh:
- shop/models.py untuk mengisi nama seller random saat produk dibuat.
- shop/views.py untuk pilihan alamat checkout.
- template detail produk untuk foto seller dari folder static/PHOTO_ADMIN.
"""

SELLER_DATA = [
    {'nama': 'JUAN', 'foto': 'juan.png'},
    {'nama': 'ZICO', 'foto': 'zico.png'},
    {'nama': 'RIVALDY', 'foto': 'rivaldy.png'},
    {'nama': 'AZIZ', 'foto': 'aziz.png'},
]

DAERAH_INDONESIA = [
    'Aceh', 'Medan, Sumatera Utara', 'Padang, Sumatera Barat', 'Pekanbaru, Riau', 'Jambi',
    'Palembang, Sumatera Selatan', 'Bengkulu', 'Lampung', 'Pangkal Pinang, Bangka Belitung',
    'Tanjung Pinang, Kepulauan Riau', 'Jakarta', 'Bogor, Jawa Barat', 'Depok, Jawa Barat',
    'Bekasi, Jawa Barat', 'Bandung, Jawa Barat', 'Cirebon, Jawa Barat', 'Semarang, Jawa Tengah',
    'Solo, Jawa Tengah', 'Yogyakarta', 'Surabaya, Jawa Timur', 'Sidoarjo, Jawa Timur',
    'Malang, Jawa Timur', 'Kediri, Jawa Timur', 'Madiun, Jawa Timur', 'Denpasar, Bali',
    'Mataram, Nusa Tenggara Barat', 'Kupang, Nusa Tenggara Timur', 'Pontianak, Kalimantan Barat',
    'Palangkaraya, Kalimantan Tengah', 'Banjarmasin, Kalimantan Selatan', 'Samarinda, Kalimantan Timur',
    'Tanjung Selor, Kalimantan Utara', 'Manado, Sulawesi Utara', 'Palu, Sulawesi Tengah',
    'Makassar, Sulawesi Selatan', 'Kendari, Sulawesi Tenggara', 'Gorontalo', 'Mamuju, Sulawesi Barat',
    'Ambon, Maluku', 'Ternate, Maluku Utara', 'Sorong, Papua Barat Daya', 'Manokwari, Papua Barat',
    'Jayapura, Papua', 'Nabire, Papua Tengah', 'Wamena, Papua Pegunungan', 'Merauke, Papua Selatan'
]


def seller_by_name(name):
    for seller in SELLER_DATA:
        if seller['nama'].lower() == (name or '').lower():
            return seller
    return SELLER_DATA[0]

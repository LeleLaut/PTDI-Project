import requests

# URL ke file PHP yang akan mengambil data dari tabel "arduino" dan "android3"
url = "http://example.com/getdata.php"

# Lakukan permintaan GET ke file PHP
response = requests.get(url)

# Cek apakah permintaan berhasil
if response.status_code == 200:
    # Data berhasil diambil dalam format JSON
    data_from_php = response.json()
    # Sekarang Anda dapat menggunakan data_from_php sesuai kebutuhan
    print(data_from_php)
else:
    print("Failed to fetch data from PHP.")

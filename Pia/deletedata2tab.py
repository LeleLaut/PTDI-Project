import mysql.connector

# Mengatur koneksi ke database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flightestdb"
)

# Membuat objek cursor
cursor = db_connection.cursor()

# Nama tabel yang ingin dihapus datanya
nama_tabel1 = "android"
nama_tabel2 = "arduino"

# Perintah SQL untuk menghapus data dari tabel 1
delete_query1 = f"DELETE FROM {nama_tabel1}"

# Perintah SQL untuk menghapus data dari tabel 2
delete_query2 = f"DELETE FROM {nama_tabel2}"

# Menjalankan perintah SQL untuk tabel 1
cursor.execute(delete_query1)

# Melakukan commit perubahan ke database untuk tabel 1
db_connection.commit()

# Menjalankan perintah SQL untuk tabel 2
cursor.execute(delete_query2)

# Melakukan commit perubahan ke database untuk tabel 2
db_connection.commit()

# Menutup kursor dan koneksi
cursor.close()
db_connection.close()

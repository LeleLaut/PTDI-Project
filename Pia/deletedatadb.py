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

nama_tabel = "arduino"

# Perintah SQL untuk menghapus semua data dari tabel
delete_query = f"DELETE FROM {nama_tabel}"

# Menjalankan perintah SQL
cursor.execute(delete_query)

# Melakukan commit perubahan ke database
db_connection.commit()

# Menutup kursor dan koneksi
cursor.close()
db_connection.close()

import pandas as pd
import mysql.connector

# Fungsi untuk mengkoneksikan ke database
def connect_to_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='flightestdb'
    )
    return connection

# Fungsi untuk mengekspor data ke CSV
def export_to_csv():
    # Koneksi ke database
    connection = connect_to_database()

    # Query untuk mengambil data dari tabel tertentu
    query = "SELECT * FROM android;"

    # Mengeksekusi query dan menyimpan hasilnya dalam DataFrame
    df = pd.read_sql_query(query, connection)

    # Menutup koneksi ke database
    connection.close()

    # Menyimpan DataFrame ke file CSV
    df.to_csv('android.csv', index=False)

    print("Data telah diekspor ke data.csv")

if __name__ == "__main__":
    export_to_csv()

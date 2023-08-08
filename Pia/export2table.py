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

def export_to_csv():
    # Koneksi ke database
    connection = connect_to_database()

    # Query untuk mengambil data dari tabel pertama
    query1 = "SELECT * FROM android;"

    # Query untuk mengambil data dari tabel kedua
    query2 = "SELECT * FROM arduinolocal;"

    # Mengeksekusi query pertama dan menyimpan hasilnya dalam DataFrame
    df1 = pd.read_sql_query(query1, connection)

    # Mengeksekusi query kedua dan menyimpan hasilnya dalam DataFrame
    df2 = pd.read_sql_query(query2, connection)

    # Menutup koneksi ke database
    connection.close()

    # Menyimpan DataFrame pertama ke file CSV
    df1.to_csv('android1.csv', index=False)

    # Menyimpan DataFrame kedua ke file CSV
    df2.to_csv('arduino1.csv', index=False)

    print("Data telah diekspor ke android1.csv dan arduino1.csv")

# Panggil fungsi untuk mengekspor data
export_to_csv()

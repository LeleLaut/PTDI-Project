import pandas as pd
from sqlalchemy import create_engine

def export_to_csv():
    # Membuat objek koneksi ke database menggunakan SQLAlchemy
    # Ganti 'your_username', 'your_password', 'your_host', dan 'your_database' dengan informasi yang sesuai
    db_connection = create_engine("mysql+pymysql://root:@localhost/flightestdb")

    # Query untuk mengambil data dari tabel pertama
    query1 = "SELECT * FROM android;"

    # Query untuk mengambil data dari tabel kedua
    query2 = "SELECT * FROM arduinolocal;"

    # Mengeksekusi query pertama dan menyimpan hasilnya dalam DataFrame
    df1 = pd.read_sql_query(query1, db_connection)

    # Mengeksekusi query kedua dan menyimpan hasilnya dalam DataFrame
    df2 = pd.read_sql_query(query2, db_connection)

    # Menyimpan DataFrame pertama ke file CSV
    df1.to_csv('android2.csv', index=False)

    # Menyimpan DataFrame kedua ke file CSV
    df2.to_csv('arduino2.csv', index=False)

    print("Data telah diekspor ke android2.csv dan arduino2.csv")

# Panggil fungsi untuk mengekspor data
export_to_csv()

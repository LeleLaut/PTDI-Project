import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flightestdb"
)

cursor = db_connection.cursor()

nama_tabel1 = "android"
nama_tabel2 = "arduino"

delete_query1 = f"DELETE FROM {nama_tabel1}"
delete_query2 = f"DELETE FROM {nama_tabel2}"

cursor.execute(delete_query1)
db_connection.commit()

cursor.execute(delete_query2)
db_connection.commit()

cursor.close()
db_connection.close()
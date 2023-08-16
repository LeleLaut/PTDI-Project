import tkinter as tk
from tkinter import ttk
import mysql.connector

# Fungsi untuk mengambil data dari database
def fetch_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='flightestdb'
        )
        cursor = connection.cursor()

        query = "SELECT * FROM arduino"
        cursor.execute(query)
        data = cursor.fetchall()

        connection.close()

        for row in data:
            tree.insert("", "end", values=row)
    except Exception as e:
        print(f"Error fetching data from database: {e}")

# Membuat jendela utama
root = tk.Tk()
root.title("UI untuk Output Database")

# Membuat treeview untuk menampilkan data
tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), show="headings")
tree.heading(1, text="gyro_x")
tree.heading(2, text="gyro_y")
tree.heading(3, text="gyro_z")
tree.heading(4, text="accel_x")
tree.heading(5, text="accel_y")
tree.heading(6, text="accel_z")
tree.heading(7, text="pitch")
tree.heading(8, text="roll")
tree.heading(9, text="yaw")
tree.heading(10, text="latitude")
tree.heading(11, text="longitude")
tree.heading(12, text="altitude")
tree.heading(13, text="counter")
tree.pack()

# Tombol untuk mengambil dan menampilkan data
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.pack(pady=10)

# Memulai loop utama
root.mainloop()
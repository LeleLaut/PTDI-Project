import sqlite3

# Menghubungkan ke database (atau gunakan koneksi ke database yang sesuai)
conn = sqlite3.connect('flightestdb')
cursor = conn.cursor()

# Baca data dari SD card dan masukkan ke database
with open('data.txt', 'r') as file:
    for line in file:
        data = line.strip().split(',')
        cursor.execute('INSERT INTO arduinolocal (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, pitch, roll, yaw, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' , data)

# Commit perubahan dan tutup koneksi
conn.commit()
conn.close()

import socket
import csv
import os
import mysql.connector

# Replace 'BROADCAST_IP' and 'PORT' with the appropriate values
BROADCAST_IP = '192.168.233.237'
PORT = 51111

if os.path.exists('./KAZ/SERVERLOCAL/local_logs_ardu.csv'):
    os.remove('./KAZ/SERVERLOCAL/local_logs_ardu.csv')

ininambah = 0

# Create a UDP socket
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set socket options to allow broadcasting and reuse the address
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the local address and port to receive messages
receive_socket.bind((BROADCAST_IP, PORT))

print(f"Listening for broadcasts from ESP8266 on port {PORT}")

# Open the database connection outside of the loop
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='flightestdb'
)

def insert_data_to_database(data):
    try:
        cursor = connection.cursor()

        query = "INSERT INTO arduinolocal (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, pitch, roll, yaw, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 

        for item in data:
            values = [float(value) for value in item[:9]]  
            values.append(item[9])  
            cursor.execute(query, tuple(values))
            connection.commit()

        cursor.close()
    except Exception as e:
        print(f"Error while saving data to the database: {e}")

while True:
    try:
        # Receive data from the broadcast
        data, esp8266_address = receive_socket.recvfrom(1024)  # 1024 is the buffer size

        # Decode the received data as UTF-8
        decoded_data = data.decode('utf-8')
        float_list = [float(number) for number in decoded_data.split(',')]
        
        float_list.append(ininambah)
        ininambah += 1
        
        # Masukkan data ke dalam database
        insert_data_to_database([float_list])
        
        with open('./KAZ/SERVERLOCAL/local_logs_ardu.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(float_list)
    
    except socket.timeout:
        # Timeout occurred, no data received
        pass

# read the data
df=sql.read_sql('select * from arduino',con)
# print the data
print(df)
# export the data into the excel sheet
df.to_csv('ds.csv')

# Close the cursor and connection after the loop ends
connection.close()
receive_socket.close()
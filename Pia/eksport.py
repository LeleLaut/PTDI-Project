import sqlite3
import csv

def export_table_to_csv(connection, table_name, csv_filename):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)
    data = cursor.fetchall()

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header if needed
        header = [description[0] for description in cursor.description]
        csv_writer.writerow(header)
        csv_writer.writerows(data)

if __name__ == "__main__":
    # Step 1: Connect to the database
    conn = sqlite3.connect('flightestdb.db')

    # Step 2: Export data from the first table to CSV
    table1_name = 'android'
    table1_csv_filename = 'andro1.csv'
    export_table_to_csv(conn, table1_name, table1_csv_filename)

    # Step 3: Export data from the second table to CSV
    table2_name = 'arduinolocal'
    table2_csv_filename = 'arduino1.csv'
    export_table_to_csv(conn, table2_name, table2_csv_filename)

    # Step 4: Close the connection
    conn.close()

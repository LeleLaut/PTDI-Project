<?php
// Koneksi ke database
$servername = "localhost"; // Nama host database
$username = "flight_test_user"; // Nama pengguna untuk koneksi ke database flight test
$password = "password_flight_test"; // Kata sandi untuk koneksi ke database flight test
$dbname = "flight_test_db"; // Nama database flight test

// Membuat koneksi
$conn = new mysqli($servername, $username, $password, $dbname);

// Memeriksa koneksi
if ($conn->connect_error) {
    die("Koneksi gagal: " . $conn->connect_error);
}

// Menerima data JSON dari ESP8266
$json_data = file_get_contents('php://input');

// Mengubah JSON menjadi array asosiatif
$data = json_decode($json_data, true);

// Mendapatkan nilai dari array asosiatif
$timestamp = $data['timestamp'];
$ultrasonic_data = $data['ultrasonic_data'];

// Menyimpan data ke database
$sql = "INSERT INTO ultrasonik_data_table (timestamp, ultrasonic_data) VALUES ('$timestamp', '$ultrasonic_data')";

if ($conn->query($sql) === TRUE) {
    echo "Data berhasil disimpan";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

// Menutup koneksi
$conn->close();
?>

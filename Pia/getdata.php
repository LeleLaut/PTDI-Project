<?php
// Koneksi ke database MySQL (PHPMyAdmin)
$connection = mysqli_connect("localhost", "root", "", "flightestdb");

// Cek koneksi berhasil atau tidak
if (!$connection) {
    die("Connection failed: " . mysqli_connect_error());
}

// Query untuk mengambil data dari tabel "arduino"
$sql_arduino = "SELECT * FROM arduino";

// Query untuk mengambil data dari tabel "android3"
$sql_android = "SELECT * FROM android3";

// Eksekusi query untuk tabel "arduino"
$result_arduino = mysqli_query($connection, $sql_arduino);

// Eksekusi query untuk tabel "android3"
$result_android = mysqli_query($connection, $sql_android);

// Buat array kosong untuk menyimpan hasil dari kedua tabel
$data = array();

// Cek apakah ada hasil data dari query tabel "arduino"
if (mysqli_num_rows($result_arduino) > 0) {
    // Loop melalui hasil data tabel "arduino" dan tambahkan ke array
    while ($row = mysqli_fetch_assoc($result_arduino)) {
        $data[] = $row;
    }
}

// Cek apakah ada hasil data dari query tabel "android3"
if (mysqli_num_rows($result_android) > 0) {
    // Loop melalui hasil data tabel "android3" dan tambahkan ke array
    while ($row = mysqli_fetch_assoc($result_android)) {
        $data[] = $row;
    }
}

// Tutup koneksi ke database
mysqli_close($connection);

// Konversi array ke format JSON dan kirimkan sebagai respons
header('Content-Type: application/json');
echo json_encode($data);
?>

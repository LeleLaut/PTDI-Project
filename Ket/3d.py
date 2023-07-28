import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

# Fungsi untuk membuat model balok berdasarkan data Pitch, Roll, dan Yaw
def create_cuboid(pitch, roll, yaw):
    # Panjang, lebar, dan tinggi balok
    length = 1
    width = 0.5
    height = 0.2

    # Sudut Pitch, Roll, dan Yaw dalam radian
    pitch_rad = np.radians(pitch)
    roll_rad = np.radians(roll)
    yaw_rad = np.radians(yaw)

    # Transformasi balok berdasarkan Pitch, Roll, dan Yaw
    rotation_matrix = np.array([
        [np.cos(yaw_rad)*np.cos(roll_rad), np.cos(yaw_rad)*np.sin(roll_rad)*np.sin(pitch_rad) - np.sin(yaw_rad)*np.cos(pitch_rad),
         np.cos(yaw_rad)*np.sin(roll_rad)*np.cos(pitch_rad) + np.sin(yaw_rad)*np.sin(pitch_rad)],
        [np.sin(roll_rad), np.cos(roll_rad)*np.cos(pitch_rad), -np.cos(roll_rad)*np.sin(pitch_rad)],
        [-np.sin(yaw_rad)*np.cos(roll_rad), np.sin(yaw_rad)*np.sin(roll_rad)*np.cos(pitch_rad) + np.cos(yaw_rad)*np.sin(pitch_rad),
         -np.sin(yaw_rad)*np.sin(roll_rad)*np.sin(pitch_rad) + np.cos(yaw_rad)*np.cos(pitch_rad)]
    ])

    # Define vertices of the cuboid
    vertices = np.array([[-length / 2, -width / 2, -height / 2],
                         [length / 2, -width / 2, -height / 2],
                         [length / 2, width / 2, -height / 2],
                         [-length / 2, width / 2, -height / 2],
                         [-length / 2, -width / 2, height / 2],
                         [length / 2, -width / 2, height / 2],
                         [length / 2, width / 2, height / 2],
                         [-length / 2, width / 2, height / 2]])

    # Apply rotation to the vertices
    rotated_vertices = np.dot(vertices, rotation_matrix.T)

    return rotated_vertices

# Fungsi untuk animasi balok 3D
def animate(i):
    # Baca data Pitch, Roll, dan Yaw dari sumber data Anda (misalnya dari file CSV)
    pitch = i  # Contoh sederhana: Pitch berubah sesuai waktu
    roll = i
    yaw = i

    # Dapatkan posisi balok 3D yang bergerak sesuai dengan data Pitch, Roll, dan Yaw
    cuboid_vertices = create_cuboid(pitch, roll, yaw)

    # Perbarui plot balok 3D
    ax.clear()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Balok 3D Bergerak')

    # Tampilkan balok 3D
    ax.scatter(cuboid_vertices[:, 0], cuboid_vertices[:, 1], cuboid_vertices[:, 2], c='r', marker='o')

# Inisialisasi plot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Animasi balok 3D
ani = animation.FuncAnimation(fig, animate, frames=360, interval=50)

plt.show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
from pyquaternion import Quaternion
import math

# Membuat sebuah quaternion (contoh)
quat = Quaternion(axis=[0, 1, 0], angle=math.radians(45))  # Quaternion dengan sumbu rotasi y dan sudut 45 derajat

# Menghitung pitch, roll, dan yaw
pitch = 45
roll = 0
yaw = 0

# Membuat titik-titik sudut kubus berdasarkan pitch, roll, yaw
def create_cube_vertices(pitch, yaw, roll, scale_factor=0.2):
    half_size = 0.5 * scale_factor
    vertices = np.array([
        [-half_size, -half_size, -half_size],
        [ half_size, -half_size, -half_size],
        [ half_size,  half_size, -half_size],
        [-half_size,  half_size, -half_size],
        [-half_size, -half_size,  half_size],
        [ half_size, -half_size,  half_size],
        [ half_size,  half_size,  half_size],
        [-half_size,  half_size,  half_size]
    ])

    rotation_matrix = Quaternion(axis=[0, 1, 0], angle=yaw).rotation_matrix
    rotated_vertices = np.dot(vertices, rotation_matrix.T)

    pitch_matrix = Quaternion(axis=[1, 0, 0], angle=pitch).rotation_matrix
    rotated_vertices = np.dot(rotated_vertices, pitch_matrix.T)

    roll_matrix = Quaternion(axis=[0, 0, 1], angle=roll).rotation_matrix
    rotated_vertices = np.dot(rotated_vertices, roll_matrix.T)

    return rotated_vertices

cube_vertices = create_cube_vertices(pitch, roll, yaw, scale_factor=0.2)

# Pindahkan kubus ke posisi tengah
center = np.mean(cube_vertices, axis=0)
cube_vertices -= center

# Definisikan sisi-sisi kubus
cube_faces = [
    [cube_vertices[0], cube_vertices[1], cube_vertices[2], cube_vertices[3]],
    [cube_vertices[4], cube_vertices[5], cube_vertices[6], cube_vertices[7]],
    [cube_vertices[0], cube_vertices[1], cube_vertices[5], cube_vertices[4]],
    [cube_vertices[2], cube_vertices[3], cube_vertices[7], cube_vertices[6]],
    [cube_vertices[1], cube_vertices[2], cube_vertices[6], cube_vertices[5]],
    [cube_vertices[4], cube_vertices[7], cube_vertices[3], cube_vertices[0]]
]

# Bagi sisi depan dan sisi lainnya
front_face = cube_faces[3]
other_faces = cube_faces[:3] + cube_faces[4:]

# Inisialisasi plot dengan ukuran yang lebih besar
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot sisi lainnya dengan warna cyan
ax.add_collection3d(Poly3DCollection(other_faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

# Plot sisi depan dengan warna merah
ax.add_collection3d(Poly3DCollection([front_face], facecolors='red', linewidths=1, edgecolors='r', alpha=.5))

# Set batas aksis XYZ
ax.set_xlim(-1, 1)  # Atur sesuai skala yang diinginkan
ax.set_ylim(-1, 1)  # Atur sesuai skala yang diinginkan
ax.set_zlim(-1, 1)  # Atur sesuai skala yang diinginkan

# Tambahkan garis sumbu X, Y, dan Z
ax.plot([0, 1], [0, 0], [0, 0], color='green', linewidth=2)  # Garis sumbu X
ax.plot([0, 0], [0, -1], [0, 0], color='red', linewidth=2)  # Garis sumbu Y
ax.plot([0, 0], [0, 0], [0, 1], color='blue', linewidth=2)  # Garis sumbu Z

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Cube with Pitch, Roll, and Yaw')

plt.show()

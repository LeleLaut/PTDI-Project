import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

# Inisialisasi plot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Membuat data balok 3D (cuboid)
length, width, height = 1, 2, 3
cuboid_vertices = np.array([
    [0, 0, 0],
    [length, 0, 0],
    [length, width, 0],
    [0, width, 0],
    [0, 0, height],
    [length, 0, height],
    [length, width, height],
    [0, width, height]
])

cuboid_edges = [
    [cuboid_vertices[0], cuboid_vertices[1]],
    [cuboid_vertices[1], cuboid_vertices[2]],
    [cuboid_vertices[2], cuboid_vertices[3]],
    [cuboid_vertices[3], cuboid_vertices[0]],
    [cuboid_vertices[4], cuboid_vertices[5]],
    [cuboid_vertices[5], cuboid_vertices[6]],
    [cuboid_vertices[6], cuboid_vertices[7]],
    [cuboid_vertices[7], cuboid_vertices[4]],
    [cuboid_vertices[0], cuboid_vertices[4]],
    [cuboid_vertices[1], cuboid_vertices[5]],
    [cuboid_vertices[2], cuboid_vertices[6]],
    [cuboid_vertices[3], cuboid_vertices[7]],
]

# Fungsi untuk merotasi balok 3D
def rotate_cuboid(angle):
    rot_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    rotated_cuboid = np.dot(cuboid_vertices, rot_matrix)
    return rotated_cuboid

# Data sudut rotasi (ubah sesuai dengan kebutuhan Anda)
angles = np.linspace(0, 2 * np.pi, 100)

# Animasi balok 3D berubah arah sesuai dengan data sudut rotasi
for angle in angles:
    ax.clear()
    rotated_cuboid = rotate_cuboid(angle)
    for edge in cuboid_edges:
        edge = np.array(edge)  # Convert the list of vertices to numpy array
        ax.plot3D(rotated_cuboid[edge[:, 0], 0], rotated_cuboid[edge[:, 0], 1], rotated_cuboid[edge[:, 0], 2], color='b')
    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    ax.set_zlim(0, height)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.pause(0.01)  # Pause to create animation effect
    plt.draw()
    time.sleep(0.01)

plt.show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

# Inisialisasi plot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Membuat data kubus
cube_vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

cube_edges = [
    [cube_vertices[0], cube_vertices[1]],
    [cube_vertices[1], cube_vertices[2]],
    [cube_vertices[2], cube_vertices[3]],
    [cube_vertices[3], cube_vertices[0]],
    [cube_vertices[4], cube_vertices[5]],
    [cube_vertices[5], cube_vertices[6]],
    [cube_vertices[6], cube_vertices[7]],
    [cube_vertices[7], cube_vertices[4]],
    [cube_vertices[0], cube_vertices[4]],
    [cube_vertices[1], cube_vertices[5]],
    [cube_vertices[2], cube_vertices[6]],
    [cube_vertices[3], cube_vertices[7]],
]

# Fungsi untuk merotasi kubus
def rotate_cube(angle):
    rot_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    rotated_cube = np.dot(cube_vertices, rot_matrix)
    return rotated_cube

# Data sudut rotasi (ubah sesuai dengan kebutuhan Anda)
angles = np.linspace(0, 2 * np.pi, 100)

# Animasi kubus berubah arah sesuai dengan data sudut rotasi
for angle in angles:
    ax.clear()
    rotated_cube = rotate_cube(angle)
    for edge in cube_edges:
        edge = np.array(edge)  # Convert the list of vertices to numpy array
        ax.plot3D(rotated_cube[edge[:, 0], 0], rotated_cube[edge[:, 0], 1], rotated_cube[edge[:, 0], 2], color='b')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.pause(0.01)  # Pause to create animation effect
    plt.draw()
    time.sleep(0.01)

plt.show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from pyquaternion import Quaternion
import math
import time

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

def read_data_from_file(filename):
    with open(filename, 'r') as file:
        data = file.readline().strip().split(',')
        pitch, roll, yaw = map(float, map(str.strip, data))
        return pitch, roll, yaw

data_filename = 'datas.txt'

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.plot([0, 1], [0, 0], [0, 0], color='green', linewidth=2)
ax.plot([0, 0], [0, 1], [0, 0], color='red', linewidth=2)
ax.plot([0, 0], [0, 0], [0, 1], color='blue', linewidth=2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Cube with Pitch, Roll, and Yaw')

# Initialize Poly3DCollection objects outside the loop
other_faces_collection = Poly3DCollection([], facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.25)
front_face_collection = Poly3DCollection([], facecolors='red', linewidths=1, edgecolors='r', alpha=0.5)
ax.add_collection3d(other_faces_collection)
ax.add_collection3d(front_face_collection)

# Loop
while True:
    pitch, roll, yaw = read_data_from_file(data_filename)
    cube_vertices = create_cube_vertices(pitch, roll, yaw, scale_factor=0.2)
    
    center = np.mean(cube_vertices, axis=0)
    cube_vertices -= center
    
    cube_faces = [
        [cube_vertices[0], cube_vertices[1], cube_vertices[2], cube_vertices[3]],
        [cube_vertices[4], cube_vertices[5], cube_vertices[6], cube_vertices[7]],
        [cube_vertices[0], cube_vertices[1], cube_vertices[5], cube_vertices[4]],
        [cube_vertices[2], cube_vertices[3], cube_vertices[7], cube_vertices[6]],
        [cube_vertices[1], cube_vertices[2], cube_vertices[6], cube_vertices[5]],
        [cube_vertices[4], cube_vertices[7], cube_vertices[3], cube_vertices[0]]
    ]
    front_face = cube_faces[3]
    other_faces = cube_faces[:3] + cube_faces[4:]

    other_faces_collection.set_verts(other_faces)
    front_face_collection.set_verts([front_face])

    plt.pause(1)
    ax.view_init(azim=30, elev=30)  # Adjust the view angle if needed
    plt.draw()
    ax.clear()
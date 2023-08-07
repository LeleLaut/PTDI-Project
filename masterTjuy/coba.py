import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pyquaternion import Quaternion

# Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define vertices of a cube
vertices = np.array([
    [-1, -1, -1],
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, -1],
    [1, 1, 1]
])

# Define faces of the cube using vertex indices
faces = [
    [vertices[0], vertices[1], vertices[3], vertices[2]],
    [vertices[4], vertices[5], vertices[7], vertices[6]],
    [vertices[0], vertices[1], vertices[5], vertices[4]],
    [vertices[2], vertices[3], vertices[7], vertices[6]],
    [vertices[1], vertices[3], vertices[7], vertices[5]],
    [vertices[0], vertices[2], vertices[6], vertices[4]]
]

# Define rotation angles around each axis based on xyz variables
rotation_angle_x = np.radians(30) * 2  # Rotation around x-axis (in radians)
rotation_angle_y = np.radians(45) * 3  # Rotation around y-axis (in radians)
rotation_angle_z = np.radians(60) * 4  # Rotation around z-axis (in radians)

# Create a rotation quaternion using the combined rotation angles
combined_rotation_quaternion = Quaternion(axis=[1, 1, 1], angle=rotation_angle_x + rotation_angle_y + rotation_angle_z)

# Rotate the cube vertices using the combined quaternion
rotated_vertices = [combined_rotation_quaternion.rotate(vertex) for vertex in vertices]

# Plot the rotated cube
cube = Poly3DCollection(faces, linewidths=1, edgecolors='r', alpha=0.2)
cube.set_facecolor('b')
ax.add_collection3d(cube)

# Set plot limits
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Graph with Rotated Cube')

# Show the plot
plt.show()

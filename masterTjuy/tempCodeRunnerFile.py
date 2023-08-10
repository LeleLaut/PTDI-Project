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
            ax.plot([0, 0], [0, 1], [0, 0], color='red', linewidth=2)  # Garis sumbu Y
            ax.plot([0, 0], [0, 0], [0, 1], color='blue', linewidth=2)  # Garis sumbu Z

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('3D Cube with Pitch, Roll, and Yaw')
                        # ... (rest of your cube visualization code)

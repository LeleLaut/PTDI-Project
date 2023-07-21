import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Fungsi untuk menghitung ketinggian (z) berdasarkan x dan y
def parabola_func(x, y):
    a = 0.1  # Konstanta a
    b = 0.1  # Konstanta b
    c = 10   # Konstanta c
    return a * x**2 + b * y**2 + c

# Rentang waktu dan jumlah langkah
time_steps = 100
t = np.linspace(0, 10, time_steps)

# Rentang koordinat x dan y
x_range = np.linspace(-10, 10, time_steps)
y_range = np.linspace(-10, 10, time_steps)

# Membuat grid untuk x dan y
X, Y = np.meshgrid(x_range, y_range)

# Menghitung ketinggian (z) untuk setiap titik pada setiap waktu t
Z = parabola_func(X, Y)

# Membuat visualisasi 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot garis gerak parabola
for i in range(time_steps):
    ax.plot([X[i, i]], [Y[i, i]], [Z[i, i]], 'bo', markersize=4)  # Titik pergerakan
    #ax.plot(X[:i, i], Y[:i, i], Z[:i, i], color='blue', alpha=0.5)  # Garis pergerakan

# Tambahkan label sumbu
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Tambahkan judul
plt.title('Gerak Parabola Sebagai Garis dalam Koordinat 3D')

# Tampilkan plot
plt.show()

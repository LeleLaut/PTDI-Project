import numpy as np
import matplotlib.pyplot as plt

# Data integer
x = np.array([1, 2, 3, 4, 5])
y = np.array([10, 15, 7, 12, 8])

# Buat plot
plt.plot(x, y, marker='o', linestyle='-')

# Posisi koordinat angka terakhir
last_x = x[-1]
last_y = y[-1]

# Tambahkan teks untuk angka terakhir
plt.text(last_x, last_y, f'({last_x}, {last_y})', ha='right', va='bottom')

# Atur label sumbu dan judul
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Grafik Data Integer')

# Tampilkan plot
plt.show()

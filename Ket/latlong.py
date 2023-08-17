import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Data awal
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Buat plot awal
fig, ax = plt.subplots()
line, = ax.plot(x, y)

# Buat tombol
button_ax = plt.axes([0.7, 0.05, 0.1, 0.075])
button = Button(button_ax, 'Tampilkan Data')

# Fungsi yang akan dipanggil saat tombol ditekan
def show_data(event):
    # Simpan data baru yang ingin ditampilkan di tengah-tengah
    new_x = np.array([4, 6])
    new_y = np.sin(new_x)
    
    # Update data plot
    line.set_data(new_x, new_y)
    
    # Perbarui tampilan plot
    plt.draw()

# Tambahkan fungsi ke tombol
button.on_clicked(show_data)

plt.show()

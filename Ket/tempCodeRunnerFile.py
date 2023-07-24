import matplotlib.animation as mpla
import matplotlib.pyplot as plt
import numpy as np

# Create data
T = np.linspace(0, 2 * np.pi, 100)
S = np.sin(T)
P = np.cos(T)

# Create the figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 8))
fig.suptitle('Grafik Trigonometri', fontsize=14, fontweight='bold')

# Line plots
line, = axs[0].plot(T, S, color='blue', label='sin(x)')
line2, = axs[1].plot(T, P, color='red', label='cos(x)')
line3, = axs[2].plot(S, T, color='green', label='sin(x)')

# Set titles and labels
axs[0].set_title('Grafik Sinus')
axs[1].set_title('Grafik Kosinus')
axs[2].set_title('Grafik Sinus terhadap Nilai x')

for ax in axs:
    ax.set_xlabel('Nilai x')
    ax.set_ylabel('Nilai y')
    ax.legend()

# Animation function
def animate(i):
    line.set_ydata(np.sin(T + i / 50))
    line2.set_ydata(np.cos(T + i / 50))
    line3.set_ydata(np.sin(T + i / 50))

# Create the animation
anim = mpla.FuncAnimation(fig, animate, interval=50)

plt.tight_layout()
plt.show()

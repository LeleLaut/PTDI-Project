import matplotlib.animation as mpla
import matplotlib.pyplot as plt
import numpy as np

T = np.linspace(0, 2 * np.pi, 100)
S = np.sin(T)
P = np.cos(T)
line, = plt.plot(T, S)
line2, = plt.plot(T, P)
line1, = plt.plot(S, T)

def animate(i):
    line.set_ydata(np.sin(T + i / 50))
    line2.set_ydata(np.cos(T + i / 50))
    line1.set_ydata(np.sin(T + i / 50))

anim = mpla.FuncAnimation(plt.gcf(), animate, interval=5)
plt.show()

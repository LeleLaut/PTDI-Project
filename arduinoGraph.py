import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib import style

plt.style.use('ggplot')

fig2 = plt.figure()
fig2.suptitle('Grafik Pitch, Roll, dan Yaw', fontsize=8, fontweight='bold')
fig2.set_size_inches(6, 4)
ax2 = fig2.add_subplot(1, 1, 1)

def animate(i):
    graph_data = open('mqtt_logs.csv', 'r').readlines()
    lines = graph_data[1:]
    GX = []
    GY = []
    GZ = []
    AX = []
    AY = []
    AZ = []
    P = []
    R = []
    Y = []
    for line in lines:
        if len(line) > 1:
            x, y, z, x1, y1, z1, p, r, y = line.split(',')
            GX.append(float(x))
            GY.append(float(y))
            GZ.append(float(z))
            AX.append(float(x1))
            AY.append(float(y1))
            AZ.append(float(z1))
            P.append(float(p))
            R.append(float(r))
            Y.append(float(y))

    # Limit the data to show only the last 5 points
    P = P[-5:]
    R = R[-5:]
    Y = Y[-5:]

    ax2.clear()
    xs = list(range(len(P)))  # Create a list of indices as xs
    ax2.plot(xs, P, label='Pitch', marker='.')
    ax2.plot(xs, R, label='Roll', marker='.')
    ax2.plot(xs, Y, label='Yaw', marker='.')
    ax2.set_ylim(-20, 20)
    ax2.set_ylabel("Nilai")
    ax2.set_xlabel("TimeStamp (s)")
    ax2.legend()

open('data.txt', 'w').close()

timestamp = -1
ani = animation.FuncAnimation(fig2, animate, interval=1000)

while True:
    # generate_random_data(timestamp)
    timestamp += 1
    plt.pause(1)

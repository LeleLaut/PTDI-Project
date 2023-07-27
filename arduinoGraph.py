import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib import style

plt.style.use('ggplot')

# Create a figure with 4 subplots
fig, ((ax2, ax3, ax4)) = plt.subplots(3,1, figsize=(8, 6))
fig.suptitle('Grafik Data', fontsize=12, fontweight='bold')

def animate(i):
    graph_data = open('mqtt_logs_andro.csv', 'r').readlines()
    #print (graph_data)
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
            x, y, z, x1, y1, z1, p, r, y,a,b= line.split(',')
            GX.append(float(x))
            GY.append(float(y))
            GZ.append(float(z))
            AX.append(float(x1))
            AY.append(float(y1))
            AZ.append(float(z1))
            P.append(float(p))
            R.append(float(r))
            Y.append(float(y))

    # Limit the data to show only the last 10 points
    GX = GX[-10:]
    GY = GY[-10:]
    GZ = GZ[-10:]
    AX = AX[-10:]
    AY = AY[-10:]
    AZ = AZ[-10:]
    P = P[-10:]
    R = R[-10:]
    Y = Y[-10:]

    ax2.clear()
    xs = list(range(len(GX)))  # Create a list of indices as xs
    ax2.plot(xs, GX, label='GX', marker='.')
    ax2.plot(xs, GY, label='GY', marker='.')
    ax2.plot(xs, GZ, label='GZ', marker='.')
    ax2.set_ylim(-360, 360)
    ax2.set_ylabel("Nilai")
    ax2.set_xlabel("TimeStamp (s)")
    ax2.legend()

    ax3.clear()
    ax3.plot(xs, AX, label='AX', marker='.')
    ax3.plot(xs, AY, label='AY', marker='.')
    ax3.plot(xs, AZ, label='AZ', marker='.')
    ax3.set_ylim(-90,90)
    ax3.set_ylabel("Nilai")
    ax3.set_xlabel("TimeStamp (s)")
    ax3.legend()

    ax4.clear()
    ax4.plot(xs, P, label='Pitch', marker='.')
    ax4.set_ylim(-360, 360)
    ax4.plot(xs, R, label='Roll', marker='.')
    ax4.plot(xs, Y, label='Yaw', marker='.')
    ax4.set_ylabel("Nilai")
    ax4.set_xlabel("TimeStamp (s)")
    ax4.legend()

    

open('mqtt_logs.csv', 'w').close()

timestamp = -1
ani = animation.FuncAnimation(fig, animate, interval=1000)

while True:
    # generate_random_data(timestamp)
    timestamp += 1
    plt.pause(1)

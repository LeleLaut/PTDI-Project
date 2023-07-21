import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib import style

plt.style.use('ggplot')

fig = plt.figure()
fig.suptitle('Grafik Ketinggian', fontsize=8, fontweight='bold')
fig.set_size_inches(6, 4)
fig2 = plt.figure()
fig2.suptitle('Grafik pitch', fontsize=8, fontweight='bold')
fig2.set_size_inches(6, 4)
ax1 = fig.add_subplot(1, 1, 1)
ax2 = fig2.add_subplot(1, 1, 1)

def generate_random_data(timestamp):
    with open('data.txt', 'a') as file:
        for i in range(1):
            ketinggian = random.randint(0, 100)
            pitch = random.randint(-20, 20)
            roll = random.randint(-20, 20)
            yaw = random.randint(-20, 20)
            file.write(f"{ketinggian}, {timestamp}, {pitch}, {roll}, {yaw}\n")
        print(ketinggian)

def animate(i):
    graph_data = open('data.txt', 'r').readlines()
    lines = graph_data[1:]
    xs = []
    ys = []
    zs = []
    vs = []
    ws = []
    for line in lines:
        if len(line) > 1:
            y, x, z, v, w = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
            zs.append(float(z))
            vs.append(float(v))
            ws.append(float(w))
    # print (xs + ys + zs)
    ax1.clear()
    ax1.plot(xs, ys)
    ax1.set_ylabel("Ketinggian")
    ax1.set_xlabel("TimeStamp (s)")
    ax2.clear()
    ax2.plot(xs, zs, xs, ws, xs, vs)
    ax2.set_ylabel("pitch")
    ax2.set_xlabel("TimeStamp (s)")
    #plt.savefig("Hasil_Update_PNG.png")

open('data.txt', 'w').close()

timestamp = -1
ani = animation.FuncAnimation(fig, animate, interval=1000)

while True:
    generate_random_data(timestamp)
    timestamp += 1
    plt.pause(1)

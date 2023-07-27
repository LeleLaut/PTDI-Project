import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib import style

plt.style.use('ggplot')

# Create a single figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))

# Set titles for each subplot
ax1.set_title('Grafik Ketinggian', fontsize=8, fontweight='bold')
ax2.set_title('Grafik Pitch, Roll, dan Yaw', fontsize=8, fontweight='bold')

def generate_random_data(timestamp):
    with open('data.txt', 'a') as file:
        for i in range(1):
            ketinggian = random.randint(0, 100)
            pitch = random.randint(-5, 5)
            roll = random.randint(-5, 5)
            yaw = random.randint(-5, 5)
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

    # Limit the data to show only the last 5 points
    xs = xs[-5:]
    ys = ys[-5:]
    zs = zs[-5:]
    vs = vs[-5:]
    ws = ws[-5:]

    ax1.clear()
    ax1.plot(xs, ys)
    ax1.set_ylabel("Ketinggian")
    ax1.set_xlabel("TimeStamp (s)")

    ax2.clear()
    ax2.plot(xs, zs, label='Pitch' , marker = '.')
    ax2.plot(xs, ws, label='Roll' , marker = '.')
    ax2.plot(xs, vs, label='Yaw' , marker = '.')
    ax2.set_ylim(-20, 20)
    ax2.set_ylabel("Nilai")
    ax2.set_xlabel("TimeStamp (s)")
    ax2.legend()

open('data.txt', 'w').close()

timestamp = -1
ani = animation.FuncAnimation(fig, animate, interval=1000)

while True:
    generate_random_data(timestamp)
    timestamp += 1
    plt.pause(1)

# Show the combined figure
plt.show()

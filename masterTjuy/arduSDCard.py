import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create a figure with 3 subplots
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, figsize=(8, 6))

fig.suptitle('Grafik Data Arduino', fontsize=12, fontweight='bold')

def animate(i):
    graph_data = open('data.txt', 'r').readlines()
    #graph_data = graph_data.replace('"', '')
    lines = graph_data[1:]  # Skip header line
    lines = [elem.replace('"', '') for elem in lines]
    
    GX = []
    GY = []
    GZ = []
    AX = []
    AY = []
    AZ = []
    P = []
    R = []
    Y = []
    Time = []
    for line in lines:
        # print(graph_data)
        if len(line) > 1:
            x, y, z, x1, y1, z1, p, r, y, t= line.split(',')
            GX.append(float(x))
            GY.append(float(y))
            GZ.append(float(z))
            AX.append(float(x1))
            AY.append(float(y1))
            AZ.append(float(z1))
            P.append(float(p))
            R.append(float(r))
            Y.append(float(y))
            Time.append(float(t))


    i_minus_10 = max(0, i - 10)

    # Limit the data to show only the last 10 points
    GX = GX[i_minus_10:i+1]
    GY = GY[i_minus_10:i+1]
    GZ = GZ[i_minus_10:i+1]
    AX = AX[i_minus_10:i+1]
    AY = AY[i_minus_10:i+1]
    AZ = AZ[i_minus_10:i+1]
    P = P[i_minus_10:i+1]
    R = R[i_minus_10:i+1]
    Y = Y[i_minus_10:i+1]
    Time = Time[i_minus_10:i+1]


    ax1.clear()
    ax1.plot(Time, GX, label='GX', marker='.')
    ax1.plot(Time, GY, label='GY', marker='.')
    ax1.plot(Time, GZ, label='GZ', marker='.')
    ax1.set_ylim(-360, 360)
    ax1.set_ylabel("Nilai")
    ax1.set_xlabel("TimeStamp (s)")
    ax1.legend()

    ax2.clear()
    ax2.plot(Time, AX, label='AX', marker='.')
    ax2.plot(Time, AY, label='AY', marker='.')
    ax2.plot(Time, AZ, label='AZ', marker='.')
    ax2.set_ylim(-90, 90)
    ax2.set_ylabel("Nilai")
    ax2.set_xlabel("TimeStamp (s)")
    ax2.legend()

    ax3.clear()
    ax3.plot(Time, P, label='Pitch', marker='.')
    ax3.plot(Time, R, label='Roll', marker='.')
    ax3.plot(Time, Y, label='Yaw', marker='.')
    ax3.set_ylim(-360, 360)
    ax3.set_title('Arduino')
    ax3.set_ylabel("Nilai")
    ax3.set_xlabel("TimeStamp (s)")
    ax3.legend()

# Create the animation outside the animate function
ani = animation.FuncAnimation(fig, animate, interval=500)

# Show the plot
plt.show()
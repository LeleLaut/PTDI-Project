import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib import style

plt.style.use('ggplot')

# Create a figure with 5 subplots
fig2, ((ax4, ax5, ax6)) = plt.subplots(3,1, figsize=(8, 6))
fig2.suptitle('Grafik Data Android', fontsize=12, fontweight='bold')



def animate(i):

    # Read data from the mqtt_logs_andro.csv file for the fifth subplot (assuming the format is the same)
    graph_data_andro = open('mqtt_logs_ardu.csv', 'r').readlines()
    lines_andro = graph_data_andro[1:]
    DataX = []
    DataY = []
    DataZ = []
    DataX1 = []
    DataY1 = []
    DataZ1 = []
    P_andro = []
    R_andro = []
    Y_andro = []
    A_andro = []
    L_andro = []
    Time_andro = []
    for line in lines_andro:
        if len(line) > 1:
            x, y, z, x1, y1, z1, p, r, y, a, l, t = line.split(',')
            DataX.append(float(x))
            DataY.append(float(y))
            DataZ.append(float(z))
            DataX1.append(float(x1))
            DataY1.append(float(y1))
            DataZ1.append(float(z1))
            P_andro.append(float(p))
            R_andro.append(float(r))
            Y_andro.append(float(y))
            A_andro.append(float(a))
            L_andro.append(float(l))
            Time_andro.append(float(t))

    # Limit the data to show only the last 10 points
    DataX = DataX[-10:]
    DataY = DataY[-10:]
    DataZ = DataZ[-10:]
    DataX1 = DataX1[-10:]
    DataY1 = DataY1[-10:]
    DataZ1 = DataZ1[-10:]
    P_andro = P_andro[-10:]
    R_andro = R_andro[-10:]
    Y_andro = Y_andro[-10:]
    A_andro = A_andro[-10:]
    L_andro = L_andro[-10:]
    Time_andro = Time_andro[-10:]

    ax4.clear()
    ax4.plot(Time_andro, DataX, label='DataX', marker='.')
    ax4.plot(Time_andro, DataY, label='DataY', marker='.')
    ax4.plot(Time_andro, DataZ, label='DataZ', marker='.')
    ax4.set_ylim(-360, 360)
    ax4.set_ylabel("Nilai")
    ax4.set_xlabel("TimeStamp (s)")
    ax4.legend()

    ax5.clear()
    ax5.plot(Time_andro, DataX1, label='DataX1', marker='.')
    ax5.plot(Time_andro, DataY1, label='DataY1', marker='.')
    ax5.plot(Time_andro, DataZ1, label='DataZ1', marker='.')
    ax5.set_ylim(-90,90)
    ax5.set_ylabel("Nilai")
    ax5.set_xlabel("TimeStamp (s)")
    ax5.legend()

    ax6.clear()
    ax6.plot(Time_andro, P_andro, label='Pitch', marker='.')
    ax6.plot(Time_andro, R_andro, label='Roll', marker='.')
    ax6.plot(Time_andro, Y_andro, label='Yaw', marker='.')
    ax6.set_ylim(-360, 360)
    ax6.set_ylabel("Nilai")
    ax6.set_xlabel("TimeStamp (s)")
    ax6.set_title('Android')
    ax6.legend()

    

open('mqtt_logs_andro.csv', 'w').close()  # Create and clear the mqtt_logs_andro.csv file

timestamp = -1
ani = animation.FuncAnimation(fig2, animate, interval=1000)

while True:
    # generate_random_data(timestamp)
    plt.pause(1)

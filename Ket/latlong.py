import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from matplotlib import style

plt.style.use('ggplot')

# Create a figure with 5 subplots
fig, ((ax3, ax7, ax6),(ax2, ax8, ax5),(ax1, ax9, ax4)) = plt.subplots(3,3, figsize=(8, 6))
fig.suptitle('Grafik Data Arduino', fontsize=12, fontweight='bold')

def animate(i):
    # Read data from the mqtt_logs_ardu.csv file
    graph_data = pd.read_csv('mqtt_logs_ardu.csv')
    GX = graph_data['GX']
    GY = graph_data['GY']
    GZ = graph_data['GZ']
    AX = graph_data['AX']
    AY = graph_data['AY']
    AZ = graph_data['AZ']
    P = graph_data['P']
    R = graph_data['R']
    Y = graph_data['Y']
    Time = graph_data['Time']

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
    Time = Time[-10:]

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

    # Read data from the mqtt_logs_andro.csv file
    graph_data_andro = pd.read_csv('mqtt_logs_andro.csv')
    DataX = graph_data_andro['DataX']
    DataY = graph_data_andro['DataY']
    DataZ = graph_data_andro['DataZ']
    DataX1 = graph_data_andro['DataX1']
    DataY1 = graph_data_andro['DataY1']
    DataZ1 = graph_data_andro['DataZ1']
    P_andro = graph_data_andro['Pitch']
    R_andro = graph_data_andro['Roll']
    Y_andro = graph_data_andro['Yaw']
    L_andro = graph_data_andro['longitude']  # Longitude
    A_andro = graph_data_andro['altitude']   # Altitude
    Time_andro = graph_data_andro['Time']

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
    L_andro = L_andro[-10:]  # Limit the longitude data to the last 10 points
    A_andro = A_andro[-10:]  # Limit the altitude data to the last 10 points
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

    ax7.clear()
    ax7.plot(Time_andro, P_andro, label='Pitch (Android)', marker='.')
    ax7.plot(Time, P, label='Pitch (Arduino)', marker='.')
    ax7.set_ylim(-180, 180)
    ax7.set_ylabel("Nilai")
    ax7.set_xlabel("TimeStamp (s)")
    ax7.set_title('Perbandingan')
    ax7.legend()

    ax8.clear()
    ax8.plot(Time_andro, R_andro, label='Roll (Android)', marker='.')
    ax8.plot(Time, R, label='Roll (Arduino)', marker='.')
    ax8.set_ylim(-180, 180)
    ax8.set_ylabel("Nilai")
    ax8.set_xlabel("TimeStamp (s)")
    ax8.legend()

    ax9.clear()
    ax9.plot(Time_andro, Y_andro, label='Yaw (Android)', marker='.')
    ax9.plot(Time, Y, label='Yaw (Arduino)', marker='.')
    ax9.set_ylim(0, 360)
    ax9.set_ylabel("Nilai")
    ax9.set_xlabel("TimeStamp (s)")
    ax9.legend()

# Menjalankan animasi dengan interval 1000 ms (1 detik)
ani = animation.FuncAnimation(fig, animate, interval=1000)

# Menampilkan plot
plt.show()
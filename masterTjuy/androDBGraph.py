import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create a figure with 3 subplots
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, figsize=(8, 6))
fig.suptitle('Grafik Data Arduino', fontsize=12, fontweight='bold')

def convert_degrees(degrees):
    while degrees > 180:
        degrees -= 360
    while degrees < -180:
        degrees += 360
    return degrees

def animate(i):
    graph_data = open('android6.csv', 'r').readlines()
    #graph_data = graph_data.replace('"', '')
    lines = graph_data[1:]  # Skip header line
    lines = [elem.replace('"', '') for elem in lines]
    
    ID = []
    GX = []
    GY = []
    GZ = []
    AX = []
    AY = []
    AZ = []
    P = []
    R = []
    Y = []
    Long = []
    Lat = []
    Alt = []
    TS = []
    Time = []
    for line in lines:
        # print(graph_data)
        if len(line) > 1:
            _, x, y, z, x1, y1, z1, p, r, y, _, _, _, c, _  = line.split(',')
            # x, y, z, x1, y1, z1, p, r, y, long ,lat,alt = line.split(',')
            #  ID.append(float(id))
            GX.append(float(x))
            GY.append(float(y))
            GZ.append(float(z))
            AX.append(float(x1))
            AY.append(float(y1))
            AZ.append(float(z1))
            P.append(float(p))
            R.append(float(r))
            Y.append(float(y))
            Time.append(float(c))
            # Long.append(float(long))
            # Lat.append(float(lat))
            # TS.append(float(ts))

    # Calculate the variable containing i-10
    i_minus_10 = max(0, i - 10)

    # Limit the data to show only the last 10 points
    GX = GX[i_minus_10:i]
    GY = GY[i_minus_10:i]
    GZ = GZ[i_minus_10:i]
    AX = AX[i_minus_10:i]
    AY = AY[i_minus_10:i]
    AZ = AZ[i_minus_10:i]
    P = P[i_minus_10:i]
    R = R[i_minus_10:i]
    Y = Y[i_minus_10:i]
    Time = Time[i_minus_10:i]
    # Long = Long[i_minus_10:i]
    # Lat = Lat[i_minus_10:i]
    

    Y_converted = [convert_degrees(y) for y in Y]

    if len(Y_converted) == 0:
        point_Y = 0
    else :
        point_Y = Y_converted[-1]
    
    if len(R) == 0:
        point_R = 0
    else :
        point_R = R[-1]

    if len(P) == 0:
        print("mas")
        point_P = 0
    else :
        point_P = P[-1]

    if len(Time) == 0:
        print("mas")
        Point_Time = 0
    else :
        Point_Time = Time[-1]

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
    ax3.plot(Time, Y_converted, label='Yaw', marker='.')
    ax3.set_ylim(-180, 180)
    ax3.set_title('Arduino')
    ax3.set_ylabel("Nilai")
    ax3.set_xlabel("TimeStamp (s)")
    ax3.legend()
    ax3.text( Point_Time, point_P,  f'({point_P})', ha='right', va='bottom')
    ax3.text( Point_Time, point_R, f'({point_R})', ha='right', va='bottom')
    ax3.text( Point_Time, point_Y, f'({point_Y})', ha='right', va='bottom')



# Create the animation outside the animate function
hz = int(input("Berapa Hz :"))
intv = 1/hz * 1000
ani = animation.FuncAnimation(fig, animate, interval=intv)

# Show the plot
plt.show()



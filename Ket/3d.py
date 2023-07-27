import matplotlib.pyplot as plt
import numpy as np

# Create some sample data
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create a figure and two subplots (axes) within it
fig, (ax1, ax2) = plt.subplots(2, 1)

# Plot the first graph in the first subplot
ax1.plot(x, y1, label='Sin(x)', color='b')
ax1.set_title('Graph 1: Sin(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.legend()

# Plot the second graph in the second subplot
ax2.plot(x, y2, label='Cos(x)', color='r')
ax2.set_title('Graph 2: Cos(x)')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.legend()

# Adjust the layout to avoid overlapping labels
plt.tight_layout()

# Show the figure with both graphs
plt.show()

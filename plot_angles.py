import numpy as np
import matplotlib.pyplot as plt

# Load binary file back into numpy array
angles = np.fromfile("angles.bin", dtype=np.float32)

# Filter out the 'spikes'
angles = [x for x in angles if x > np.average(angles)]

x = np.arange(len(angles))
m, b = np.polyfit(x, angles, 1)

plt.plot(angles)
plt.title("Periapsis Angle Over Time")
plt.xlabel("Orbit")
plt.ylabel("Angle (degrees)")
plt.plot(x, m * x + b, "r--")  # Fits y = mx + b directly
plt.show()
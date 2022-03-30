import matplotlib.pyplot as plt
import numpy as np

avPCO2 = np.array([0.99,30.5,24.5,25.4,26.5,17.5])

avDLI = np.array([7,4,3,8,2,1])

xpoints = np.array([0,1,2,3,4,5,6,7,8,9,10])
y = np.array([0,10,20,30,40,50,60,70,80,90,100])

plotTime1 = "Dienstag"
plotTime2 = "Mittwoch"

fig, ax1 = plt.subplots()

plt.suptitle("Average pCO2 and Temp from " + plotTime1 + " to " + plotTime2)

color = 'tab:red'
ax1.set_xlabel('time (min)')
ax1.set_ylabel('pCO2', color = color)
ax1.plot(avPCO2, color = color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('DLI', color = color)
ax2.plot(avDLI, color = color)

fig.tight_layout()

fig.savefig('/home/pi/Documents/Figures/test.png')

plt.show()

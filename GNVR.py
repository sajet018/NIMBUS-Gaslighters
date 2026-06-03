import numpy as np
import matplotlib.pyplot as plt
d = float(input("Enter the hull diameter in centimetres. "))
def gnvr_profile(x, D):
    if x<0 or x>3.05*D:
        return 0.0
    if x<1.25*D:
        return 0.5*D*np.sqrt(max(0.0, 1.0-((x/(1.25*D))-1.0)**2))
    elif x<=2.875*D:
        return np.sqrt(max(0.0, (4.0*D)**2-(x-1.25*D)**2))-3.5*D
    else:
        val = 0.1373*D*(1.8*D-(x-1.25*D))
        return np.sqrt(max(0.0, val))
x1 = np.linspace(0, 3.05*d, 4000)
y1 = []
y2 = []
for x2 in x1:
    y1.append(gnvr_profile(x2, d))
    y2.append(-gnvr_profile(x2, d))
plt.plot(x1, y1, lw=2, color="black")
plt.plot(x1, y2, lw=2, color="black")
plt.title("GNVR Profile", fontsize=18)
plt.xlabel("x (m)", fontsize = 14)
plt.ylabel("r (m)", fontsize = 14)
plt.show()
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("qt4agg")
import matplotlib.pyplot as plt

fn = ["./threadedcylinder-lengths.csv",
      "./ywosupports-lengths.csv",
      "./keyring-lengths.csv",
      ]

leg_text = ["Cylinder", "Y", "Key Ring"]
unit_conv = 1000.0

# Plot averages
plt.figure()
for F in fn:
    D = pd.read_csv(F)
    plt.plot(unit_conv*D["Avg."])

plt.title("Average contour length")
plt.xlabel("Layer Index")
plt.ylabel("Length (mm)")
plt.legend(leg_text)
plt.savefig("avg_contour_length.png")

# Plot averages w/ std dev
plt.figure()
for F in fn:
    D = pd.read_csv(F)
    plt.errorbar(np.arange(0.0, D["Avg."].size, 1), unit_conv*D["Avg."], yerr=unit_conv*D["Dev."])

plt.title("Average contour length w/ std dev")
plt.xlabel("Layer Index")
plt.ylabel("Length (mm)")
plt.legend(leg_text)
plt.savefig("dev_contour_length.png")

# Plot min
plt.figure()
for F in fn:
    D = pd.read_csv(F)
    plt.plot(unit_conv*D["Min"])

plt.title("Min contour length")
plt.xlabel("Layer Index")
plt.ylabel("Length (mm)")
plt.legend(leg_text)
plt.savefig("min_contour_length.png")

# Plot max
plt.figure()
for F in fn:
    D = pd.read_csv(F)
    plt.plot(unit_conv*D["Max"])

plt.title("Max contour length")
plt.xlabel("Layer Index")
plt.ylabel("Length (mm)")
plt.legend(leg_text)
plt.savefig("max_contour_length.png")

plt.show()


import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use("qt4agg")
import matplotlib.pyplot as plt

line_colors = list(mpl.rcParams['axes.prop_cycle'])

fn = ["./threadedcylinder-lengths.csv",
      "./ywosupports-lengths.csv",
      "./keyring-lengths.csv",
      "./propeller-lengths.csv",
      ]

leg_text = ["Cylinder", "Y", "Key Ring", "Propeller"]
unit_conv = 1000.0

# Plot averages
plt.figure()
for F in fn:
    D = pd.read_csv(F)
    plt.plot(unit_conv*D["Avg."])
    print F + " overall avg: " + str(D["Avg."].mean())

plt.title("Average contour length")
plt.xlabel("Layer Index")
plt.ylabel("Length (mm)")
plt.legend(leg_text)
plt.savefig("avg_contour_length.png")

# Plot averages w/ std dev
for k,F in enumerate(fn):
    plt.figure()
    D = pd.read_csv(F)
    plt.errorbar(np.arange(0.0, D["Avg."].size, 1), unit_conv*D["Avg."],
            yerr=unit_conv*D["Dev."], color=line_colors[k]['color'])
    print F + " avg of std devs: " + str(D["Dev."].mean())

    plt.title("Average contour length w/ std dev: " + leg_text[k])
    plt.xlabel("Layer Index")
    plt.ylabel("Length (mm)")
    plt.savefig("dev_contour_length_" + leg_text[k].replace(" ","") + ".png")

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


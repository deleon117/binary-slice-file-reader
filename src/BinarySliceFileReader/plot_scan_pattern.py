import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("qt4agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

if not len(sys.argv) == 3:
    print "Usage: python plot_scan_pattern.py <name of summary file> <gif flag:0 or 1>"
    sys.exit()

if not sys.argv[2].isdigit():
    print "Usage: python plot_scan_pattern.py <name of summary file> <gif flag:0 or 1>"
    print "Input Error: gif flag must be a number: 0 or 1"
    sys.exit()

if int(sys.argv[2]) < 0 or int(sys.argv[2]) > 1:
    print "Usage: python plot_scan_pattern.py <name of summary file> <gif flag:0 or 1>"
    print "Input Error: gif flag must be a number: 0 or 1"
    sys.exit()

f = open(sys.argv[1],"r")
A = pd.DataFrame(f.readlines())

# Find fill-scan block headers
inds = A.loc[A[0] == 'x1\ty1\tx2\ty2\n'].index

if not list(inds.values):
    print "No scan blocks found. Exiting..."
    sys.exit()

# Grab all fill-scan vectors
# IMPORTANT: If formatting changes, will have to adjust hard-coded values
section_line_front = 1
section_line_back = 6
allScans = []
for i in range(len(inds)-1):
    allScans.append([x[0] for x in A.loc[inds[i]+section_line_front:inds[i+1]-section_line_back].values.tolist()])

# Get last block
allScans.append([x[0] for x in A.loc[inds[-1]+1:A.size-5].values.tolist()])
allScans = [x.replace("\t",",").replace("\n","") for y in allScans for x in y]

# Parse entries and store
x = []
y = []
for s in allScans:
    sps = s.split(",")
    x.append(float(sps[0]))
    y.append(float(sps[1]))
    x.append(float(sps[2]))
    y.append(float(sps[3]))


# Animate the fill scans
fig, ax = plt.subplots()

line, = ax.plot(x[0], y[0], marker="x")
ax.set_xlim([min(x),max(x)])
ax.set_ylim([min(y),max(y)])


def animate(i):
    line.set_xdata(x[:i])  # update the data
    line.set_ydata(y[:i])  # update the data
    return line,


# Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(x)), init_func=init,
                              interval=25, blit=True)
if int(sys.argv[2]):
    ani.save(sys.argv[1] + "_scan.gif", writer="imagemagick", fps=20)

# Plot the fill scan start and end points
fig = plt.figure()
plt.scatter(x, y, s=2)

plt.show()

#pd.DataFrame([x,y]).T.to_csv("canon_layer0457_scan.csv", index=None, header=None)

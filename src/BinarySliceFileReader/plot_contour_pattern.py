import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("qt4agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

if not len(sys.argv) == 3:
    print "Usage: python plot_contour_pattern.py <name of summary file> <gif flag:0 or 1>"
    sys.exit()

if not sys.argv[2].isdigit():
    print "Usage: python plot_contour_pattern.py <name of summary file> <gif flag:0 or 1>"
    print "Input Error: gif flag must be a number: 0 or 1"
    sys.exit()

if int(sys.argv[2]) < 0 or int(sys.argv[2]) > 1:
    print "Usage: python plot_contour_pattern.py <name of summary file> <gif flag:0 or 1>"
    print "Input Error: gif flag must be a number: 0 or 1"
    sys.exit()

f = open(sys.argv[1],"r")
A = pd.DataFrame(f.readlines())

# Find fill-scan block headers
inds = A.loc[A[0] == 'x1\ty1\tx2\ty2\n'].index

# Find contour block headers
contour_start_index = A.loc[A[0] == 'Type\tPoint Count\tx1, y1, x2, y2 ...\n'].index[0]
contour_section_front = 1
# Find start of fill-scan blocks
if not list(inds.values):
    scanBlockStart = A.loc[A[0] == 'Scan line blocks [0]\n'].index
    try:
        contour_end_index = scanBlockStart[0] - 2
    except IndexError:
        print '"Scan line blocks [0]" seems to be missing.'
        sys.exit()
else:
    contour_end_index = inds[0] - 6

# Grab all contours
allContours = [x[0] for x in A.loc[contour_start_index + contour_section_front:contour_end_index].values.tolist()]

# Parse entries and store

cx = []
cy = []
contourCount = 0
for s in allContours:
    sps = s.split("\t")
    if len(sps) > 1:
        # delete the last element if new line character
        if sps[-1] == '\n':
            del sps[-1]
        cxi = []
        cyi = []
        for i in range(2,len(sps)-1,2):
            cxi.append(float(sps[i  ]))
            cyi.append(float(sps[i+1]))
        cx.append(cxi)
        cy.append(cyi)
        contourCount += 1

totalLength = sum([len(j) for j in cx])

# Put all contours in 1D array
x = np.array([i for j in cx for i in j])
y = np.array([i for j in cy for i in j])

# Animate the contours
fig, ax = plt.subplots()

line, = ax.plot(x[0], y[0])
bordx = 0.01*(max(x) - min(x))
bordy = 0.01*(max(y) - min(y))
ax.set_xlim([min(x) - bordx,max(x) + bordx])
ax.set_ylim([min(y) - bordy,max(y) + bordy])
ax.set_title("Total number of points among the "
        + str(contourCount) + " contours: " + str(totalLength))

def animate(i):
    line.set_xdata(x[:i])  # update the data
    line.set_ydata(y[:i])  # update the data
    return line,


# Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, totalLength), init_func=init,
                              interval=25, blit=True)

if int(sys.argv[2]):
    ani.save(sys.argv[1] + "_contour.gif", writer="imagemagick", fps=20)

# Plot the contour points
fig = plt.figure()
for i in range(len(cx)):
    plt.scatter(cx[i], cy[i], s=2)

plt.show()

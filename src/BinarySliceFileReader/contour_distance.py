import sys
import numpy as np
import pandas as pd

if not len(sys.argv) == 2:
    print "Usage: python plot_contour_distance.py <name of summary file>"
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

L = np.array([], dtype="float64")
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
        x = np.array(cxi)
        y = np.array(cyi)

        # Calculate length of contour segments
        dx = x[1:] - x[:-1]
        dy = y[1:] - y[:-1]
        LC = np.sqrt(dx*dx + dy*dy)
        LC = np.append(LC, np.sqrt( (x[0]-x[-1]) * (x[0]-x[-1]) + (y[0]-y[-1]) * (y[0]-y[-1]) ))
        contourCount += 1
        L = np.append(L, LC)

print str(L.mean()) + "," + str(L.std()) + "," + str(L.max()) + "," + str(L.min()) + "," + str(np.median(L))
#print "Avg: " + str(L.mean()) + " Dev: " + str(L.std()) + " Max: " + str(L.max()) + " Min: " + str(L.min()) + " Med: " + str(np.median(L))

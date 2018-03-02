import sys
import pandas as pd

if not len(sys.argv) == 2:
    print "Usage: python count_scans_contours.py <name of summary file>"
    sys.exit()

f = open(sys.argv[1],"r")
A = pd.DataFrame(f.readlines())

# Find fill-scan block headers
inds = A.loc[A[0] == 'x1\ty1\tx2\ty2\n'].index

if not list(inds.values):
    numScanLines = 0
else:
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
    numScanLines = len(allScans)


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
numPartContours = 0
for s in allContours:
    sps = s.split("\t")
    if len(sps) > 1:
        numPartContours += int(sps[1])

print "Total Fill Scans: " + str(numScanLines) + " Total Contour Scans: " + str(numPartContours)

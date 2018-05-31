import statistics
from operator import itemgetter
import math

# Kat Young (kmy9ca)
# closestpair-kmy9ca.py
# python 2.7.10

############### GET INPUTS #####################
filename = 'garden.txt'

with open(filename, "r") as ins:
     coordinates = []
     xvalues = []

     for line in ins:
         line = line.split()
         line = [float(i) for i in line]
         xvalues.append(line[0])
         coordinates.append(line)
del coordinates[0]
del xvalues[0]
############# SORT LIST BY X ########################
coordinates = sorted(coordinates, key=itemgetter(0))



############## DISTANCE FUNCTION ###############
def distance(point1,point2):
    return math.sqrt(((point1[0] - point2[0])**2)+((point1[1]-point2[1])**2))


################## DIVIDE ##########################

def closestPair( list ):
    yOrdered = []
    ################### BASE CASES ###########################
    if len(list) == 1:
        theMin = math.inf
        yOrdered.append(list[0])
        return theMin, yOrdered
    if len(list) == 3:
        min1 = distance(list[0], list[1])
        min2 = distance(list[0], list[2])
        min3 = distance(list[2], list[1])
        theMin = min(min1,min2,min3)

        if list[0][1] < list[1][1] and list[0][1] < list[2][1]:
            yOrdered.append(list[0])
            if list[1][1] < list[2][1]:
                yOrdered.append(list[1])
                yOrdered.append(list[2])
            else:
                yOrdered.append(list[2])
                yOrdered.append(list[1])
        if list[1][1] < list[0][1] and list[1][1] < list[2][1]:
            yOrdered.append(list[1])
            if list[0][1] < list[2][1]:
                yOrdered.append(list[0])
                yOrdered.append(list[2])
            else:
                yOrdered.append(list[2])
                yOrdered.append(list[0])
        if list[2][1] < list[1][1] and list[2][1] < list[0][1]:
            yOrdered.append(list[2])
            if list[1][1] < list[0][1]:
                yOrdered.append(list[1])
                yOrdered.append(list[0])
            else:
                yOrdered.append(list[0])
                yOrdered.append(list[1])
        return theMin, yOrdered

    if len(list) == 2:
        min1 = distance(list[0], list[1])
        yOrdered = []
        if list[0][1] < list[1][1]:
            yOrdered.append(list[0])
            yOrdered.append(list[1])
        else:
            yOrdered.append(list[1])
            yOrdered.append(list[0])
        return min1, yOrdered


    if len(list) > 3:
        xArray = []                                         # to calculate median
        for item in list:
            xArray.append(item[0])                          # array of x values
        xmedian = float(statistics.median(xArray))          # calculate median
        leftlist = []                                       # DIVIDE
        rightlist = []
        equalMedian = []

        for i in range(0,len(list)):                    # separate to left/right
            if list[i][0] < xmedian:
                leftlist.append(list[i])
            if list[i][0] > xmedian:
                rightlist.append(list[i])
            if list[i][0] == xmedian:
                equalMedian.append(list[i])

        if len(equalMedian) != 0:
            count = 0
            for i in range(0, len(equalMedian)):
                if count % 2 == 0:
                    leftlist.append(equalMedian[i])
                if count % 2 == 1:
                    rightlist.append(equalMedian[i])
                count += 1

        leftmin, leftsorted = closestPair(leftlist)                          # RECURSIVE call on left
        rightmin, rightsorted = closestPair(rightlist)                        # RECURSIVE call on right
        delta = min(leftmin,rightmin)
        lbound = xmedian - delta
        rbound = xmedian + delta
        #call merge
        MergedList = merge(leftsorted,rightsorted)
        RunwayList = []
        for point in range(0,len(MergedList)):
            if lbound <= MergedList[point][0] <= rbound:
                RunwayList.append(MergedList[point])                    # List of runway points is created and filled

        #call combine
        runwayMin = combine(RunwayList)
        return min(runwayMin,delta), MergedList


def merge(left,right):
    newList = []
    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0][1] < right[0][1]:
                newList.append(left.pop(0))
            else:
                newList.append(right.pop(0))
        if len(left) == 0 and len(right) != 0:
            newList.append(right.pop(0))

        if len(right) == 0 and len(left) != 0:
            newList.append(left.pop(0))

    return newList



def combine(coordinates):
    runwayMin = math.inf
    while len(coordinates) > 15:
        for p in range(1,15):
            currDist = distance(coordinates[0], coordinates[p])
            runwayMin = min(runwayMin, currDist)
        del coordinates[0]

    while len(coordinates) < 16 and len(coordinates) > 1:
        for w in range(1,len(coordinates)):
            currDist = distance(coordinates[0], coordinates[w])
            runwayMin = min(runwayMin,currDist)
        del coordinates[0]
    return runwayMin


answer = closestPair(coordinates)
print(answer[0])

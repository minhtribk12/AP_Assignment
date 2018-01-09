#################################################################################
# Author: Minh-Tri Nguyen
# Email: nmtribk@hcmut.edu.vn
# Date: 08/01/2017
#################################################################################

import math
import csv
import numpy as np
from scipy.spatial import distance
from journey import Journey
from point import Point
import matplotlib.pyplot as plt

Topleft = Point(11.175186, 106.309795)
BottomRight = Point(10.368436, 107.036295)
Lat_d = Topleft.getLat() - BottomRight.getLat() # max distance in Y axis
Lng_d = BottomRight.getLng() - Topleft.getLng() # max distance in X axis
GridSize = (Lat_d/1000, Lng_d/1000) # Size of 1 cell
plt.axis([0, 1000, 0, 1000]) # create space to draw plot

def cell (lat, lng):
    x = (Topleft.getLat() - lat)/GridSize[0] # calculate index in X axis
    y = (lng - Topleft.getLng())/GridSize[1] # calculate index in Y axis
    return Point(math.ceil(x), math.ceil(y)) # Round result and return

def compareJourney_HD(journey_1, journey_2):
    distance_m = distance.cdist(journey_1.getNdarray(), journey_2.getNdarray()) # calculate distance matrix
    min_axis0 = distance_m.min(axis=0) # extract min distance from each point of route to journey
    meanDistance = min_axis0.mean() # calculate mean distance
    maxDistance = min_axis0.max() # calculate max distance
    return meanDistance,maxDistance

def compareJourney_DF(journey_1, journey_2):
    m = journey_1.size
    n = journey_2.size
    distance_m = np.empty((m, n))
    distance_m.fill(-1)
    distance_m[0,0] = np.linalg.norm(journey_1.array_[0]-journey_2.array_[0])
    for j in range (1, n):
        distance_m[0,j] = max(distance_m[0,j-1], np.linalg.norm(journey_1.array_[0]-journey_2.array_[j]))
    for i in range (1, m):
        distance_m[i,0] = max(distance_m[i-1,0], np.linalg.norm(journey_1.array_[i]-journey_2.array_[0]))
        for j in range (1, n):
            min_distance = min([distance_m[i-1,j-1], distance_m[i, j-1], distance_m[i-1,j]])
            distance_m[i,j] = max(min_distance, np.linalg.norm(journey_1.array_[i]-journey_2.array_[j]))
    return distance_m[m-1,n-1]

def compareJourney_VDF(journey_1, journey_2):
    m = journey_1.size
    n = journey_2.size
    distance_m = np.empty((m, n))
    distance_m.fill(-1)
    distance_m[0,0] = np.linalg.norm(journey_1.array_[0]-journey_2.array_[0])
    for j in range (1, n):
        distance_m[0,j] = distance_m[0,j-1] + np.linalg.norm(journey_1.array_[0]-journey_2.array_[j])
    for i in range (1, m):
        distance_m[i,0] = distance_m[i-1,0] + np.linalg.norm(journey_1.array_[i]-journey_2.array_[0])
        for j in range (1, n):
            min_distance = min([distance_m[i-1,j-1], distance_m[i, j-1], distance_m[i-1,j]])
            distance_m[i,j] = min_distance + np.linalg.norm(journey_1.array_[i]-journey_2.array_[j])
    return distance_m[m-1,n-1]


def readRoute(filename):
    route = Journey()
    with open(filename, 'rb') as f:
        reader = csv.reader(x.replace('\0', '') for x in f) # read file and remove null character
        for row in reader:
            x = float(row[5]) # convert Lat to float
            y = float(row[6]) # convert Long to float
            point = cell(x,y) # calculate cell
            if not point.equal(route.getLastPoint()): # remove if new point is the same with recent point
                route.addPoint(point)
            # extract point list from polyline
            polyLine = str(row[7]).replace("[","").replace("]","").replace(" ","").split(";") 
            for vertex in polyLine:
                if vertex is not None:
                    point = str(vertex).split(",")
                    if (len(point) == 2):
                        y = float(point[0])
                        x = float(point[1])
                        #check valid point
                        if ((x > BottomRight.getLat()) and (x < Topleft.getLat()) and (y < BottomRight.getLng()) and (y > Topleft.getLng())):
                            point = cell(x,y)
                            if not point.equal(route.getLastPoint()):
                                route.addPoint(point)
    route.finish()
    return route

def readJourney(filename):
    journey = Journey()
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            if ((x > BottomRight.getLat()) and (x < Topleft.getLat()) and (y < BottomRight.getLng()) and (y > Topleft.getLng())):
                point = cell(x,y)
                if not point.equal(journey.getLastPoint()):
                    journey.addPoint(point)
    journey.finish()
    return journey

def drawPlot(journey,option):
    a = journey.array_
    plt.plot(a[:,0], a[:,1], option)

def readData():
    journey_a = readJourney("../data_new/a.csv")
    journey_b = readJourney("../data_new/b.csv")
    route_1 = readRoute("../data_new/r1.csv")
    route_2 = readRoute("../data_new/r2.csv")
    route_3 = readRoute("../data_new/r3.csv")
    route_4 = readRoute("../data_new/r4.csv")
    route_5 = readRoute("../data_new/r5.csv")
    route_6 = readRoute("../data_new/r6.csv")
    route_7 = readRoute("../data_new/r7.csv")
    route_8 = readRoute("../data_new/r8.csv")
    route_9 = readRoute("../data_new/r9.csv")
    route_10 = readRoute("../data_new/r10.csv")
    route_11 = readRoute("../data_new/r11.csv")
    route_12 = readRoute("../data_new/r12.csv")
    route_13 = readRoute("../data_new/r13.csv")
    route_14 = readRoute("../data_new/r14.csv")
    route_15 = readRoute("../data_new/r15.csv")

def Hausdorff_distance():
    result1 = compareJourney_HD(journey_a,route_1)
    print result1
    result2 = compareJourney_HD(journey_a,route_2)
    print result2
    result3 = compareJourney_HD(journey_a,route_3)
    print result3
    result4 = compareJourney_HD(journey_a,route_4)
    print result4
    result5 = compareJourney_HD(journey_a,route_5)
    print result5
    result6 = compareJourney_HD(journey_a,route_6)
    print result6
    result7 = compareJourney_HD(journey_a,route_7)
    print result7
    result8 = compareJourney_HD(journey_a,route_8)
    print result8
    result9 = compareJourney_HD(journey_a,route_9)
    print result9
    result10 = compareJourney_HD(journey_a,route_10)
    print result10
    result11 = compareJourney_HD(journey_a,route_11)
    print result11
    result12 = compareJourney_HD(journey_a,route_12)
    print result12
    result13 = compareJourney_HD(journey_a,route_13)
    print result13
    result14 = compareJourney_HD(journey_a,route_14)
    print result14
    result15 = compareJourney_HD(journey_a,route_15)
    print result15

def drawResult():
    drawPlot(journey_a, "ro")
    drawPlot(journey_b, "bo")
    drawPlot(route_1, "yo")
    plt.show()

def main():
    journey_a = readJourney("../data_new/a.csv")
    route_1 = readRoute("../data_new/r1.csv")
    print compareJourney_DF(journey_a, route_1)
    print compareJourney_VDF(journey_a, route_1)
    

if __name__ == '__main__':
    main()
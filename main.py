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
Lat_d = Topleft.getLat() - BottomRight.getLat()
Lng_d = BottomRight.getLng() - Topleft.getLng()
GridSize = (Lat_d/1000, Lng_d/1000)
plt.axis([0, 1000, 0, 1000])

def cell (lat, lng):
    x = (Topleft.getLat() - lat)/GridSize[0]
    y = (lng - Topleft.getLng())/GridSize[1]
    return Point(math.ceil(x), math.ceil(y))

def compareJourney(journey_1, journey_2):
    distance_m = distance.cdist(journey_1.getNdarray(), journey_2.getNdarray())
    min_axis0 = distance_m.min(axis=0)
    meanDistance = min_axis0.mean()
    maxDistance = min_axis0.max()
    return meanDistance,maxDistance

def readRoute(filename):
    route = Journey()
    with open(filename, 'rb') as f:
        reader = csv.reader(x.replace('\0', '') for x in f)
        for row in reader:
            x = float(row[5])
            y = float(row[6])
            point = cell(x,y)
            if not point.equal(route.getLastPoint()):
                route.addPoint(point)
            polyLine = str(row[7]).replace("[","").replace("]","").replace(" ","").split(";")
            for vertex in polyLine:
                if vertex is not None:
                    point = str(vertex).split(",")
                    if (len(point) == 2):
                        y = float(point[0])
                        x = float(point[1])
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

def main():
    journey_a = readJourney("a.csv")
    journey_b = readJourney("b.csv")
    route_1 = readRoute("r1.csv")
    route_2 = readRoute("r2.csv")
    route_3 = readRoute("r3.csv")
    route_4 = readRoute("r4.csv")
    route_5 = readRoute("r5.csv")
    route_6 = readRoute("r6.csv")
    route_7 = readRoute("r7.csv")
    route_8 = readRoute("r8.csv")
    route_9 = readRoute("r9.csv")
    route_10 = readRoute("r10.csv")
    route_11 = readRoute("r11.csv")
    route_12 = readRoute("r12.csv")
    route_13 = readRoute("r13.csv")
    route_14 = readRoute("r14.csv")
    route_15 = readRoute("r15.csv")
    
 
    #################################################################################
    result1 = compareJourney(journey_a,route_1)
    print result1
    drawPlot(journey_a, "ro")
    drawPlot(journey_b, "bo")
    drawPlot(route_1, "yo")
    plt.show()
    result2 = compareJourney(journey_a,route_2)
    print result2
    result3 = compareJourney(journey_a,route_3)
    print result3
    result4 = compareJourney(journey_a,route_4)
    print result4
    result5 = compareJourney(journey_a,route_5)
    print result5
    result6 = compareJourney(journey_a,route_6)
    print result6
    result7 = compareJourney(journey_a,route_7)
    print result7
    result8 = compareJourney(journey_a,route_8)
    print result8
    result9 = compareJourney(journey_a,route_9)
    print result9
    result10 = compareJourney(journey_a,route_10)
    print result10
    result11 = compareJourney(journey_a,route_11)
    print result11
    result12 = compareJourney(journey_a,route_12)
    print result12
    result13 = compareJourney(journey_a,route_13)
    print result13
    result14 = compareJourney(journey_a,route_14)
    print result14
    result15 = compareJourney(journey_a,route_15)
    print result15

if __name__ == '__main__':
    main()
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
list_route = []

def cell (lat, lng):
    x = (Topleft.getLat() - lat)/GridSize[0] # calculate index in X axis
    y = (lng - Topleft.getLng())/GridSize[1] # calculate index in Y axis
    return Point(math.ceil(x), math.ceil(y)) # Round result and return

def checkvalidpoint(x,y):
    if ((x > BottomRight.getLat()) and (x < Topleft.getLat()) and (y < BottomRight.getLng()) and (y > Topleft.getLng())):
        return True
    else:
        return False


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
            x = 0.0
            y = 0.0
            try:
                y = float(row[5])
                x = float(row[6])
            except ValueError:
                #print row[5] + " , " + row[6] + "error"
                continue
            #check valid point
            if (checkvalidpoint(x,y)):
                point = cell(x,y)
                if not point.equal(route.getLastPoint()):
                    route.addPoint(point)
            # extract point list from polyline
            polyLine = str(row[7]).replace("[","").replace("]","").replace(" ","").split(";") 
            for vertex in polyLine:
                if vertex is not None:
                    point = str(vertex).split(",")
                    if (len(point) == 2):
                        x = 0.0
                        y = 0.0
                        try:
                            y = float(point[0])
                            x = float(point[1])
                        except ValueError:
                            #print point[0] + " , " + point[1] + "error"
                            continue
                        #check valid point
                        if (checkvalidpoint(x,y)):
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
            x = 0.0
            y = 0.0
            try:
                x = float(row[0])
                y = float(row[1])
            except ValueError:
                #print "value error"
                continue
            if (checkvalidpoint(x,y)):
                point = cell(x,y)
                if not point.equal(journey.getLastPoint()):
                    journey.addPoint(point)
    journey.finish()
    return journey

def drawPlot(journey,option):
    a = journey.array_
    plt.plot(a[:,0], a[:,1], option)

def readData():
    list_route.append([1, readRoute("../data_new/1.csv")])
    list_route.append([2, readRoute("../data_new/2.csv")])
    list_route.append([3, readRoute("../data_new/3.csv")])
    list_route.append([4, readRoute("../data_new/4.csv")])
    list_route.append([5, readRoute("../data_new/5.csv")])
    list_route.append([6, readRoute("../data_new/6.csv")])
    list_route.append([7, readRoute("../data_new/7.csv")])
    list_route.append([8, readRoute("../data_new/8.csv")])
    list_route.append([9, readRoute("../data_new/9.csv")])
    list_route.append([10, readRoute("../data_new/10.csv")])
    list_route.append([11, readRoute("../data_new/11.csv")])
    list_route.append([12, readRoute("../data_new/12.csv")])
    list_route.append([13, readRoute("../data_new/13.csv")])
    list_route.append([14, readRoute("../data_new/14.csv")])
    list_route.append([15, readRoute("../data_new/15.csv")])
    list_route.append([16, readRoute("../data_new/16.csv")])
    list_route.append([17, readRoute("../data_new/17.csv")])
    list_route.append([18, readRoute("../data_new/18.csv")])
    list_route.append([19, readRoute("../data_new/19.csv")])
    list_route.append([20, readRoute("../data_new/20.csv")])
    list_route.append([22, readRoute("../data_new/22.csv")])
    list_route.append([23, readRoute("../data_new/23.csv")])
    list_route.append([24, readRoute("../data_new/24.csv")])
    list_route.append([25, readRoute("../data_new/25.csv")])
    list_route.append([27, readRoute("../data_new/27.csv")])
    list_route.append([28, readRoute("../data_new/28.csv")])
    list_route.append([29, readRoute("../data_new/29.csv")])
    list_route.append([30, readRoute("../data_new/30.csv")])
    list_route.append([31, readRoute("../data_new/31.csv")])
    list_route.append([32, readRoute("../data_new/32.csv")])
    list_route.append([33, readRoute("../data_new/33.csv")])
    list_route.append([34, readRoute("../data_new/34.csv")])
    list_route.append([35, readRoute("../data_new/35.csv")])
    list_route.append([36, readRoute("../data_new/36.csv")])
    list_route.append([37, readRoute("../data_new/37.csv")])
    list_route.append([38, readRoute("../data_new/38.csv")])
    list_route.append([39, readRoute("../data_new/39.csv")])
    list_route.append([40, readRoute("../data_new/40.csv")])
    list_route.append([41, readRoute("../data_new/41.csv")])
    list_route.append([42, readRoute("../data_new/42.csv")])
    list_route.append([43, readRoute("../data_new/43.csv")])
    list_route.append([44, readRoute("../data_new/44.csv")])
    list_route.append([45, readRoute("../data_new/45.csv")])
    list_route.append([46, readRoute("../data_new/46.csv")])
    list_route.append([47, readRoute("../data_new/47.csv")])
    list_route.append([48, readRoute("../data_new/48.csv")])
    list_route.append([50, readRoute("../data_new/50.csv")])
    list_route.append([51, readRoute("../data_new/51.csv")])
    list_route.append([52, readRoute("../data_new/52.csv")])
    list_route.append([53, readRoute("../data_new/53.csv")])
    list_route.append([54, readRoute("../data_new/54.csv")])
    list_route.append([55, readRoute("../data_new/55.csv")])
    list_route.append([56, readRoute("../data_new/56.csv")])
    list_route.append([57, readRoute("../data_new/57.csv")])
    list_route.append([58, readRoute("../data_new/58.csv")])
    list_route.append([59, readRoute("../data_new/59.csv")])
    list_route.append([60, readRoute("../data_new/60.csv")])
    list_route.append([61, readRoute("../data_new/61.csv")])
    list_route.append([62, readRoute("../data_new/62.csv")])
    list_route.append([64, readRoute("../data_new/64.csv")])
    list_route.append([65, readRoute("../data_new/65.csv")])
    list_route.append([66, readRoute("../data_new/66.csv")])
    list_route.append([68, readRoute("../data_new/68.csv")])
    list_route.append([69, readRoute("../data_new/69.csv")])
    list_route.append([70, readRoute("../data_new/70.csv")])
    list_route.append([71, readRoute("../data_new/71.csv")])
    list_route.append([72, readRoute("../data_new/72.csv")])
    list_route.append([73, readRoute("../data_new/73.csv")])
    list_route.append([74, readRoute("../data_new/74.csv")])
    list_route.append([76, readRoute("../data_new/76.csv")])
    list_route.append([78, readRoute("../data_new/78.csv")])
    list_route.append([79, readRoute("../data_new/79.csv")])
    list_route.append([81, readRoute("../data_new/81.csv")])
    list_route.append([83, readRoute("../data_new/83.csv")])
    list_route.append([84, readRoute("../data_new/84.csv")])
    list_route.append([85, readRoute("../data_new/85.csv")])
    list_route.append([86, readRoute("../data_new/86.csv")])
    list_route.append([87, readRoute("../data_new/87.csv")])
    list_route.append([88, readRoute("../data_new/88.csv")])
    list_route.append([89, readRoute("../data_new/89.csv")])
    list_route.append([90, readRoute("../data_new/90.csv")])
    list_route.append([91, readRoute("../data_new/91.csv")])
    list_route.append([93, readRoute("../data_new/93.csv")])
    list_route.append([94, readRoute("../data_new/94.csv")])
    list_route.append([95, readRoute("../data_new/95.csv")])
    list_route.append([96, readRoute("../data_new/96.csv")])
    list_route.append([99, readRoute("../data_new/99.csv")])
    list_route.append([100, readRoute("../data_new/100.csv")])
    list_route.append([101, readRoute("../data_new/101.csv")])
    list_route.append([102, readRoute("../data_new/102.csv")])
    list_route.append([103, readRoute("../data_new/103.csv")])
    list_route.append([104, readRoute("../data_new/104.csv")])
    list_route.append([107, readRoute("../data_new/107.csv")])
    list_route.append([110, readRoute("../data_new/110.csv")])
    list_route.append([122, readRoute("../data_new/122.csv")])
    list_route.append([126, readRoute("../data_new/126.csv")])
    list_route.append([127, readRoute("../data_new/127.csv")])
    list_route.append([128, readRoute("../data_new/128.csv")])
    list_route.append([139, readRoute("../data_new/139.csv")])
    list_route.append([140, readRoute("../data_new/140.csv")])
    list_route.append([141, readRoute("../data_new/141.csv")])
    list_route.append([144, readRoute("../data_new/144.csv")])
    list_route.append([145, readRoute("../data_new/145.csv")])
    list_route.append([146, readRoute("../data_new/146.csv")])
    list_route.append([148, readRoute("../data_new/148.csv")])
    list_route.append([149, readRoute("../data_new/149.csv")])
    list_route.append([150, readRoute("../data_new/150.csv")])
    list_route.append([151, readRoute("../data_new/151.csv")])
    list_route.append([152, readRoute("../data_new/152.csv")])
    list_route.append([153, readRoute("../data_new/153.csv")])
    

def Hausdorff_distance(journey):
    for route in list_route:
        result = compareJourney_HD(journey, route[1])
        print str(route[0]) + ": " + str(result)

def Frechet_distance(journey):
    for route in list_route:
        result = compareJourney_DF(journey, route[1])
        print str(route[0]) + ": " + str(result)

def Frechet_distance2(journey):
    for route in list_route:
        result = compareJourney_VDF(journey, route[1])
        print str(route[0]) + ": " + str(result)

def drawResult(journey, index):
    drawPlot(journey, "ro")
    for route in list_route:
        if (route[0] == index):
            drawPlot(route[1], "bo")
    plt.show()

def main():
    journey_a = readJourney("../data_new/a.csv")
    journey_b = readJourney("../data_new/b.csv")
    readData()
    Hausdorff_distance(journey_b)
    #Frechet_distance(journey_a)
    #drawResult(journey_a, 24)
    

if __name__ == '__main__':
    main()
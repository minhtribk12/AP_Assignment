#################################################################################
# Author: Minh-Tri Nguyen
# Email: nmtribk@hcmut.edu.vn
# Date: 08/01/2017
#################################################################################

import numpy as np
from point import Point


class Journey:
    def __init__(self):
        self.journey = []
        self.size = 0
        self.list = []
        self.listexisted = False
        self.arrayexisted = False
        self.array_ = None
    def addPoint(self, point):
        self.journey.append(point)
        self.size += 1
    def printJourney(self):
        for point in self.journey:
            print (str(point.getLat()) + "," + str(point.getLng()) + "\n")
    def getLastPoint(self):
        if(self.size == 0):
            return Point(0,0)
        return self.journey[self.size-1]
    def getNdarray(self):
        if self.arrayexisted:
            return self.array_
        else:
            self.array_ = np.array(self.getListPoint())
            self.arrayexisted = True
            return self.array_
    def getListPoint(self):
        if self.listexisted:
            return self.list
        else:
            self.list = []
            for point in self.journey:
                self.list.append([point.getLat(),point.getLng()])
            self.listexisted = True
            return self.list
    def finish(self):
        self.array_ = np.array(self.getListPoint())
        self.arrayexisted = True


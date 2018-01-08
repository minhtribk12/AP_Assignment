#################################################################################
# Author: Minh-Tri Nguyen
# Email: nmtribk@hcmut.edu.vn
# Date: 08/01/2017
#################################################################################

class Point:
    def __init__ (self, lat, lng):
        self.lat = lat
        self.lng = lng
    def getLat(self):
        return self.lat
    def getLng(self):
        return self.lng
    def setLat(self, lat):
        self.lat = lat
    def setLng(self, lng):
        self.lng = lng
    def equal(self, other):
        if ((self.lat == other.lat) and (self.lng == self.lng)):
            return True
        else: 
            return False
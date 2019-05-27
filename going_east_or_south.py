from pygeodesy.ellipsoidalVincenty import LatLon

BEARING_SOUTH = 180.0
BEARING_EAST = 90.0

POINT = LatLon(-37.711874, 144.966859)

DISTANCE_METERS = 10000.0

east = POINT.destination(DISTANCE_METERS, BEARING_EAST)
south = POINT.destination(DISTANCE_METERS, BEARING_SOUTH)

print ("Origin " + str(POINT))
print ("East   " + str(east))
print ("South  " + str(south))

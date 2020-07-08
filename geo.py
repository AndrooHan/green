import geopandas as gpd
from shapely.geometry import Polygon, Point
import math
# from haversine import haversine, Unit

def test():
	states = gpd.read_file('us-states.json')
	cali_multi_poly = states.loc[states['NAME'] == 'California'].geometry
	return cali_multi_poly
	# states.show()
	# print(states.head())

	# p1 = Point(36.527295,-120.418203)
	# cali_multi_poly = states.loc[states['NAME'] == 'California'].geometry
	# print("Cali")
	# print(type(cali_multi_poly))
	# print(cali_multi_poly)
	# contain = cali_multi_poly.intersects(p1)
	# print("Contains")
	# print(contain)
	# return states
# def within_point(x_1, y_1, x_2, y_2, distance):

# 	# create your two points
# 	point_1 = Point(x_1, y_1)
# 	point_2 = Point(x_2, y_2)

# 	# create your circle buffer from one of the points
# 	distance = 1000
# 	circle_buffer = point_1.buffer(distance)
# 	return point_1.distance(point_2) < distance:

def find_circle(centerLat, centerLon, radius):
	N = 10 # number of discrete sample points to be generated along the circle

	# generate points
	circlePoints = []
	for k in range(N):
	    # compute
	    angle = math.pi*2*k/N
	    dx = radius*math.cos(angle)
	    dy = radius*math.sin(angle)
	    point = {}
	    point['lat']= float(centerLat) + (180/math.pi)*(dy/6378137)
	    point['lon']= float(centerLon) + (180/math.pi)*(dx/6378137)/math.cos(float(centerLat)*math.pi/180)
	    # add to list
	    circlePoints.append((point['lat'], point['lon']))

	print(circlePoints)

	return Polygon(circlePoints)

def inside_polygon(polygon, latitude, longitude):
	p = Point(latitude, longitude)
	return polygon.contains(p)


# 1 degree of Longitude = cosine (latitude) * (miles)

def degreesToRadians(degrees):
  return degrees * math.pi / 180;


def create_circle(radius, points, latitude, longitude):
	# Degrees to radians 
	d2r = math.pi / 180
	# Radians to degrees
	r2d = 180 / math.pi
	#Earth radius is 3,963 miles
	cLat = (radius / 3963) * r2d
	cLng = cLat / math.cos(latitude * d2r)
	print("cLat "+str(cLat)+" cLng "+str(cLng))
	# generate points
	circlePoints = []
	for i in range(1, points+1):
		theta = math.pi * (i/1)
		print("theta: "+str(theta))
		circleY = longitude + (cLng * math.cos(theta))
		circleX = latitude + (cLat * math.sin(theta))
		circlePoints.append((circleX, circleY))
	return circlePoints

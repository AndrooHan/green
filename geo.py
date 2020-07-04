import geopandas as gpd
from shapely.geometry import Polygon, Point
import math

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
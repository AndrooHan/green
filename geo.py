from shapely.geometry import Polygon, Point
import math
from haversine import haversine, Unit


def distance_between(lat1, lon1, lat2, lon2):
	return haversine((float(lat1), float(lon1)), (float(lat2), float(lon2)), unit=Unit.MILES)

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

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
	p = Point(longitude, latitude)
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


def validate_lat_long_radius(latitude, longitude, radius):
    latvalid = latitude > -90 and latitude < 90
    longvalid = longitude > -180 and longitude < 180
    radiusvalid = radius > 0
    print('{} {} {}'.format(latitude, longitude, radiusvalid))
    return latvalid and longvalid and radiusvalid



def within_radius(feed_post, latitude, longitude, radius):
    return distance_between(latitude, longitude, feed_post['latitude'], feed_post['longitude']) <= radius

def within_geofence(feed_post, geofence):
    if geofence['gemoetry']['type'] == 'Polygon':
        for coordinate in geofence['geometry']['coordinates']:
            poly = Polygon(coordinate)
            return geo.inside_polygon(poly, feed_post['latitude'], feed_post['longitude'])
    else:
        print('Geofence {} not type poygon'.format(geofence['id']))
    return False

from redis_helper import Redis
import geo
import json
from collections import defaultdict 
from shapely.geometry import Polygon
import radar

def get_feed_posts_within(latitude, longitude, radius):
    print("finding posts within")
    print("latitude: " +  str(latitude))
    print("longitude: " +  str(longitude))
    print("radius: " + str(radius))
    user_circle = geo.find_circle(latitude, longitude, radius)
    filtered_posts = [post for post in get_feed_posts() if geo.inside_polygon(user_circle, post['latitude'], post['longitude'])]
    filtered_posts.sort(reverse=True, key=sortPostsFunc)
    return filtered_posts

def get_feed_posts_close_to(latitude, longitude, radius):
    print("finding posts close to")
    print("latitude: " +  str(latitude))
    print("longitude: " +  str(longitude))
    print("radius: " + str(radius)) # should be in miles
    filtered_posts = [post for post in get_feed_posts() if geo.distance_between(latitude, longitude, post['latitude'], post['longitude']) <= radius]
    filtered_posts.sort(reverse=True, key=sortPostsFunc)
    return filtered_posts

def get_feed_posts():
    keys = Redis.get().keys()
    vals = Redis.get().mget(keys)
    json_vals = [json.loads(v) for v in vals]
    feed_posts = [item for item in json_vals if item['type'] == 'post']
    feed_posts.sort(reverse=True, key=sortPostsFunc)
    return feed_posts

def sortPostsFunc(post):
  return post['created_at']


# latitude, longitude, radius
def get_all_posts(latitude, longitude, radius):
    posts = defaultdict(list)
    nearby_geofences = radar.search_nearby_geofences(latitude, longitude)
    print('nearby_fences of {},{} : {}'.format(latitude, longitude, nearby_geofences))
    for post in get_feed_posts():
        #Radius
        if geo.distance_between(latitude, longitude, post['latitude'], post['longitude'] <= radius ):
            posts['radius'].append(post)

        #Geofences
        for geofence in nearby_geofences:
            for coordinate in geofence.geometry.coordinates:
                print('coordinate: {}'.format(str(coordinate)))
                polygon = Polygon(coordinate)
                if geo.inside_polygon(polygon, latitude, longitude):
                    posts[geofence.id].append(post)
                else:
                    print("{} {} not in {}".format(latitude, longitude, geofence.id))

    return posts




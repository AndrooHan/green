from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import render_template
import random
import string
import geo
import radar
import uuid
import io
import base64
import redis_helper
import feed
import users
import time
from shapely.geometry import Polygon, Point


app = Flask(__name__)

@app.route("/test")
def test():
    return [ob.to_json() for ob in radar.list_all_geofences()][0]


#/api/status?latitude=34.2323&longitude=-232.99222&radius=10
@app.route("/api/status", methods=["GET"])
def status():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    radius = request.args.get('radius')
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)
    except:
        return Response("{'error':'cant convert input'}", status=400, mimetype='application/json')

    if not geo.validate_lat_long_radius(latitude, longitude, radius):
        return Response("{'error':'invalid latitude or longitude'}", status=400, mimetype='application/json')

    # returns a dict of lists per geofence
    posts = feed.get_all_posts(latitude, longitude, radius)

    return jsonify(posts)

@app.route('/feed')
def get_all_feed():
    return jsonify(feed.get_feed_posts())

@app.route('/user', methods=['POST'])
def add_user():
    content = request.json
    user_id = content['id']
    username = content['username']
    provider_uid = content['provider_uid']
    redis_helper.add_user_redis(user_id, username, provider_uid)
    return "Okay"

@app.route('/users')
def get_user():
    return jsonify(users.get_users())


#/api/status?latitude=34.2323&longitude=-232.99222&radius=10
@app.route('/api/feed')
def get_specific_feed():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    return jsonify(feed.get_feed_posts_close_to(float(latitude), float(longitude), 100))

@app.route('/add', methods=['POST'])
def add_message():
    content = request.json
    latitude = content['latitude']
    longitude = content['longitude']

    print("latitude: " + str(latitude))
    print("longitude: " + str(longitude))
    post = {
        "id": content['id'],
        "username": content['username'],
        "text": content['text'],
        "created_at": int(time.time()),
        "latitude": latitude,
        "longitude": longitude,
        "likes": [],
        "type": "post",
    }
    if not r.exists(post['id']):
        redis_helper.add_or_update_redis(post)
    
    return jsonify(feed.get_feed_posts_close_to(latitude, longitude, 100))

@app.route('/like', methods=['POST'])
def like_message():
    post_id = request.json['post_id']
    user_id = request.json['user_id']

    post_json = get_redis_post(post_id)
    if user_id not in post_json['likes']:
            post_json['likes'].append(user_id)
    
    print("new post likes: " + str(post_json))
    redis_helper.add_or_update_redis(post_json)
    
    return jsonify(feed.get_feed_posts_close_to(post_json['latitude'], post_json['longitude'], 100))
    
def within_geofence(feed_post, geofence):
    if geofence['gemoetry']['type'] == 'Polygon':
        for coordinate in geofence['geometry']['coordinates']:
            poly = Polygon(coordinate)
            return geo.inside_polygon(poly, feed_post['latitude'], feed_post['longitude'])
    else:
        print('Geofence {} not type poygon'.format(geofence['id']))
    return False

redis_helper.seed_redis()





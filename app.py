from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import json
import time
import random
import string
import geo
import uuid
import redis
import os
import fakeredis
import socket



app = Flask(__name__)
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

r = fakeredis.FakeStrictRedis() if str(ip_address) == "127.0.0.1" else redis.from_url(os.environ.get("REDIS_URL"))

@app.route('/test')
def random_test():
    gs = geo.test()

    # return render_template('simple.html',  tables=[gs.to_html(classes='data')], titles=gs.columns.values)
    return "looool"
    # gs.savefig('img/plot.png')
    # return render_template('plot.html', url='/img/plot.png')
    # return "cool"

@app.route('/feed')
def get_all_feed():
    return jsonify(get_feed_posts())


#/api/feed?latitude=34.2323&longitude=-232.99222
@app.route('/api/feed')
def get_specific_feed():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return jsonify(get_feed_posts_within(float(latitude), float(longitude), 100))

@app.route('/add', methods=['POST'])
def add_message():
    content = request.json
    latitude = content['latitude']
    longitude = content['longitude']

    print("latitude: " + str(latitude))
    print("longitude: " + str(longitude))
    post = {
        "username": content['username'],
        "text": content['text'],
        "created_at": int(time.time()),
        "latitude": latitude,
        "longitude": longitude,
        "likes": 0,
    }
    add_to_redis(post)
    
    return jsonify(get_feed_posts_within(latitude, longitude, 100))

# @app.route('/add-test')
# def add_message_test():
#     global feed_posts
#     feed_posts.append(
#         {
#             "username": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
#             "text": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(200)),
#             "created_at": int(time.time()),
#         }
#     )
#     return jsonify([post for post in get_feed_posts()])

def myFunc(post):
  return post['created_at']

# def get_feed_posts_within2(latitude, longitude, radius):
#     print("finding posts within using new func")
#     print("latitude: " +  str(latitude))
#     print("longitude: " +  str(longitude))
#     print("radius: " + str(radius))
#     filtered_posts = [post for post in get_feed_posts() if geo.within_point(circle, latitude, 1)]
#     filtered_posts.sort(reverse=True, key=myFunc)

def get_feed_posts_within(latitude, longitude, radius):
    print("finding posts within")
    print("latitude: " +  str(latitude))
    print("longitude: " +  str(longitude))
    print("radius: " + str(radius))
    user_circle = geo.find_circle(latitude, longitude, radius)
    filtered_posts = [post for post in get_feed_posts() if geo.inside_polygon(user_circle, post['latitude'], post['longitude'])]
    filtered_posts.sort(reverse=True, key=myFunc)
    return filtered_posts

def get_feed_posts():
    keys = r.keys()
    vals = r.mget(keys)
    feed_posts = [json.loads(v) for v in vals]
    feed_posts.sort(reverse=True, key=myFunc)
    return feed_posts


# Redis functions ===============================
def seed_redis():
    r.flushdb()
    feed_posts = [
        {
            "username": "user_a",
            "text": "first post!",
            "created_at": int(time.time()),
            "latitude": 37.2310016,
            "longitude": -121.7691648,
            "likes": 28,
        },
        {
            "username": "user_b",
            "text": "So Im currently an 18 year old boy whos been pro life for about as long as Ive known abortion existed. I just graduated high school a few weeks ago and this is pretty much just a rant about the hive mind of my now former school. Being pro life in my generation is something that gets looked down on, and peoples reaction to someone saying theyre pro life is about equal to if you tell them you kill puppies for fun. Thats the level of shock and disgust people my age have for someone being pro life. Rational conversations dont exist since holding that opinion makes you a misogynistic prick not worth their time. Anytime abortion is brought up they make the same few points and these points themselves prove they have zero knowledge of the science behind it. The points are",
            "created_at": int(time.time())+10,
            "latitude": 37.2310016,
            "longitude": -121.7691648,
            "likes": 6,
        },
        {
            "username": "user_c",
            "text": "hello everyone",
            "created_at": int(time.time())+20,
            "latitude": 37.2310016,
            "longitude": -121.7691648,
            "likes": 12,
        },
    ]
    for post in feed_posts:  
        json_post = json.dumps(post)
        r.set(str(uuid.uuid4()), json_post)

def add_to_redis(post):
    json_post = json.dumps(post)
    r.set(str(uuid.uuid4()), json_post)



seed_redis()





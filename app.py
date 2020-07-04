from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import json
import time
import random
import string
import geo


app = Flask(__name__)

feed_posts = [
    {
        "username": "user_a",
        "text": "first post!",
        "created_at": int(time.time()),
        "latitude": 37.2310016,
        "longitude": -121.7691648,
    },
    {
        "username": "user_b",
        "text": "So Im currently an 18 year old boy whos been pro life for about as long as Ive known abortion existed. I just graduated high school a few weeks ago and this is pretty much just a rant about the hive mind of my now former school. Being pro life in my generation is something that gets looked down on, and peoples reaction to someone saying theyre pro life is about equal to if you tell them you kill puppies for fun. Thats the level of shock and disgust people my age have for someone being pro life. Rational conversations dont exist since holding that opinion makes you a misogynistic prick not worth their time. Anytime abortion is brought up they make the same few points and these points themselves prove they have zero knowledge of the science behind it. The points are",
        "created_at": int(time.time())+10,
        "latitude": 37.2310016,
        "longitude": -121.7691648,
    },
    {
        "username": "user_c",
        "text": "hello everyone",
        "created_at": int(time.time())+20,
        "latitude": 37.2310016,
        "longitude": -121.7691648,
    },
]

@app.route('/test')
def random_test():
    gs = geo.test()

    # return render_template('simple.html',  tables=[gs.to_html(classes='data')], titles=gs.columns.values)
    return "looool"
    # gs.savefig('img/plot.png')
    # return render_template('plot.html', url='/img/plot.png')
    # return "cool"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/feed')
def get_all_feed():
    return jsonify([post for post in get_feed_posts()])


#/api/feed?latitude=34.2323&longitude=-232.99222
@app.route('/api/feed')
def get_specific_feed():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    print("latitude: " + latitude)
    print("longitude: " + longitude)
    circle = geo.find_circle(latitude, longitude, 100000)

    # find posts within the circle
    return jsonify([post for post in get_feed_posts() if geo.inside_polygon(circle, post['latitude'], post['longitude'])])

@app.route('/add', methods=['POST'])
def add_message():
    global feed_posts
    content = request.json
    latitude = content['latitude']
    longitude = content['longitude']
    print("latitude: " + str(latitude))
    print("longitude: " + str(longitude))
    feed_posts.append(
        {
            "username": content['username'],
            "text": content['text'],
            "created_at": int(time.time()),
            "latitude": latitude,
            "longitude": longitude,
        }
    )
    circle = geo.find_circle(content['latitude'], content['longitude'], 100000)
    return jsonify([post for post in get_feed_posts() if geo.inside_polygon(circle, post['latitude'], post['longitude'])])

@app.route('/add-test')
def add_message_test():
    global feed_posts
    feed_posts.append(
        {
            "username": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
            "text": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(200)),
            "created_at": int(time.time()),
        }
    )
    return jsonify([post for post in get_feed_posts()])

def myFunc(post):
  return post['created_at']


def get_feed_posts():
    global feed_posts
    feed_posts.sort(reverse=True, key=myFunc)
    return feed_posts




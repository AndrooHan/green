from flask import Flask
from flask import jsonify
from flask import request
import json
import time
import random
import string


app = Flask(__name__)

feed_posts = [
    {
        "username": "user_a",
        "text": "first post!",
        "created_at": int(time.time()),
    },
    {
        "username": "user_b",
        "text": "So Im currently an 18 year old boy whos been pro life for about as long as Ive known abortion existed. I just graduated high school a few weeks ago and this is pretty much just a rant about the hive mind of my now former school. Being pro life in my generation is something that gets looked down on, and peoples reaction to someone saying theyre pro life is about equal to if you tell them you kill puppies for fun. Thats the level of shock and disgust people my age have for someone being pro life. Rational conversations dont exist since holding that opinion makes you a misogynistic prick not worth their time. Anytime abortion is brought up they make the same few points and these points themselves prove they have zero knowledge of the science behind it. The points are",
        "created_at": int(time.time())+10,
    },
    {
        "username": "user_c",
        "text": "hello everyone",
        "created_at": int(time.time())+20,
    },
]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/feed')
def get_all_feed():
    global feed_posts
    return jsonify([post for post in get_feed_posts()])

@app.route('/add', methods=['POST'])
def add_message():
    global feed_posts
    content = request.json
    feed_posts.append(
        {
            "username": content['username'],
            "text": content['text'],
            "created_at": int(time.time()),
        }
    )
    return jsonify([post for post in get_feed_posts()])

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




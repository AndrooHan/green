from flask import Flask
from flask import jsonify
import json
import time


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/feed')
def get_all_feed():
    feed_posts = [
        {
            "username": "user_a",
            "text": "first post!",
            "created_at": int(time.time()),
        },
        {
            "username": "user_b",
            "text": "whats poppin?",
            "created_at": int(time.time())+10,
        },
        {
            "username": "user_a",
            "text": "hello everyone",
            "created_at": int(time.time())+20,
        },
    ]
    return jsonify([post for post in feed_posts])

@app.route('/feed/<int:region_id>')
def get_feed(region_id):
    feed_posts = [
        {
            "username": "user_a",
            "text": "first post!",
            "created_at": int(time.time()),
        },
        {
            "username": "user_b",
            "text": "whats poppin?",
            "created_at": int(time.time())+10,
        },
        {
            "username": "user_a",
            "text": "hello everyone",
            "created_at": int(time.time())+20,
        },
    ]
    return jsonify([post for post in feed_posts])
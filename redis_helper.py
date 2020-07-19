import fakeredis
import socket
import time
import json

class Redis:
   __instance = None
   @staticmethod 
   def get():
      """ Static access method. """
      if Redis.__instance == None:
         Redis()
      return Redis.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if Redis.__instance != None:
         raise Exception("This class is a singleton!")
      else:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        Redis.__instance = fakeredis.FakeStrictRedis() if str(ip_address) == "127.0.0.1" else redis.from_url(os.environ.get("REDIS_URL"))

# Redis functions ===============================
def seed_redis():
    Redis.get().flushdb()
    feed_posts = [
        {
            "id": "71e5cfa0-9e18-4810-8f73-afdb009203c0",
            "username": "user_a",
            "text": "first post!",
            "created_at": int(time.time()),
            "latitude": 37.2310016,
            "longitude": -121.7691648,
            "likes": ['username_a'],
            "type": "post",
        },
        {
            "id": "6fb4a31e-c9fa-4ab3-b160-9e043011426c",
            "username": "user_b",
            "text": "So Im currently an 18 year old boy whos been pro life for about as long as Ive known abortion existed. I just graduated high school a few weeks ago and this is pretty much just a rant about the hive mind of my now former school. Being pro life in my generation is something that gets looked down on, and peoples reaction to someone saying theyre pro life is about equal to if you tell them you kill puppies for fun. Thats the level of shock and disgust people my age have for someone being pro life. Rational conversations dont exist since holding that opinion makes you a misogynistic prick not worth their time. Anytime abortion is brought up they make the same few points and these points themselves prove they have zero knowledge of the science behind it. The points are",
            "created_at": int(time.time())+10,
            "latitude": 37.2310016,
            "longitude": -121.7691648,
            "likes": ['username_a'],
            "type": "post",
        },
        {
            "id": "4efa3744-0d5c-47d9-aa18-5c922a45c899",
            "username": "user_c",
            "text": "hello everyone",
            "created_at": int(time.time())+20,
            "latitude": 37.2310016,
            "longitude": -121.7691648,
            "likes": ['username_a'],
            "type": "post",
        },
    ]
    for post in feed_posts:  
        json_post = json.dumps(post)
        Redis.get().set(str(post['id']), json_post)

def add_or_update_redis(post):
    json_post = json.dumps(post)
    Redis.get().set(post['id'], json_post)

def get_redis_post(post_id):
    redis_post = r.get(str(post_id))
    return json.loads(redis_post)

def add_user_redis(user_id, username, provider_uid):
    user = {
        "id": user_id,
        "username": username,
        "provider_uid": provider_uid,
        "type": "user",
    }
    json_user = json.dumps(user)
    Redis.get().set(user_id, json_user)
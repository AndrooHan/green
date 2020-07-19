from redis_helper import Redis
import json 

def get_users():
    keys = Redis.get().keys()
    vals = Redis.get().mget(keys)
    json_vals = [json.loads(v) for v in vals]
    users = [item for item in json_vals if item['type'] == 'user']
    return users
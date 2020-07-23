import os
import tempfile
from redis_helper import Redis, feed_posts
import redis_helper
import pytest
from app import app
import json


# @pytest.fixture
# def client():
#     db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
#     flaskr.app.config['TESTING'] = True

#     with flaskr.app.test_client() as client:
#         with flaskr.app.app_context():
#             flaskr.init_db()
#         yield client

#     os.close(db_fd)
#     os.unlink(flaskr.app.config['DATABASE'])


def test_empty_db():
    rv = Redis.get().exists('hello')
    assert rv == 0

def test_like_message():
	with app.test_client() as c:
		feed_post_id = '71e5cfa0-9e18-4810-8f73-afdb009203c0'
		api_response = c.post('/like', json={
			'post_id': feed_post_id,
			'user_id': 'test_user_id'
		})
		
		assert 'test_user_id' in redis_helper.get_redis_post(feed_post_id)['likes']

def json_equal(jsona, jsonb):
	json.dumps(jsona, sort_keys=True) == json.dumps(jsonb, sort_keys=True)
    
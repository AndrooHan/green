# radar client 
import requests
from json import JSONEncoder
import json

test_secret = 'prj_test_sk_5ae3bc84823264425e7fda77c5eabf32b4989d4b'
'''
    {
  "meta": {
    "code": 200,
    "hasMore": false
  },
  "geofences": [
    {
      "_id": "5f13735973cf1800455e8054",
      "geometryCenter": {
        "coordinates": [
          -73.98566439999999,
          40.7484405
        ],
        "type": "Point"
      },
      "live": false,
      "enabled": true,
      "description": "Empire State Building",
      "type": "circle",
      "createdAt": "2020-07-18T22:10:33.905Z",
      "mode": "car",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -73.9844773064389,
              40.7484405
            ],
            ...
          ]
        ]
      },
      "geometryRadius": 100,
      "tag": "test_tag",
      "externalId": "test_external_id",
      "updatedAt": "2020-07-18T22:10:33.913Z"
    }
  ]
}
    '''
class Geofence:
    def __init__(self, externalId, description, geometry, *args, **kwargs):
        self.id = externalId
        self.description = description
        self.geometry = Geometry(**geometry)
    
    def to_json(self):
        return json.dumps(self, cls=MyEncoder)

class Geometry:
    def __init__(self, type, coordinates, *args, **kwargs):
        self.type = type
        self.coordinates = coordinates

    def to_json(self):
        return json.dumps(self, cls=MyEncoder)

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__ 

def list_all_geofences():
    uri = 'https://api.radar.io/v1/geofences'
    response = requests.get(uri,  headers={'Authorization': test_secret})
    json_response = json.loads(response.content)
    # for geofence in json_response['geofences']:
    #     print('Geofence: {}'.format(geofence))
    r = [Geofence(**geofence) for geofence in json_response['geofences']]
    print(r)
    return r
# https://api.radar.io/v1/search/geofences
def search_nearby_geofences(latitude, longitude):
    uri = 'https://api.radar.io/v1/search/geofences'
    payload = {
        'near': '{},{}'.format(latitude, longitude),
        'radius': '100', # minimum accepted value. We want fences we are in already
        'limit': '100'
    }
    response = requests.get(uri, headers={'Authorization': test_secret}, params=payload)
    json_response = json.loads(response.content)
    print(json_response)
    r = [Geofence(**geofence) for geofence in json_response['geofences']]
    print(r)
    return r

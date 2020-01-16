from pymongo import MongoClient
import requests
from time import sleep

client = MongoClient('localhost', 27017)
db = client.Permissions
collection = db.Permissions
posts = [
    {
        'Owner':'root',
        'Stranger':'ricardo',
        'Mode': 16877,
        'Timer': 10
    }
]
#r = requests.post('/a', data = posts)
db.Permissions.insert(posts)
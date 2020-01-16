from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from bson.json_util import dumps



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Permissions"
mongo = PyMongo(app)
    
posts = [
    {
        'Owner':'root',
        'Stranger':'ricardo',
        'Mode': 16877,
        'Timer': 10
    }
]

@app.route("/permission/<Owner>/<Stranger>", methods=['GET'])
def permission(Owner, Stranger):
    assert Owner == request.view_args['Owner']
    assert Stranger == request.view_args['Stranger']
    online_users = mongo.db.Permissions.find({'Owner': Owner, 'Stranger':Stranger },{'_id':0, 'Mode':1, 'Timer':1})
    v = list(online_users)
    print(v)
    print("AAA")
    return str(v)

@app.route("/insert/<Owner>/<Stranger>/<Mode>/<Timer>", methods=['GET'])
def insert(Owner, Stranger, Mode, Timer):
    assert Owner == request.view_args['Owner']
    assert Stranger == request.view_args['Stranger']
    assert Mode == request.view_args['Mode']
    assert Timer == request.view_args['Timer']
    mongo.db.Permissions.insert({'Owner': Owner, 'Stranger':Stranger, 'Mode': Mode, 'Timer': Timer })
    new_user = mongo.db.Permissions.find({'Owner': Owner, 'Stranger':Stranger, 'Mode': Mode, 'Timer': Timer })
    v = list(new_user)
    print(v)
    print("AAA")
    return str(v)

@app.route("/change/<Owner>/<Stranger>/<Mode>/<Timer>", methods=['GET'])
def change(Owner, Stranger, Mode, Timer):
    assert Owner == request.view_args['Owner']
    assert Stranger == request.view_args['Stranger']
    assert Mode == request.view_args['Mode']
    assert Timer == request.view_args['Timer']
    new_user = mongo.db.Permissions.find({'Owner': Owner, 'Stranger':Stranger})
    v = list(new_user)
    if len(str(v))>0:
        mongo.db.Permissions.update({'Owner': Owner, 'Stranger':Stranger}, {"$set": {'Mode': Mode, 'Timer': Timer} })
        new_user = mongo.db.Permissions.find({'Owner': Owner, 'Stranger':Stranger, 'Mode': Mode, 'Timer': Timer })
        v = list(new_user)
        print(v)
        print("AAA")
        return str(v)
    return 0
    
    







if __name__ == '__main__':
    app.run(debug=True)
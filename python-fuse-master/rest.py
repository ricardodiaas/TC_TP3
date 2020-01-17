from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from bson.json_util import dumps
import os
import socket
import threading
import json
import smtplib, ssl



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Permissions"
mongo = PyMongo(app)
    
def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    return s.getsockname()[0]




def sendmail(user, stranger, email, timer, group):
    print('mailsender active')
    print(stranger)
    print(user)
    print(group)
    ip = getip()
    print(ip)
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "tecnologiaseguranca1920@gmail.com"
    password = "ricardomateus"
    receiver_email = email
    # p = randrange(1,9999)
    message2 = " link: http://"+ip+":5000/insertgroup/"+stranger+"/"+group+"/10"
    subject = "Semeone is trying to access your files!!!"

    message1 = "The user with the name "+stranger+" is trying to accesss your file, to allow him click on the link below:\n"+message2
    msg = f'Subject: {subject} \n\n{message1}'
    print(msg)            
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        #server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        #server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
        
        
@app.route("/permission/<Owner>/<Stranger>", methods=['GET'])
def permission(Owner, Stranger):
    assert Owner == request.view_args['Owner']
    assert Stranger == request.view_args['Stranger']
    online_users = mongo.db.Permissions.find({'Owner': Owner, 'Stranger':Stranger },{'_id':0, 'Mode':1, 'Timer':1})
    v = list(online_users)
    data = json.dumps(v)
    r = Response(data, status=200, mimetype='application/json')
    print(v)

    return r

@app.route("/insert/<Owner>/<Stranger>/<Mode>/<Timer>", methods=['GET'])
def insert(Owner, Stranger, Mode, Timer):
    assert Owner == request.view_args['Owner']
    assert Stranger == request.view_args['Stranger']
    assert Mode == request.view_args['Mode']
    assert Timer == request.view_args['Timer']
    mongo.db.Permissions.insert({'Owner': Owner, 'Stranger':Stranger, 'Mode': Mode, 'Timer': Timer })
    new_user = mongo.db.Permissions.find({'Owner': Owner, 'Stranger':Stranger, 'Mode': Mode, 'Timer': Timer })
    v = list(new_user)
    data = json.dumps(v)
    r = Response(data, status=200, mimetype='application/json')
    
    return r

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
        data = json.dumps(v)
        r = Response(data, status=200, mimetype='application/json')
        return r
    return 0

def remove(name,group):
    os.system('deluser '+name+' '+group)
    mongo.db.Permissions.remove({'User':name, 'Group':group})

@app.route("/insertgroup/<User>/<Group>/<Timer>", methods=['GET'])
def InsertToGroup(User, Group, Timer):
    assert User == request.view_args['User']
    assert Group == request.view_args['Group']
    assert Timer == request.view_args['Timer']
    mongo.db.Permissions.insert({'User': User, 'Group':Group, 'Timer': Timer })
    new_user = mongo.db.Permissions.find({'User': User, 'Group':Group, 'Timer': Timer}, {'_id':0})
    v = list(new_user)
    t = threading.Timer(600,remove,[User,Group])
    os.seteuid(0)
    os.system('usermod -a -G'+Group+' '+User)
    t.start()
    
    data = json.dumps(v)
    r = Response(data, status=200, mimetype='application/json')
    return r



@app.route("/sendmail/<Owner>/<Stranger>/<Group>", methods=['GET'])
def Mail(Owner, Stranger, Group):
    assert Owner == request.view_args['Owner']
    assert Stranger == request.view_args['Stranger']
    assert Group == request.view_args['Group']
    sendmail(Owner,Stranger,"tecnologiaseguranca1920@gmail.com",10,Group)
    data = "Please Check your e-mail!"
    r = Response(data, status=200, mimetype='application/json')
    return r
    
    
    







if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    

# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context

from random import random

import os

from time import sleep
from threading import Thread, Event


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def fetch_data():
    cred = credentials.Certificate("static/weather-monitor-2019-firebase-adminsdk-dm8wu-c0f1c07493.json")

    # Initialize the app with a service account, granting admin privileges
    init_app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://weather-monitor-2019.firebaseio.com'
    })
    print(init_app.name)

    user = "ANKhM4ZhhAeOjKGu6SB3FTU6rFt2"
    device = "224e7159-3dc7-4eb9-bf0d-e2c0446e7f48"
    mode = "/Temp/Data"
    date = "/20-12-2019"

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('/users/' + user + '/GetWay/' + device + mode + date)
    # print(ref.get())

    print("Fetching data from server...")

    # ---
    # Have to add those queries before get()
    # limit_to_last() have to be after order_by_key()
    # --
    data = ref.order_by_key().limit_to_last(50).get()

    print("Sending 1st Batch...")

    for val in data:
        print(val)
        socketio.emit('newnumber', {'number': data[val], 'label': val}, namespace='/test')


    print("Update per minutue...")

    while not thread_stop_event.isSet():
        data = ref.order_by_key().limit_to_last(1).get()
        for val in data:
            print(val)
            socketio.emit('newnumber', {'number': data[val], 'label': val}, namespace='/test')
            socketio.sleep(60)
    # print(data.values)
    # print(data)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(fetch_data)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)

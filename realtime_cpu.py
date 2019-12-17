
# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
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
    date = "/18-10-2019"

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('/users/' + user + '/GetWay/' + device + mode + date)
    # print(ref.get())

    data = ref.get()

    # for day in data.values() :
    #     print(day)
    has_new_value = True

    # while not thread_stop_event.isSet():
    for val in data:
        print(val)
        socketio.emit('newnumber', {'number': data[val], 'label': val}, namespace='/test')
        socketio.sleep(1)
    # print(data.values)
    # print(data)


def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = round(random()*10, 3)
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(1)


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
    socketio.run(app)

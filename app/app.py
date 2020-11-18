
from logging import debug
import eventlet
import socketio
import multiprocessing
from text_to_image import text_to_image

sio = socketio.Server(cors_allowed_origins='http://localhost:8080')
app = socketio.WSGIApp(sio)

jobs = []

def respond():
    urls = text_to_image()
    sio.emit('serverToClient', urls)
    print('urls ', urls)

def access():
    print('acces')

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def clientToServer(sid, data):
    urls = text_to_image()
    sio.emit('serverToClient', urls, callback=access)
    print('urls ', urls)
    

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app, debug=True)
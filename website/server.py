from gevent import monkey
monkey.patch_all()
from chat import *
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
import os
from Tkinter import *
from tkMessageBox import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

DISCOVERY_URL = ('https://{api}.googleapis.com/'
	'$discovery/rest?version={apiVersion}')

# def callServer(message):
# 	'''Run a sentiment analysis request on text within a passed filename'''

# 	http = httplib2.Http()

# 	credentials = GoogleCredentials.get_application_default().create_scoped(
# 		['https://www.googleapis.com/auth/cloud-platform'])
# 	http = httplib2.Http()
# 	credentials.authorize(http)
	
# 	service = discovery.build('language', 'v1beta1',
# 		http = http, discoveryServiceUrl = DISCOVERY_URL)

# 	service_request = service.documents().analyzeSentiment(
#     	body={
#       	'document': {
#         	'type': 'PLAIN_TEXT',
#          	'content': message,
#       		}
#     	})
# 	response = service_request.execute()
# 	polarity = response['documentSentiment']['polarity']
# 	magnitude = response['documentSentiment']['magnitude']
# 	print "Sentiment: Emotion of %s (-1 to 1)" % (polarity * magnitude)
# 	return polarity * magnitude

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
socketio = SocketIO(app)

@app.route('/')
def chat():
  return render_template('chat.html')

@app.route('/login')
def login():
  return render_template('login.html')

@socketio.on('message', namespace='/chat')
def chat_message(message):
  #emotion = callServer(message['data']['message']) 
  print("message = ", message)
  sent = semantic(message['data']['message'])
  if sent < 0:
    showwarning('Warning', 'Please be more considerate')
    message['data']['message'] += "----- The Emotion on this message is Poor! :("
  else:
    message['data']['message'] += "----- The Emotion on this message is Good! :)"
  emit('message', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/chat')
def test_connect():
  emit('my response', {'data': 'Connected', 'count': 0})

if __name__ == '__main__':
  socketio.run(app)

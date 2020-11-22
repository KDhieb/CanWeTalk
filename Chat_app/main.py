import os
import socketio
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

sio = socketio.Client()

# Add Twilio authentication
account_sid = "ACcf38ea43fc81a1e3ad61701d6ebc096d"
auth_token = "19de24461133f84dad89be010d3b2554"
client = Client(account_sid, auth_token)


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    incoming_sms = request.args.get("incoming_sms")

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    socketio.emit('receive_message', data, room=data['room'])
    
    # Stores the room and message in a variable
    outbound_number = data['room']
    outbound_message = data['message']

    # Sends the message back to the user via SMS
    client.messages.create(
        to=outbound_number,
        from_="+16479058445",
        body=outbound_message
    )


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


# Routes for Twilio API
@app.route("/inbound_sms", methods=['GET', 'POST'])
def inbound_sms():
    response = MessagingResponse()

    # Grab information from incoming SMS message
    inbound_message = request.form['Body']
    from_number = request.form['From']
    to_number = request.form['To']

    # Store the above information in a data object to pass on
    data={'username': from_number, 'room': from_number, 'message': inbound_message}

    # Emits a received message using the above data object to the room number
    socketio.emit('receive_message', data, room=from_number)

    return 'message sent'

if __name__ == '__main__':
    socketio.run(app, debug=True)
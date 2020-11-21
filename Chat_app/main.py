from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

# Added by Ben:
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

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

    # username = request.args.get('from_n')
    # room = 1
    incoming_sms = request.args.get("incoming_sms")

    if username and room:
        return render_template('chat.html', username=username, room=room, incoming_sms=incoming_sms)
    else:
        return redirect(url_for('home'))


@socketio.on('send_message')
def handle_send_message_event(data):
    print(data)
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    socketio.emit('receive_message', data, room=data['room'])


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

    # Grab information from incoming message
    inbound_message = request.form['Body']
    from_number = request.form['From']
    to_number = request.form['To']

    # Print test messages
    print(inbound_message)
    print(from_number)
    print(to_number)

    # Resonse back to user
    # response.message("Message recieved")

    # Redirect to outbound_sms with message paramter
    return redirect(url_for('outbound_sms', message=inbound_message))

@app.route("/outbound_sms", methods=['GET', 'POST'])
def outbound_sms():

    # Capture message argument in a variable
    incoming_sms = request.args.get("message")
    print(incoming_sms)
    from_n='+6045621572'
    
    # participant = client.conversations \
    #     .conversations('CH6194ca428ad94766bbd997477b6d7327   ') \
    #     .participants \
    #     .create(
    #         messaging_binding_address='+16045621572',
    #         messaging_binding_proxy_address='16479058445'
    #     )

    # print(participant.sid)

    client.messages.create(
    # to="+15148348842", #Khalid
    to="+16045621572", #Ben
    from_="+16479058445",
    body=incoming_sms
)

    data={'username': 'adf', 'room': '1', 'message': 'THIS IS A VERY LONG MESAGE TO DETECT'}
    # emit('my response')
    # return
    print(data)


  
    return redirect(url_for('handle_send_message_event'))
    # return redirect(url_for('chat', incoming_sms=incoming_sms, room=1, username=from_n))
    # return redirect(handle_send_message_event, data={'username': "bob", 'room': 1 'message': 'test' })

if __name__ == '__main__':
    socketio.run(app, debug=True)
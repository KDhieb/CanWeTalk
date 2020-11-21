import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse()
    print(resp.value)

    resp.message("Welcome to the university help line. Please provide your name to continue.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
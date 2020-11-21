import os
from twilio.rest import Client

account_sid = "ACcf38ea43fc81a1e3ad61701d6ebc096d"
auth_token = "19de24461133f84dad89be010d3b2554"

client = Client(account_sid, auth_token)

client.messages.create(
    to="+16045621572",
    from_="+16479058445",
    body="This is a test"
)
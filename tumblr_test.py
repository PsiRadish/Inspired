import os
# from requests_oauthlib import OAuth1Session
import pytumblr
import json

# Credentials from the application page
client_key    = os.environ['CLIENT_KEY']
client_secret = os.environ['SECRET_KEY']
access_key    = os.environ['TEST_ACCESS_KEY']
access_secret = os.environ['TEST_ACCESS_SECRET']

user = pytumblr.TumblrRestClient(
    client_key,
    client_secret,
    access_key,
    access_secret
)

print(json.dumps(user.info(), sort_keys=True, indent=4, separators=(',', ': ')))

import os
# from requests_oauthlib import OAuth1Session
import pytumblr
import json

# Credentials from the application page
client_key    = os.environ['TUMBLR_CLIENT']
client_secret = os.environ['TUMBLR_SECRET']
access_key    = os.environ['TEST_ACCESS_KEY']
# access_key    = "55555555555555555555555555555555555555555555555555"
access_secret = os.environ['TEST_ACCESS_SECRET']
access_secret = "55555555555555555555555555555555555555555555555555"

user = pytumblr.TumblrRestClient(
    client_key,
    client_secret,
    access_key,
    access_secret
)

# print(json.dumps(user.info(), sort_keys=True, indent=4, separators=(',', ': ')))
print(json.dumps(user.info(), indent=4))

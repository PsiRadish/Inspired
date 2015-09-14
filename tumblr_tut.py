import os
from requests_oauthlib import OAuth1Session
import pytumblr

# Credentials from the application page
client_key = os.environ['CLIENT_KEY']
client_secret = os.environ['SECRET_KEY']

# OAuth URLs given on the application page
request_token_url       = 'http://www.tumblr.com/oauth/request_token'
authorization_base_url  = 'http://www.tumblr.com/oauth/authorize'
access_token_url        = 'http://www.tumblr.com/oauth/access_token'

# Fetch a request token
tumblr_oauth = OAuth1Session(client_key, client_secret=client_secret, callback_uri='http://www.tumblr.com/dashboard')

tumblr_oauth.fetch_request_token(request_token_url)

# Link user to authorization page
authorization_url = tumblr_oauth.authorization_url(authorization_base_url)
print('Please go here and authorize,\n' + authorization_url)

# Get the verifier code from the URL
redirect_response = input('Paste the full redirect URL here: ')
# redirect_response = "https://www.tumblr.com/dashboard?oauth_token=JQTsGZhgMjUQgTgvQAqori0UKaII99vTV3tiGEXFmNBBntuGHt&oauth_verifier=FS3STTAUEkS9lOeYn8LNy84CxoU8Yy4kfUD319HBTRqqiL2WrO"
tumblr_oauth.parse_authorization_response(redirect_response)

# Fetch the access token
access_tokens = tumblr_oauth.fetch_access_token(access_token_url)
access_key = access_tokens['oauth_token']
access_secret = access_tokens['oauth_token_secret']
print('access_key    =', access_key)
print('access_secret =', access_secret)

# Fetch a protected resource
# print(tumblr_oauth.get('http://api.tumblr.com/v2/user/dashboard'))

user = pytumblr.TumblrRestClient(
    client_key,
    client_secret,
    access_key,
    access_secret
)

print(user.info())

from flask import Flask, redirect, request
import requests
import base64
import json

app = Flask(__name__)

# Replace 'YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', and 'YOUR_REDIRECT_URI'
# with your actual Dropbox app credentials and the redirect URI you specified in your app settings.
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:5000/callback'

DROPBOX_AUTH_URL = 'https://www.dropbox.com/oauth2/authorize'
DROPBOX_TOKEN_URL = 'https://api.dropboxapi.com/oauth2/token'
DROPBOX_API_BASE_URL = 'https://api.dropboxapi.com/2'

@app.route('/')
def home():
    # Construct the authorization URL
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'token_access_type': 'offline',  # Requests refresh token
        'state': 'asdfasfsaf'  # You can add a random state for added security
    }
    authorization_url = f"{DROPBOX_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        # Exchange the authorization code for an access token
        auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        headers = {
            'Authorization': f"Basic {auth_header}"
        }

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }

        response = requests.post(DROPBOX_TOKEN_URL, data=data, headers=headers)
        if response.status_code == 200:
            client_credentials = response.json()
            print(client_credentials)
            return f"Access Token: {json.dumps(client_credentials)}"
        else:\
            return "Failed to get the access token."
    else:
        return "Authorization code not found."

if __name__ == '__main__':
    app.run(port=5000)

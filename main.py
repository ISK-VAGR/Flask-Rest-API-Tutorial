from flask import Flask, request, jsonify
from functools import wraps
from flask import Flask, request, abort
from flask_restful import Api, Resource, fields, marshal_with
import requests

app = Flask(__name__)
api = Api(app)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'X-API-KEY' not in request.headers:
            abort(401)  # Unauthorized if API key is missing
        else:
            api_key = request.headers['X-API-KEY']
            if not is_valid_api_key(api_key):
                abort(403)  # Forbidden if API key is invalid
        return f(*args, **kwargs)
    return decorated_function

import requests

def is_valid_api_key(api_key):
    # Replace the following URL with the actual URL of your SharePoint list API
    url = "https://your_sharepoint_site/_api/web/lists/GetByTitle('APIKeys')/items"
    headers = {
        "Accept": "application/json;odata=verbose",
        "Authorization": "Bearer " + "your_access_token",  # Replace with actual method to get access token
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json()['d']['results']
            for item in items:
                if api_key == item['APIKey']:  # Adjust 'APIKey' based on your SharePoint list column name
                    return True
        return False
    except Exception as e:
        print(f"Error validating API key against SharePoint: {e}")
        return False

from flask_restful import Resource, marshal_with

# Assuming you've already set up your resource fields and require_api_key decorator

resource_fields = {
    'status': fields.String,
    'message': fields.String
}

class UserAccess(Resource):
    @marshal_with(resource_fields)
    @require_api_key
    def get(self):
        # This is just an example endpoint to illustrate the concept
        # Replace with your actual logic
        return {'status': 'success', 'message': 'Access granted'}

# Add the resource to the API
api.add_resource(UserAccess, "/user-access")

if __name__ == "__main__":
    app.run(debug=True)  # Turn off debug in production environments
from flask import Flask, jsonify, request, Blueprint
from pymongo import MongoClient
from bson import ObjectId
from flask_restful import Resource, Api

# Connect to the  database
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['users']

# Create a blueprint for the User resource
users_bp = Blueprint('users', __name__)
api = Api(users_bp)

class UserResource(Resource):
    def get(self):
        # Retrieve all users from database
        users = collection.find()
        result = []
        for user in users:
            result.append({
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'password': user['password']
            })
        return jsonify(result)

    def get(self, id):
        # Retrieve a specific user from database
        user = collection.find_one({'_id': ObjectId(id)})
        if user:
            result = {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'password': user['password']
            }
            return jsonify(result)
        else:
            return jsonify({'message': 'User not found'})

    def post(self):
        # Create a new user 
        data = request.get_json()
        user = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        result = collection.insert_one(user)
        return jsonify({'message': 'User created successfully'})

    def put(self, id):
        # Update an existing user 
        data = request.get_json()
        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'name': data['name'], 'email': data['email'], 'password': data['password']}}
        )
        if result.modified_count > 0:
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'message': 'User not found'})

    def delete(self, id):
        # Delete a user 
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'})

# Register the UserResource blueprint
api.add_resource(UserResource, '/users', '/users/<id>')

app = Flask(__name__)

# Register the users blueprint with the app
app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(debug=True)

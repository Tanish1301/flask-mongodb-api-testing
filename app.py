from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['users']

# API endpoints
@app.route('/users', methods=['GET'])
def get_all_users():
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

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
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

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = collection.insert_one(user)
    return jsonify({'message': 'User created successfully'})

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    result = collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': {'name': data['name'], 'email': data['email'], 'password': data['password']}}
    )
    if result.modified_count > 0:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)

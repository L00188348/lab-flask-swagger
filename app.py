from flask import Flask, render_template, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

users = [
    {'id': 1, 'name': 'John', 'email': 'john@email.com', 'age': 30},
    {'id': 2, 'name': 'Mary', 'email': 'mary@email.com', 'age': 25}
]

@app.route('/')
def landing():
    return render_template('index.html')

# GET all users
@app.route('/api/users', methods=['GET'])
def list_users():
    """Endpoint that returns a list of all users
    ---
    responses:
      200:
        description: List of users
        examples:
          application/json: [{"id": 1, "name": "John", "email": "john@email.com", "age": 30}]
    """
    return jsonify(users)

# GET specific user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint that returns a specific user by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User found
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

# POST create new user
@app.route('/api/users', methods=['POST'])
def create_user():
    """Endpoint that creates a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            age:
              type: integer
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid data
    """
    data = request.json
    
    # Basic validation
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'message': 'Name and email are required'}), 400
    
    # Create new user
    new_user = {
        'id': len(users) + 1,
        'name': data.get('name'),
        'email': data.get('email'),
        'age': data.get('age', 0)  # Default age 0 if not provided
    }
    users.append(new_user)
    
    return jsonify({'message': 'User created!', 'user': new_user}), 201

# PUT update existing user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Endpoint that updates an existing user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            age:
              type: integer
    responses:
      200:
        description: User updated successfully
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.json
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    user['age'] = data.get('age', user['age'])
    
    return jsonify({'message': 'User updated!', 'user': user})

# DELETE user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Endpoint that deletes a user
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    users = [u for u in users if u['id'] != user_id]
    return jsonify({'message': 'User deleted!'})

# GET users by age (query parameter example)
@app.route('/api/users/filter/by-age', methods=['GET'])
def filter_users_by_age():
    """Endpoint that filters users by minimum age
    ---
    parameters:
      - name: min_age
        in: query
        type: integer
        required: true
        description: Minimum age to filter
    responses:
      200:
        description: Filtered list of users
      400:
        description: min_age parameter required
    """
    min_age = request.args.get('min_age', type=int)
    
    if min_age is None:
        return jsonify({'message': 'min_age parameter is required'}), 400
    
    filtered_users = [u for u in users if u['age'] >= min_age]
    return jsonify(filtered_users)

# GET statistics
@app.route('/api/users/stats/summary', methods=['GET'])
def user_statistics():
    """Endpoint that returns user statistics
    ---
    responses:
      200:
        description: User statistics
        examples:
          application/json: {"total_users": 2, "average_age": 27.5}
    """
    total = len(users)
    avg_age = sum(u['age'] for u in users) / total if total > 0 else 0
    
    return jsonify({
        'total_users': total,
        'average_age': round(avg_age, 1)
    })

if __name__ == '__main__':
    app.run(debug=True)
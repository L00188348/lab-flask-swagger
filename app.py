from flask import Flask, render_template, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def list_users():
    """Endpoint that returns a list of users
    ---
    responses:
      200:
        description: List of users
        examples:
          application/json: [{"id": 1, "name": "John", "email": "john@email.com"}]
    """
    users = [
        {'id': 1, 'name': 'John', 'email': 'john@email.com'},
        {'id': 2, 'name': 'Mary', 'email': 'mary@email.com'}
    ]
    return jsonify(users)

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
    responses:
      201:
        description: User created successfully
    """
    data = request.json
    return jsonify({'message': 'User created!', 'user': data}), 201

if __name__ == '__main__':
    app.run(debug=True)
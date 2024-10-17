
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'postgres')
db_host = os.getenv('DB_HOST', '54.237.98.29')
db_name = os.getenv('DB_NAME', 'test')
db_port = os.getenv('DB_PORT', '5432')
                    
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
db = SQLAlchemy(app)





# Default route for testing
@app.route('/')
def index():
    return "Hello, World welcome to Python Flask app with Postgresql Database!"


@app.route('/db-check', methods=['GET'])
def db_check():
    try:
        # Run a simple query to check the database connection
        result = db.session.execute(text('SELECT 1'))
        return "Database connection is successful! Webhook added", 200
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500

# Create a route to insert a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    
    # Validate the incoming data
    if not data or 'name' not in data:
        return jsonify({'message': 'Invalid request, name is required'}), 400

    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': f"User '{new_user.name}' added successfully"}), 201

# Create a route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users]), 200


if __name__ == '__main__':
    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5001)


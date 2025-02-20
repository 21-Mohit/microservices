from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_required, current_user
from pymongo import MongoClient
from datetime import datetime
import uuid
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,decode_token

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Required for Flask-Login

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
  # Redirect unauthorized users to login page
jwt = JWTManager(app)
# Connect to MongoDB
client = MongoClient("mongodb+srv://palmohit897:1234567890@cluster0.tbarxzw.mongodb.net/")
db = client["microservice"]
#users_collection = db["users"]
orders_collection = db["orders"]

# Dummy User Model (Authentication is handled in user_service)



# Place an Order (User must be logged in)
@app.route('/order', methods=['POST'])
@jwt_required()
def place_order():
    user = get_jwt_identity()
    return jsonify({"message": f"Welcome {user}, here are your orders!"})

    products = data.get("products")  # List of product IDs & quantities

    if not products:
        return jsonify({"error": "No products in order"}), 400

    order = {
        "order_id": str(uuid.uuid4()),
        "user_id": current_user.id,
        "products": products,
        "status": "Processing",
        "created_at": datetime.utcnow()
    }

    orders_collection.insert_one(order)
    return jsonify({"message": "Order placed successfully!", "order_id": order["order_id"]}), 201

# Get User Orders
@app.route('/orders', methods=['GET'])
@jwt_required(locations=["cookies"])
def get_orders():
    user = get_jwt_identity()
    return jsonify({"message": f"Welcome {user}, here are your orders!"})
    token = request.args.get('token')  # ✅ Get token from URL

    if not token:
        return jsonify({"error": "Missing token"}), 401

    try:
        user = decode_token(token)["sub"]  # ✅ Decode JWT token
        return jsonify({"message": f"Welcome {user}, here are your orders!"})
    except Exception as e:
        return jsonify({"error": "Invalid token"}), 401

    user = get_jwt_identity()
    return jsonify({"message": f"Welcome {user}, here are your orders!"})

# Update Order Status
@app.route('/order/<order_id>', methods=['PUT'])
@login_required
def update_order_status(order_id):
    new_status = request.json.get("status")

    if new_status not in ["Processing", "Shipped", "Delivered", "Cancelled"]:
        return jsonify({"error": "Invalid status"}), 400

    result = orders_collection.update_one(
        {"order_id": order_id, "user_id": current_user.id},
        {"$set": {"status": new_status}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Order not found or status unchanged"}), 404

    return jsonify({"message": "Order status updated successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)

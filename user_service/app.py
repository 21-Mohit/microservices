from flask import Flask, jsonify, request, render_template_string
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient
from db import save_user,get_user
from flask import Flask, render_template,request, redirect, url_for
from flask_login import current_user,LoginManager,login_user, logout_user, login_required
from user import User

app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Change this in production
jwt = JWTManager(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://palmohit897:1234567890@cluster0.tbarxzw.mongodb.net/")
db = client["microservice"]
users_collection = db["users"]
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# User Registration

@app.route('/signup', methods = ['GET','POST'])
def signUp():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        save_user(username,password)
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

# User Login
@app.route('/login',methods=['GET','POST'])
def login():
    
    #if current_user.is_authenticated:
       # return redirect("http://localhost:5003/orders")

    message = '' 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user and user.check_password(password):
            login_user(user)
            access_token = create_access_token(identity=username)
            response = redirect(f"http://localhost:5003/orders?token={access_token}")
            response.set_cookie("access_token_cookie", access_token, httponly=True,samesite="Lax")
            return response
            #return jsonify({"message": "Login successful", "access_token": access_token}), 200
        else:
            message = "failed to login"
    return render_template('login.html', message = message)

@app.route('/')
def home():
    return render_template("index.html")


@login_manager.user_loader
def load_user(username):
    return get_user(username)

if __name__ == '__main__':
    app.run(debug=True, port=5002)

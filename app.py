from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Shubhh%408128%24@localhost/rest_api_crud_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return{
        "success":True,
        "message": "REST API CRUD Server is Running"
    }

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return{
            "success":False,
            "message":"Name and email are required"
        },400

    user = User(name=name, email=email)

    db.session.add(user)
    db.session.commit()

    return {
        "success":True,
        "message":"User created successfully",
        "user":{
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }, 201


@app.route("/api/users", methods=["GET"])
def get_users():
    users= User.query.all()

    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })

    return {
        "success":True,
        "message":user_list
    },200

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {
            "success":False,
            "message": "User not found"
        }, 404

    return {
        "success": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }, 200


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }, 404

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {
            "success": False,
            "message": "Name and Email are required"
        }, 400

    user.name = name
    user.email = email

    db.session.commit()

    return {
        "seccuss": True,
        "message": "User updated successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }, 200


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }, 404

    db.session.delete(user)
    db.session.commit()

    return{
        "success": True,
        "message": "User deleted successfully"
    }, 200



if __name__ == "__main__":
    app.run(debug=True)
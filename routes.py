# routes

from flask import Blueprint, request, jsonify
from models import db, Tasks, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def test():
    return "Yeah! It's Working !!!"


@routes_bp.route("/tasks", methods = ['GET'])
@jwt_required()
def get_tasks():
    completed = request.args.get('completed')
    current_user_id = get_jwt_identity()
    if completed is not None:
        if completed.lower() == 'true':
            status_flag = True
        elif completed.lower() == 'false':
            status_flag = False
        else:
            return jsonify({"error":"Invalid value for completed. Use 'true' or 'false'."}), 400

        filtered_tasks = Tasks.query.filter(Tasks.completed == status_flag, Tasks.user_id == current_user_id).all()
        return jsonify([task.to_dict() for task in filtered_tasks]), 200

    all_tasks = Tasks.query.filter(Tasks.user_id == current_user_id).all()
    return jsonify([task.to_dict() for task in all_tasks]), 200


@routes_bp.route("/tasks", methods = ['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    print("Incoming JSON data:", data)  # Debug print
    title = data.get('title')
    description = data.get('description')
    current_user_id = get_jwt_identity()
    if not title or not isinstance(title, str) or title.strip() == "":
        return jsonify({"error":"The title value is not provided"}), 400

    new_task = Tasks(title = title.strip(), description = description.strip() if description else '', completed = False, user_id = current_user_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"success":True, "task":new_task.to_dict()}), 201



@routes_bp.route("/tasks/<int:given_id>", methods = ['GET', 'PUT', 'DELETE'])
@jwt_required()
def task_handler_id(given_id):
    current_user_id =  get_jwt_identity()

    task = Tasks.query.filter(Tasks.id == given_id, Tasks.user_id == current_user_id).first()
    if not task:
        return jsonify({"error":"Task with given id not found!"}), 404

    if request.method == 'GET':
        return jsonify(task.to_dict()), 200

    elif request.method == 'PUT':
        data = request.get_json()
        title = data.get('title')
        completed = data.get('completed')

        if title is None and completed is None:
            return jsonify({"error":"Title and Completed value not provided"}), 400

        if title is not None :
            if not isinstance(title, str) or title.strip() == "":
                return jsonify({"error":"Title should be a valid string !"}), 400
            task.title = title.strip()

        if completed is not None:
            if not isinstance(completed, bool):
                return jsonify({"error": "Completed should be a boolean value !"}), 400
            task.completed = completed

        db.session.commit()
        return jsonify({"success":True, "task":task.to_dict()}), 200

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({"success": True, "message": f"Task {task.id} deleted"}), 200


@routes_bp.route("/register", methods = ['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username is None or (password is None or password.strip() == ""):
        return jsonify({"error": "Invalid username or password"}), 400


    username_valid = User.query.filter_by(username = username).first()
    if username_valid:
        return jsonify({"error":"Username already taken, please provide a different username ! "}), 409

    hashed_password = generate_password_hash(password)
    user = User(username, hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"success":True, "message":f"user with username -  {username} created"}), 201



@routes_bp.route("/login", methods = ['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return jsonify({"error": "Invalid username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error":"Invalid username or password"}), 400

    access_token = create_access_token(identity = str(user.id))
    return jsonify(access_token = access_token), 200


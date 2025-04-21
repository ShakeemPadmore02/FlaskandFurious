from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize, get_current_user
from flask_jwt_extended import ( # type: ignore
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    current_user,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)



index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
#@jwt_required()
def index_page():
    current_user = get_current_user()
    if not current_user:
        return render_template('login.html')
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
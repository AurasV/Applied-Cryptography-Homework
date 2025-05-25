from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies
from passlib.hash import bcrypt
import enum
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ac_user:172003@localhost/ac_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'this-is-a-secret-key-aurel'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

class UserType(enum.Enum):
    user = "user"
    admin = "admin"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.Enum(UserType), default=UserType.user)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
@jwt_required()
def admin_page():
    claims = get_jwt()
    if claims.get('type') != 'admin':
        return render_template('unauthorized.html'), 403
    return render_template('admin.html')

@app.route('/admin/data')
@jwt_required()
def admin_data():
    claims = get_jwt()
    if claims.get('type') != 'admin':
        return jsonify(msg="Admins only!"), 403

    users = User.query.all()
    result = [{'id': u.id, 'username': u.username, 'email': u.email, 'type': u.user_type.value} for u in users]
    return jsonify(users=result)

@app.route('/users/new', methods=['POST'])
def register_user():
    data = request.get_json()
    user_type_str = data.get('type', 'user')
    try:
        user_type = UserType(user_type_str)
    except ValueError:
        return jsonify(msg="Invalid user type"), 400

    hashed = bcrypt.hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=hashed, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(msg=f"{user_type.name.capitalize()} created"), 201

@app.route('/users/admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    hashed = bcrypt.hash(data['password'])
    new_admin = User(username=data['username'], email=data['email'], password=hashed, user_type=UserType.admin)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify(msg="Admin created"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.verify(data['password'], user.password):
        token = create_access_token(identity=str(user.id), additional_claims={
            'username': user.username,
            'type': user.user_type.name
        })
        response = jsonify(msg="Login successful", access_token=token)
        set_access_cookies(response, token)
        return response
    return jsonify(msg="Bad username or password"), 401


@app.route('/logout', methods=['POST'])
def logout():
    resp = jsonify(msg="Logged out")
    unset_jwt_cookies(resp)
    return resp

@app.route('/users/<int:user_id>')
@jwt_required()
def get_user(user_id):
    claims = get_jwt()
    identity = get_jwt_identity()
    if claims.get('type') != 'admin' and int(identity) != user_id:
        return jsonify(msg="Unauthorized"), 403
    user = User.query.get_or_404(user_id)
    return jsonify(id=user.id, username=user.username, email=user.email, type=user.user_type.value)

@app.route('/me')
@jwt_required()
def me():
    claims = get_jwt()
    identity = get_jwt_identity()
    return jsonify(
        id=identity,
        username=claims.get("username"),
        type=claims.get("type")
    )

if __name__ == '__main__':
    app.run(debug=True)

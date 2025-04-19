from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['JWT_SECRET_KEY']='GUVIHCL123#@#@'
db=SQLAlchemy(app)
jwt=JWTManager(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100),unique=True, nullable=False)
    password=db.Column(db.String(200), nullable=False)


@app.route('/api/register',methods=['POST'])
def register_user():
    data=request.json
    existing_user=User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message':'User already exists'}), 400
    hashed_password=generate_password_hash(data['password'],method='pbkdf2:sha256')
    new_user=User(name=data['name'],email=data['email'],password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User Registered Successfully'}), 201


@app.route('/api/login',methods=['POST'])
def login_user():
    data=request.json
    user=User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password,data['password']):
        access_token=create_access_token(identity=str(user.id))
        return jsonify({'access_token':access_token})
    return jsonify({'message':'Invalid Credentials'}), 401



@app.route('/api/users',methods=['GET'])
@jwt_required()
def get_users():
    current_user_id=get_jwt_identity()
    users=User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])


@app.route('/test',methods=['GET'])
def Test():
    data={"app":True}
    return jsonify(data)


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
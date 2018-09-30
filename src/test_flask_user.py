#!/usr/bin/env python

import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse, fields, marshal
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# initialization
app = Flask('test_flask_userapi')
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'users'  # 定义表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True)
    password_hash = db.Column(db.String(256))

    def hash_password(self, password):
        """
        密码散列
        :param password: 明文密码
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        接受一个明文的密码作为参数并且当密码正确的话返回 True 
        或者密码错误的话返回 False。当用户提供和需要验证凭证的时候调用。
        :param password: 明文密码
        :return: 验证结果
        """
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        """
        生成令牌
        :param expiration: 
        :return: 
        """""
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        验证令牌
        :param token: 令牌
        :return: 
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


@app.route('/api/users', methods=['POST'])
def new_user():
    r = reqparse.RequestParser()
    r.add_argument('username', type=str, location='json')
    r.add_argument('password', type=str, location='json')
    args = r.parse_args()
    username = args.get('username')
    password = args.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    print(user)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@auth.verify_password
def verify_password(username_or_token, password):
    # 先验证token, 没有token则 验证用户名 密码
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()  # 获取用户名
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username })

if __name__ == "__main__":

    print("test flask user api!")
    if not os.path.exists('db.sqlite'):
        db.create_all()

    app.run(debug=True)  # 调试时用，好处，修改代码后，不用重启程序
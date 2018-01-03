# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify

bpaccount = Blueprint('account', __name__, template_folder='templates')
import application.model as model


@bpaccount.route('/account', methods=['POST'])
def register():
    username = (request.json.get('username') or '').strip()
    password = request.json.get('password') or ''
    email = (request.json.get('email') or '').strip()

    if not username:
        return jsonify({'error': 'Empty field "username"'}), 400

    if not password:
        return jsonify({'error': 'Empty field "password"'}), 400

    if not email:
        return jsonify({'error': 'Empty field "email"'}), 400

    user = model.account_register(username=username, password=password, email=email)

    if user:
        return jsonify({'token': user['token']}), 201
    else:
        return jsonify({'error': 'Account register error'}), 400


@bpaccount.route('/account/token', methods=['POST'])
def login():
    username = (request.json.get('username') or '').strip()
    password = request.json.get('password') or ''

    if not username:
        return jsonify({'error': 'Empty field "username"'}), 400

    if not password:
        return jsonify({'error': 'Empty field "password"'}), 400

    user = model.account_login(username=username, password=password)
    if user:
        return jsonify({'token': user['token']}), 200
    else:
        return jsonify({'error': 'Bad credentials'}), 403

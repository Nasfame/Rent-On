import csv
import json
import time

import jwt
from flask import Blueprint, request

owner = Blueprint('owner', __name__)


@owner.route('/details')
def listing():
    with open('data/owners.csv', 'r') as f1:
        f1 = csv.DictReader(f1)
        li = list(f1)
    return json.dumps(li)


@owner.route('/register', methods=['POST'])
def create():
    with open('data/owners.csv', 'a') as f1:
        f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'password'])
        cnt = json.loads(listing())
        values = request.json
        print(values)
        values['id'] = len(cnt) + 1
        f1.writerow(values)
    return json.dumps("Success")


@owner.route('/login', methods=['POST'])
def login():
    login_data = list(request.json.values())
    db = json.loads(listing())
    values = []
    role = ''
    id = ''
    for i in db:
        values.append([i['name']])
        if i['name'] == login_data[0] and i['password'] == login_data[1]:
            role = 'owner'
            id = i['id']
            break
    admin = {'username': 'Hiro', 'password': 'Hi123'}
    if login_data == admin.values():
        role: 'admin'
    payload = {'id': id, 'username': login_data[0], 'role': role,
               'time': time.time() + 3600}  # LoggedOutafter 1hr 3600sec
    encode_jwt = jwt.encode(payload, 'hiro')
    return {'auth_token': encode_jwt.decode()}  # converts bits to string

import csv
import json
import time

import jwt
from flask import Blueprint, request

platform = Blueprint('platform', __name__)


def checkauth(auth_token):
    decoded = jwt.decode(auth_token, 'hiro')
    if decoded['time'] < time.time() or decoded['role'] == '':
        return json.dumps("Service Unavailable for Yu!")


@platform.route('/properties/<auth_token>')
def listing(auth_token):
    try:
        checkauth(auth_token)
        with open('data/property.csv', 'r') as f1:
            f1 = csv.DictReader(f1)
            li = list(f1)
        return json.dumps(li)
    except jwt.exceptions.DecodeError:
        return json.dumps("Try New Auth Code")
    except:
        return json.dumps("Unknown Error")


@platform.route('/register/<auth_token>', methods=['POST'])
def create(auth_token):
    try:
        decoded = jwt.decode(auth_token, 'hiro')
        if decoded['time'] < time.time() or decoded['role'] != 'admin' or decoded['role'] != 'owner':
            return json.dumps("Insufficient Power")
        with open('data/property.csv', 'a') as f1:
            f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'area', 'BHK', 'amenities', 'furnishing', 'locality',
                                                'owner_name'])
            cnt = json.loads(listing(auth_token))
            values = request.json
            print(values)
            values['id'] = len(cnt) + 1
            f1.writerow(values)
        return json.dumps("Success")
    except jwt.exceptions.DecodeError:
        return json.dumps("Try New Auth Code")
    except:
        return json.dumps("Unknown Error")


@platform.route('/modify/<int:id>/<auth_token>', methods=['PATCH'])
def edit(id, auth_token):
    try:
        decoded = jwt.decode(auth_token, 'hiro')
        if decoded['time'] < time.time() or decoded['role'] not in ['admin', 'owner']: return json.dumps(
            "Insufficient Power")
        info = request.json
        info['id'] = id
        cnt = json.loads(listing(auth_token))
        if id > len(cnt): return json.dumps("Sorry Data unavailable")
        cnt[id] = info
        with open('data/property.csv', 'w') as f1:
            f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'area', 'BHK', 'amenities', 'furnishing', 'locality',
                                                'owner_name'])
            f1.writeheader()
            f1.writerows(cnt)
        return json.dumps("Modified property successfully")
    except jwt.exceptions.DecodeError:
        return json.dumps("Try New Auth Code")
    except:
        return json.dumps("Unknown Error")


@platform.route('/delete/<int:id>/<auth_token>', methods=['DELETE'])
def delete(id, auth_token):
    try:
        decoded = jwt.decode(auth_token, 'hiro')
        if decoded['time'] < time.time() or decoded['role'] not in ['admin', 'owner']: return json.dumps(
            "Insufficient Power")
        cnt = json.loads(listing(auth_token))
        if id > len(cnt): return json.dumps("Sorry Data unavailable")
        cnt.pop(id - 1)
        with open('data/property.csv', 'w') as f1:
            f1 = csv.DictWriter(f1, fieldnames=['id', 'name', 'area', 'BHK', 'amenities', 'furnishing', 'locality',
                                                'owner_name'])
            f1.writeheader()
            f1.writerows(cnt)
        return json.dumps("Deleted property successfully")
    except jwt.exceptions.DecodeError:
        return json.dumps("Try New Auth Code")
    except:
        return json.dumps("Unknown Error")

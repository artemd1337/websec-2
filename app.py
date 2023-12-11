import flask
import json
import sqlite3

from flask import Flask, request
from flask_cors import CORS
from parser import parse_timetable, get_current_week

app = Flask(__name__, template_folder='template')
CORS(app, resources={r'/api/*': {'origins': '*'}})


@app.route('/api/get_timetable', methods=["POST"])
def get_timetable():
    data = request.json
    category = data['category']
    if category not in ["group", "staff"]:
        return flask.abort(404)
    id = data['id']
    week = 0
    if 'week' in data:
        week = int(data['week'])
    day = 0
    if 'day' in data:
        day = int(data['day'])
    result = parse_timetable(category, int(id), week, day)
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@app.route("/api/get_timetable_lk/", methods=["GET"])
def get_timetable_lk():
    data = request.args
    category = data['category']
    if category not in ["group", "staff"]:
        return flask.abort(404)
    id = data['id']
    week = 0
    if 'week' in data:
        week = int(data['week'])
    day = 0
    if 'day' in data:
        day = int(data['day'])
    result = parse_timetable(category, int(id), week, day)
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@app.route('/api/get_current_week', methods=['GET'])
def get_current_week_route():
    week_number = get_current_week()
    return json.dumps(week_number), 200, {'Content-Type': 'application/json'}


@app.route("/api/search", methods=['get'])
def search():
    data = flask.request.args
    searchString = ""
    if 'text' in data:
        searchString = data['text']
    if searchString == '':
        return json.dumps([]), 200, {'Content-Type': 'application/json'}
    if searchString[0].isdigit():
        table_name = "groups"
    elif searchString[0].isalpha():
        table_name = "teachers"
    else:
        return json.dumps([]), 200, {'Content-Type': 'application/json'}
    database_result = []
    with sqlite3.connect("database.sqlite3") as conn:
        request = "select id, name from "+table_name+" where name LIKE '%" + searchString + "%' LIMIT 5;"
        data = conn.execute(request)
        database_result = data.fetchall()
    result = []
    for id, name in database_result:
        if table_name == "groups":
            result.append({'id': id, 'name': name, 'category': 'group'})
        else:
            result.append({'id': id, 'name': name, 'category': 'staff'})
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run()

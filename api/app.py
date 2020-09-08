import json
from json import dumps
import os
# import magic
import urllib.request

import jsonpickle as jsonpickle
from flask import Flask, flash, request, redirect, render_template, make_response, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import random
import string
from flask_mysql_connector import MySQL
import csv
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
FlaskJSON(app)
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Test1234@'
app.config['MYSQL_DATABASE'] = 'traineeboats'
mysql = MySQL(app)
CORS(app)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "./uploads/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'txt', 'csv'}


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/list', methods=['GET'])
def list1():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dim_vessel")
    # data = cursor.fetchall()
    # print(data)
    # data1 = {Boat(i[0], i[1], i[2], i[3]) for i in data}
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


@app.route('/api/list', methods=['DELETE'])
def delete():
    rows = tuple(request.get_json())
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM dim_vessel WHERE mmsi IN (%s)" % ','.join(['%s'] * len(rows))
    cursor.execute(sql, rows)
    mysql.connection.commit()
    # data = cursor.fetchall()
    # print(data)
    # data1 = {Boat(i[0], i[1], i[2], i[3]) for i in data}
    return ""


@app.route('/api/get_vessel', methods=['GET'])
def get_vessel():
    q = request.args.get("q") or ""
    page = int(request.args.get("page") or 0)
    count = int(request.args.get("count") or 0)
    cursor = mysql.connection.cursor()
    sql = """SELECT * FROM dim_vessel"""
    if q != "":
        sql += " WHERE mmsi LIKE %(q)s OR imo LIKE %(q)s  OR name LIKE %(q)s OR type LIKE %(q)s"
    if page != 0 and count != 0:
        sql += " LIMIT %(page)s,%(limit)s"
        # val = (q, q, q, q, str(page), str(count))
        val = {
            "q": q,
            "limit": count,
            "page": page
        }
    elif count != 0 and page == 0:
        sql += " LIMIT %(limit)s"
        # val = (q, q, q, q, count)
        val = {
            "q": q,
            "limit": count,
        }
    else:
        val = {
            "q": q
        }
    cursor.execute(sql, val)
    # data = cursor.fetchall()
    # print(data)
    # data1 = {Boat(i[0], i[1], i[2], i[3]) for i in data}
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No file selected for uploading'
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], get_random_string(10))
            file.save(filename)

            with open(filename, newline='') as f:
                reader = csv.reader(f, delimiter=",")
                data = list(reader)

            val = []
            for i in data:
                # print(len(i))
                if len(i) == 5:
                    if i[1].isdigit() and i[0].isdigit():
                        val.append((i[1], i[0], i[2], i[4]))
                    # if not mysql.new_cursor().execute("SELECT Name, COUNT(1) FROM dim_vessel WHERE mmsi = %s", (i[1])).fetchone()[0]:

            cursor = mysql.connection.cursor()
            cursor.executemany(
                "INSERT INTO dim_vessel(mmsi, imo, name, type) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE mmsi=mmsi",
                val)
            mysql.connection.commit()

            os.remove(filename)

        return 'File successfully uploaded'
    else:
        return 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'


if __name__ == '__main__':
    app.run()


class Boat:
    def __init__(self, mmsi, imo, name, type):
        self.mmsi = mmsi
        self.imo = imo
        self.name = name
        self.type = type

    mmsi = ""
    imo = ""
    name = ""
    type = ""

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs361_renfroc"
app.config["MYSQL_PASSWORD"] = "DHSwrestler11294!!"
app.config["MYSQL_DB"] = "cs361_renfroc"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def home_page():
    if request.method == 'GET':
        city_query = "SELECT city_id, city_name \
FROM Cities \
ORDER BY city_name ASC;"
        
        cur = mysql.connection.cursor()
        cur.execute(city_query)
        name = cur.fetchall()
        mysql.connection.commit()
        return render_template('index.html', city_name=name)

    if request.method == "POST":
        if request.form.get("Create"):
            return render_template('index.html', read=name)

@app.route('/details', methods=['GET','POST'])
def details():

    return render_template('details.html')

if __name__ == "__main__":
    app.run(port=46789, debug=True)
import os
from dotenv import load_dotenv
from flask import Flask, request    #for posting and getting from db
from flask import redirect, url_for  #for redirecting pages
from flask import render_template  #html template
from flask import session  #session variables
from datetime import timedelta #for permanent session things
from flask import flash #for flashing messages between pages
from flask_bcrypt import Bcrypt #password encryption
import mysql.connector

# configuration

#load_dotenv()
app = Flask(__name__)
app.secret_key = "hello"    #seecret key required to use sessions
app.permanent_session_lifetime = timedelta(minutes=60)
url = os.getenv("DATABASE_URL") #database url
bcrypt = Bcrypt(app) #encryption object

#connection = mysql.connector.connect(host='', database='', user='', password='')


# database queries

CREATE_MESSAGES_TABLE_IF_NOT_EXIST = "CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, email TEXT, message TEXT);"

INSERT_MESSAGE = "INSERT INTO messages (email, message) VALUES (%s, %s);"

CREATE_ADMIN_TABLE_IF_NOT_EXIST = "CREATE TABLE IF NOT EXISTS admin (id SERIAL PRIMARY KEY, username TEXT, password TEXT);"

INSERT_ADMIN = "INSERT INTO admin (username, password) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM admin LIMIT 1);"

CHECK_LOGIN_AND_PASSWORD = "SELECT username, password FROM admin;"

GET_MESSAGES = "SELECT id,email,message FROM messages;"

COUNT_ROWS_IN_MESSAGES = "SELECT COUNT(email) FROM messages;"

CLEAR_ALL = "TRUNCATE TABLE messages;"

# routing

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about_me")
def about_me():
    return render_template("about_me.html")

@app.route("/offer")
def offer():
    return render_template("offer.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/hobby")
def hobby():
    return render_template("hobby.html")

@app.route("/contact", methods=["POST","GET"])
def contact():
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]
        connection = mysql.connector.connect(host='', database='', user='', password='')
        cursor = connection.cursor()
        cursor.execute(CREATE_MESSAGES_TABLE_IF_NOT_EXIST)
        connection.commit()
        cursor.execute(INSERT_MESSAGE, (email,message))
        connection.commit()
        cursor.close()
        connection.close()

        flash(f"Wysłano wiadomość z podpisem: {email}!", "info")
        return redirect(url_for("contact"))
    else:
        return render_template("contact.html")

# login, admin, logout

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["login"]
        not_hashed_pw = request.form["password"]
        password = bcrypt.generate_password_hash(not_hashed_pw).decode('utf-8') #hashing pw for db insert
        db_user_data = verify(user,password)
        is_pw_valid = bcrypt.check_password_hash(db_user_data[1], not_hashed_pw)
        if db_user_data[0]==user and is_pw_valid:
            session.permanent = True
            session["user"] = user
            session["password"] = password
            flash(f"Zalogowano jako {user}!", "info")
            return redirect(url_for("user"))
        else:
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Jesteś już zalogowany!", "info")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/logout", methods=["POST","GET"])
def logout():
    flash("Wylogowano!", "info")
    session.pop("user", None)
    session.pop("password", None)
    return redirect(url_for("home"))

@app.route("/user")
def user():
    if "user" in session and "password" in session:
        user = session["user"]
        password = session["password"]
        all_email_messages, rows_num = get_messages()
        return render_template("usr.html", user=user, data=all_email_messages, rows_num=rows_num)
    else:
        return redirect(url_for("login"))

@app.route("/login/verify", methods=["POST","GET"])
def verify(user,password):
    connection = mysql.connector.connect(host='', database='', user='', password='')
    cursor = connection.cursor()
    cursor.execute(CREATE_ADMIN_TABLE_IF_NOT_EXIST)
    connection.commit()
    cursor.execute(INSERT_ADMIN, (user,password))
    connection.commit()
    user='Se.Brzustowicz@gmail.com'
    cursor.execute(CHECK_LOGIN_AND_PASSWORD)
    db_user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    return db_user_data

@app.get("/user/get_messages")
def get_messages():
    connection = mysql.connector.connect(host='', database='', user='', password='')
    cursor = connection.cursor()
    cursor.execute(COUNT_ROWS_IN_MESSAGES)
    rows_num = cursor.fetchone()[0]
    cursor.execute(GET_MESSAGES)
    all_email_messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return all_email_messages, rows_num

@app.route("/user/clear", methods=["POST","GET"])
def clear():

    connection = mysql.connector.connect(host='', database='', user='', password='')
    cursor = connection.cursor()
    cursor.execute(CLEAR_ALL)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for("user"))

if __name__ == "__main__":
    app.run()
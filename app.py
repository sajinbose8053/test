import sqlite3
from flask import Flask, render_template, request, redirect, url_for ,session

app = Flask(__name__)
app.secret_key = "secret123"   # Required for session

# -----------------------------
# Create Database + Table
# -----------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    
    # Insert sample user
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
                   ("admin", "1234"))
    
    conn.commit()
    conn.close()

init_db()   #this is the data base that  was created by sql lite......
'''
# Simple demo credentials
USERNAME = "admin"
PASSWORD = "1234"
'''
# -------- Login --------
# -----------------------------
# Login Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")
# -----------------------------
# Home Route
# -----------------------------
@app.route("/home")
def home():
    if "username" in session:
        return render_template("home.html", user=session["username"])
    return redirect(url_for("login"))

# -----------------------------
# Logout Route
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)



'''
#--------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            return render_template("home.html")
        else:
            message = "Invalid Username or Password "

    return render_template("login.html", message=message)
#-----------------------------------------------------------
@app.route('/logout')
def logout():
    #session.pop('user', None)   # remove user from session  ---- LATER GONNA ADDED THIS LINE 

    return render_template("login.html")

#***********************************************************
if __name__ == "__main__":
    app.run(debug=True)
 #<!--sfdnijhbd-->
 '''
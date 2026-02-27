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
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT 
                    
    )
    """)
    
    # Insert sample user                                                                       \
    #cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",           |------this is the data thatis stored in database... 
     #             ("admin", "1234"))                                                          /
    
    conn.commit()
    conn.close()

init_db()   #this is the data base that  was created by sql lite......
'''
# Simple demo credentials
USERNAME = "admin"                   ----->this is  used to save name and passwd in variable whotout using data base
PASSWORD = "1234"
'''
#--------------------------------------------

@app.route("/")
def index():
    return redirect(url_for("register"))

#-----------------------------------
# rejesteration Route
#-----------------------------------
@app.route("/register",methods = ["GET","POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try :
            cursor.execute("""
            INSERT INTO users (username, email, phone, password)
            VALUES (?, ?, ?, ?)
            """, (username, email, phone, password))

            conn.commit()
            conn.close()

            return redirect(url_for("login"))
        except:
            error = "username or email already exist"
    return render_template("register.html", error=error)

# -----------------------------
# Login Route
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
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
             error =  "Invalid Username or Password"

    return render_template("login.html" , error=error)
# -----------------------------
# Home Route
# -----------------------------
@app.route("/home")
def home():
    if "username" in session:
        username = session['username']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT username, email, phone FROM users WHERE username=?", (username,))# '''(session["username"],)'''
        user = cursor.fetchone()

        conn.close()
        return render_template("home.html", user=user )
    else:
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
#added a new cmd

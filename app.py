from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple demo credentials
USERNAME = "admin"
PASSWORD = "1234"

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

@app.route("/logout", methods=["POST"])
def logout():
    return redirect(url_for("login"))

#***********************************************************
if __name__ == "__main__":
    app.run(debug=True)

    #<!--sfdnijhbd-->

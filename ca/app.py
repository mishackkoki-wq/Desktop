from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data for testing
users = {
    "student1@campus.ac.za": {"password": "12345", "name": "Thapelo"}
}

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email in users and users[email]["password"] == password:
            return redirect(url_for("dashboard", user=email))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard/<user>")
def dashboard(user):
    student = users[user]
    return render_template("dashboard.html", name=student["name"])

if __name__ == "__main__":
    app.run(debug=True)

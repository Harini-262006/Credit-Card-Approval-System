from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "creditcardsecretkey"

DATABASE = "database/credit.db"


# ==========================================
# Database Connection
# ==========================================

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# Login
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid Username or Password")

    return render_template("login.html")


# ==========================================
# Register
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (username, email, password)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful")

        return redirect(url_for("login"))

    return render_template("register.html")


# ==========================================
# Dashboard
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# ==========================================
# Prediction Page
# ==========================================

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if "username" not in session:
        return redirect(url_for("login"))

    prediction = None

    if request.method == "POST":

        income = float(request.form["income"])
        family = float(request.form["family"])
        children = float(request.form["children"])
        age = float(request.form["age"])
        employment = float(request.form["employment"])

        gender = request.form.get("gender", "")
        marital = request.form.get("marital", "")
        occupation = request.form.get("occupation", "")
        education = request.form.get("education", "")
        housing = request.form.get("housing", "")

        score = 0

        # Income
        if income >= 500000:
            score += 3
        elif income >= 300000:
            score += 2
        elif income >= 150000:
            score += 1

        # Age
        if 21 <= age <= 60:
            score += 2

        # Employment Experience
        if employment >= 5:
            score += 2
        elif employment >= 2:
            score += 1

        # Family Members
        if family <= 5:
            score += 1

        # Children
        if children <= 2:
            score += 1

        # Education
        if education in [
            "Graduate",
            "Post Graduate",
            "Professional Degree"
        ]:
            score += 2

        # Occupation
        if occupation in [
            "Engineer",
            "Software",
            "Government",
            "Doctor",
            "Manager",
            "Business"
        ]:
            score += 2

        # Housing
        if housing == "House / Apartment":
            score += 1

        # Marital Status
        if marital in ["Married", "Single"]:
            score += 1

        # Gender (optional demo rule)
        if gender in ["Male", "Female"]:
            score += 1

        # Final Decision
        if score >= 10:
            prediction = "Accepted"
        else:
            prediction = "Rejected"

        conn = get_connection()

        conn.execute("""
            INSERT INTO predictions
            (
                username,
                income,
                family,
                children,
                age,
                employment,
                result
            )
            VALUES(?,?,?,?,?,?,?)
        """,
        (
            session["username"],
            income,
            family,
            children,
            age,
            employment,
            prediction
        ))

        conn.commit()
        conn.close()

        return render_template(
            "predict.html",
            prediction=prediction
        )

    return render_template(
        "predict.html",
        prediction=prediction
    )
# ==========================================
# Prediction History
# ==========================================

@app.route("/history")
def history():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    records = conn.execute(
        """
        SELECT *
        FROM predictions
        WHERE username=?
        ORDER BY id DESC
        """,
        (session["username"],)
    ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        records=records
    )


# ==========================================
# User Profile
# ==========================================

@app.route("/profile")
def profile():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (session["username"],)
    ).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# ==========================================
# About Page
# ==========================================

@app.route("/about")
def about():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("about.html")


# ==========================================
# Contact Page
# ==========================================

@app.route("/contact")
def contact():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("contact.html")


# ==========================================
# Logout
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("home"))


# ==========================================
# Error Pages
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template("500.html"), 500


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    if not os.path.exists("database"):
        os.makedirs("database")

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
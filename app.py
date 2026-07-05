from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import pandas as pd
import joblib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import numpy as np

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "rising_waters_secret_key")

# ==========================
# LOAD MODEL & SCALER
# ==========================

MODEL_FILE = "floods.save"
SCALER_FILE = "transform.save"

model = None
scaler = None

if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)

if os.path.exists(SCALER_FILE):
    scaler = joblib.load(SCALER_FILE)

# ==========================
# DATABASE
# ==========================

DATABASE = "rising_waters.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL

    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        temp REAL,
        humidity REAL,
        cloud_cover REAL,
        annual REAL,
        jan_feb REAL,
        mar_may REAL,
        jun_sep REAL,
        oct_dec REAL,
        avgjune REAL,
        sub REAL,

        result TEXT,
        confidence REAL,
        created_at TEXT,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    conn.commit()
    conn.close()


init_db()

# ==========================
# HELPERS
# ==========================


def logged_in():
    return "user_id" in session


def login_required():

    if not logged_in():
        return redirect(url_for("login"))

    return None


# ==========================
# HOME
# ==========================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ==========================
# SIGNUP
# ==========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:

            flash("Passwords do not match", "danger")
            return redirect(url_for("signup"))

        conn = get_connection()
        cur = conn.cursor()

        user = cur.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user:

            conn.close()
            flash("Email already registered", "warning")
            return redirect(url_for("signup"))

        hashed = generate_password_hash(password)

        cur.execute("""
        INSERT INTO users(name,email,password)
        VALUES(?,?,?)
        """,
        (name,email,hashed))

        conn.commit()
        conn.close()

        flash("Registration Successful", "success")

        return redirect(url_for("login"))

    return render_template("signup.html")


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=get_connection()

        user=conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"]=user["id"]
            session["name"]=user["name"]
            session["email"]=user["email"]

            flash("Welcome back!","success")

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password","danger")

    return render_template("login.html")


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully","info")

    return redirect(url_for("index"))
# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    check = login_required()
    if check:
        return check

    conn = get_connection()

    total_predictions = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    flood_count = conn.execute(
        """
        SELECT COUNT(*) FROM predictions
        WHERE user_id=? AND result='Flood Risk'
        """,
        (session["user_id"],)
    ).fetchone()[0]

    safe_count = total_predictions - flood_count

    history = conn.execute("""
        SELECT *
        FROM predictions
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 5
    """,(session["user_id"],)).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_predictions=total_predictions,
        flood_count=flood_count,
        safe_count=safe_count,
        history=history
    )


# ==========================
# PROFILE
# ==========================

@app.route("/profile")
def profile():

    check = login_required()
    if check:
        return check

    conn = get_connection()

    total_predictions = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    flood_count = conn.execute(
        """
        SELECT COUNT(*)
        FROM predictions
        WHERE user_id=?
        AND result='Flood Risk'
        """,
        (session["user_id"],)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "profile.html",
        total_predictions=total_predictions,
        flood_count=flood_count
    )


# ==========================
# PREDICT
# ==========================

@app.route("/predict", methods=["GET", "POST"])
def predict():

    check = login_required()
    if check:
        return check

    if request.method == "GET":
        return render_template("predict.html")

    try:

        temp = float(request.form["temp"])
        humidity = float(request.form["humidity"])
        cloud_cover = float(request.form["cloud_cover"])
        annual = float(request.form["annual"])
        jan_feb = float(request.form["jan_feb"])
        mar_may = float(request.form["mar_may"])
        jun_sep = float(request.form["jun_sep"])
        oct_dec = float(request.form["oct_dec"])
        avgjune = float(request.form["avgjune"])
        sub = float(request.form["sub"])

        # Create DataFrame with the SAME column names as the dataset
        features = pd.DataFrame([{
            "Temp": temp,
            "Humidity": humidity,
            "Cloud Cover": cloud_cover,
            "ANNUAL": annual,
            "Jan-Feb": jan_feb,
            "Mar-May": mar_may,
            "Jun-Sep": jun_sep,
            "Oct-Dec": oct_dec,
            "avgjune": avgjune,
            "sub": sub
        }])

        if scaler is None or model is None:
            flash("Model not found. Train the model first.", "danger")
            return redirect(url_for("predict"))

        scaled = scaler.transform(features)

        prediction = model.predict(scaled)[0]
        confidence = float(model.predict_proba(scaled)[0].max()) * 100

        result = "Flood Risk" if prediction == 1 else "Safe"

        conn = get_connection()

        conn.execute("""
            INSERT INTO predictions (
                user_id,
                temp,
                humidity,
                cloud_cover,
                annual,
                jan_feb,
                mar_may,
                jun_sep,
                oct_dec,
                avgjune,
                sub,
                result,
                confidence,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            temp,
            humidity,
            cloud_cover,
            annual,
            jan_feb,
            mar_may,
            jun_sep,
            oct_dec,
            avgjune,
            sub,
            result,
            round(confidence, 2),
            datetime.now().strftime("%d-%m-%Y %H:%M")
        ))

        conn.commit()
        conn.close()

        if prediction == 1:
            return render_template(
                "chance.html",
                confidence=round(confidence, 2)
            )
        else:
            return render_template(
                "no_chance.html",
                confidence=round(confidence, 2)
            )

    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("predict"))
    # ==========================
# HISTORY
# ==========================

@app.route("/history")
def history():

    check = login_required()
    if check:
        return check

    conn = get_connection()

    history = conn.execute("""

    SELECT *
    FROM predictions

    WHERE user_id=?

    ORDER BY id DESC

    """,

    (session["user_id"],)

    ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=history
    )


# ==========================
# DELETE HISTORY
# ==========================

@app.route("/delete_history")
def delete_history():

    check = login_required()
    if check:
        return check

    conn = get_connection()

    conn.execute(

        "DELETE FROM predictions WHERE user_id=?",

        (session["user_id"],)

    )

    conn.commit()
    conn.close()

    flash(
        "Prediction history deleted successfully.",
        "success"
    )

    return redirect(url_for("history"))


# ==========================
# CONTEXT PROCESSOR
# ==========================

@app.context_processor
def inject_user():

    return dict(

        logged_in=("user_id" in session),

        username=session.get("name"),

        email=session.get("email")

    )


# ==========================
# ERROR HANDLERS
# ==========================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html"

    ),404


@app.errorhandler(500)
def internal_server(error):

    return render_template(

        "500.html"

    ),500


# ==========================
# RUN SERVER
# ==========================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )

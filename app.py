from flask import Flask, render_template, request, url_for, redirect, session
from models import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "seilaqualquercoisa"  

db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        userphone = request.form["userphone"]

        
        user = User(username=username, userphone=userphone)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))  

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        userphone = request.form["userphone"]

        # 🔹 Busca usuário combinando username e userphone
        user = User.query.filter_by(username=username, userphone=userphone).first()
        if user:
            session["user_id"] = user.id 
            return redirect(url_for("initial_user_page")) 
        else:
            return "Usuário ou telefone incorretos"

    
    return render_template("login.html")


@app.route("/initial_user_page")
def initial_user_page():
    if "user_id" not in session:  
        return redirect(url_for("login"))


    user = User.query.get(session["user_id"])
    return render_template("initial_user_page.html", user=user)


@app.route("/logout")
def logout():
    session.pop("user_id", None) 
    return redirect(url_for("login"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

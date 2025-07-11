from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()


# Flask Login Management
lg=LoginManager()
lg.init_app(app)

@lg.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        if User.query.filter_by(email=request.form.get('email')).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        hashsalt=generate_password_hash(
            password=request.form.get('password'),   # type: ignore
            method="pbkdf2:sha256", 
            salt_length=8
        )
        reg=User(
            email=request.form.get('email'),
            password=hashsalt,
            name=request.form.get('name')
        )
        db.session.add(reg)
        db.session.commit()
        login_user(reg)
        return redirect(url_for('secrets'))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=="POST":
        email1=request.form.get('email')
        password1=request.form.get('password')
        checkaccess=User.query.filter_by(email=email1).first()
        if not checkaccess:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(pwhash=checkaccess.password, password=password1):  # type: ignore
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(checkaccess)
            return redirect(url_for("secrets"))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

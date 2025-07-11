from wsgiref.validate import validator
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.app_context().push()
Bootstrap(app)

class Film(FlaskForm):
    rate = FloatField("Your Rating out of 10 e.g 7.6", validators=[DataRequired()])
    rev = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")

class Addfile(FlaskForm):
    name = StringField("Movie Title")
    subm = SubmitField("Add Movie")
# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MOVIES.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CREATE TABLE
class Movie(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=False)
    review = db.Column(db.String(255), unique=False, nullable=False)
    imgurl = db.Column(db.String(255), unique=False, nullable=False)

# db.create_all()

newmovie=Movie(
    title="Photo Tooth",
    year=2003,
    description="it already has everything you need to render your Quick Form. This is so that students don't just create a simple HTML form. If you've forgotten how to work with WTForms, you can go back a few lessons and review the content there or just use the documentation You don't need to change the code in edit.html",
    rating=8.1,
    ranking=8,
    review="You should be There is an edit button on the back of the movie card",
    imgurl="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)

# db.session.add(newmovie)
# db.session.commit()

@app.route("/")
def home():
    movies=db.session.query(Movie).all()
    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i
    db.session.commit()
    return render_template("index.html",allmovies=movies)

@app.route("/edit", methods=['POST','GET'])
def edit():
    modify = Film()
    bid = request.args.get('id')
    if modify.validate_on_submit():
        movieupdate = Movie.query.get(bid)
        movieupdate.rating = float(request.form['rate'])
        movieupdate.review = request.form['rev']
        db.session.commit()
        return redirect(url_for('home'))
    movieselected = Movie.query.get(bid)
    return render_template("edit.html",form=modify,movies=movieselected)

@app.route("/delete")
def delete():
    bid = request.args.get('id')
    moviedelete = Movie.query.get(bid)
    db.session.delete(moviedelete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=['POST','GET'])
def add():
    addm=Addfile()
    if addm.validate_on_submit():
        par = {
            "api_key":"eff06f2ba3d24de4a27955090c67585e",
            "query":request.form['name'],
            "language":"en-US"
        }
        res = requests.get(url="https://api.themoviedb.org/3/search/movie",params=par)
        res.raise_for_status()
        rest = res.json()['results']
        return render_template("select.html",coll=rest)
    return render_template("add.html",form2=addm)

@app.route("/select", methods=['POST','GET'])
def select():
    return render_template("select.html")

@app.route('/select/<int:id>')
def detial(id):
    par1 = {
        "api_key":"eff06f2ba3d24de4a27955090c67585e",
        "language":"en-US"
    }
    res1 = requests.get(url=f"https://api.themoviedb.org/3/movie/{id}",params=par1)
    res1.raise_for_status()
    rest1 = res1.json()
    print(rest1)
    newmovie1=Movie(
        title=rest1["title"],
        year=rest1["release_date"].split("-")[0],
        description=rest1["overview"],
        rating=rest1["vote_average"],
        ranking=8,
        review=rest1["tagline"],
        imgurl=f"https://api.themoviedb.org/3/movie{rest1['poster_path']}"
    )
    db.session.add(newmovie1)
    db.session.commit()
    return redirect(url_for("edit", id=newmovie1.id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

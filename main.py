from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask import session

# an instance of the Flask class we imported (that is our Web Server Gateway Interface) so that Flask knows where to
# look for templates and static files
app = Flask(__name__)
# Set the secret key to some random bytes.
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# identifier for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/gamedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# object of class SQLAlchemy contains an auxiliary function for the ORM operation
# (a programming technique in which a metadata descriptor is used to connect object code to a relational database. )
db = SQLAlchemy(app)


# database tables represented by models -- defining columns and their arguments
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ownerid = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.Integer, nullable=False)
    apples = db.Column(db.Integer, nullable=False)


# this commented function was only used once to create the tables
# @app.route('/initdb', methods=['GET'])
# def initdb():
#     with app.app_context():
#         db.create_all()
#     return 'The Db is Ready!'


# this function handle the results of GET and POST requests from the form in Login.html
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(login=username, password=password).first()  # find the user in db, if match
        if user:
            session['userId'] = user.id
            # returns game to client side
            return render_template("Game.html", name=user.fullname, scores=orderedTopScores(session['userId']))
        else:
            # User not found or incorrect password, Login page is rendered with an error message
            # User can then retry
            return render_template("LogIn.html", valid=True)
    else:
        # when page is first loaded it provides the Login page
        return render_template("LogIn.html")


# creates a list of the top 5 scores for the current user
def orderedTopScores(userId):
    return Games.query.filter_by(ownerid=userId).order_by(Games.apples.desc()).limit(5).all()


@app.route("/saveGame", methods=['POST'])
def saveGame():
    saveGameOnDB(request.form['apples'], request.form['times'], session['userId'])
    tops = orderedTopScores(session['userId'])
    return render_template("Game.html", scores=tops)  # gets passed scores so that it can be displayed in the Game.html


# it gets passed data from the game and the userId, then inserts it in the db games table
def saveGameOnDB(apples, time, userId):
    row = Games(ownerid=userId, apples=apples, time=time)
    db.session.add(row)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

handles = db.Table('handles',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('handle_id', db.Integer, db.ForeignKey('handle.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=True)
    teams = db.relationship('Team', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)
       
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handles = db.relationship('Handle', secondary=handles, backref=db.backref('teams', lazy='dynamic'))
    timestamp = db.Column(db.DateTime)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Team %r>' % (self.user)
        
class Handle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    cost = db.Column(db.Integer)
    datapoints = db.relationship('HandleData', backref='handle_author', lazy='dynamic')

    def __repr__(self):
        return '<Handle %r>' % (self.name)  

class HandleData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    handle = db.Column(db.Integer, db.ForeignKey('handle.id'))
    retweets = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<HandleData %r>' % (self.dataPt)          

@app.route('/')
def home():
    return render_template("./index.html")

@app.route('/getinfo', methods=["POST"])
def getinfo():
	'''
	This method returns the json data from
	a timeline from a user thingy
	'''
	pass

@app.route('/buytweeter',methods=["POST"])
def buytweeter():
	'''
	this method buys a tweeter 
	'''



if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, redirect, request, url_for, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy

import datetime as DT
import json

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
    password = db.Column(db.String(64), index=True)
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
        
    def get_points(self):
        return sum([handle.get_latest() for handle in self.handles])
        
class Handle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    cost = db.Column(db.Integer)
    datapoints = db.relationship('HandleData', backref='handle_author', lazy='dynamic')

    def __repr__(self):
        return '<Handle %r>' % (self.name)
        
    def get_latest(self):
        return sorted(self.datapoints, key=lambda x: x.timestamp)[-1]

class HandleData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    handle = db.Column(db.Integer, db.ForeignKey('handle.id'))
    retweets = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<HandleData %r>' % (self.dataPt) 

@app.route('/login',methods=["POST"])
def login():
    user = User.query.filter_by(username = request.args.get("username")).first()
    if user is None or request.args.get("password") != user.password:
        return redirect(url_for("home"))
    else:
        g.user = user
        return redirect(url_for("front_panel"))
        
@app.route('/signup',methods=["POST"])
def signup():
    user = User.query.filter_by(username = request.args.get("username")).first()
    if user is None:
        user = User(username = request.args.get("username"), password = request.args.get("password"))
        db.session.add(user)
        db.session.commit()
        g.user = user
        return redirect(url_for("front_panel"))
    else:
        return redirect(url_for("home"))

@app.route('/leaderboard')
def leaderboard():
    users = sorted([user for user in User.query.all() if len(user.teams) > 0], key=lambda user: user.teams[0].get_points())
    render_template('leaderboard.html', users=users)
    
@app.route('/team')
def team():
    if g.user is None:
        redirect(url_for('home'))
    
    if len(g.user.teams) == 0:
        handles = Handle.query.all()
        team = None
    else:
        team = g.user.teams[0]
        handles = None
        
    render_template('team.html', handles = handles, team = team)

@app.route('/createteam', methods=["POST"])
def create_team():

    if g.user.teams > 0:
        redirect(url_for('team'))
    
    handles=[]
    for checkbox in request.form.getlist('check'):
        handles.append(Handle.query.filter_by(name = checkbox.value).first())
    
    if sum([handle.cost for handle in handles]) <= 100:
        team = Team(user = g.user.id, handles = handles)

        db.session.add(team)
        db.session.commit()
    
        render_template('team.html', handles = handles, team = team)
    
    else:
        redirect(url_for('team'))
    
@app.route('/RTData')
def RTData():
    users = sorted([user for user in User.query.all() if len(user.teams) > 0], key=lambda user: user.teams[0].get_points())
    render_template('leaderboard.html', users=users)
    

@app.route('/')
def home():
	return render_template('index.html')

if __name__ == "__main__":
	app.run(debug=True)
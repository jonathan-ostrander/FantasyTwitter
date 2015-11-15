from flask import Flask, render_template, redirect, request, url_for, jsonify, g, session
from flask.ext.sqlalchemy import SQLAlchemy

import datetime as DT
import json

app = Flask(__name__, static_folder='static')
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
        return sorted(self.datapoints, key=lambda x: x.timestamp)[-1].retweets

class HandleData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    handle = db.Column(db.Integer, db.ForeignKey('handle.id'))
    retweets = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<HandleData %r>' % (self.handle)

@app.before_request
def load_access_token():

    if 'username' in session:
        username = session['username']
    else:
        username = None

    g.user = User.query.filter_by(username = username).first()

@app.route('/login')
def login():
    print request.args.get("username")
    user = User.query.filter_by(username = request.args.get("username")).first()
    print user
    if user is None or request.args.get("password") != user.password:
        return redirect(url_for("home"))
    else:
        session['username'] = user.username
        return redirect(url_for("leaderboard"))

@app.route('/signup')
def signup():
    user = User.query.filter_by(username = request.args.get("username")).first()
    if user is None:
        user = User(username = request.args.get("username"), password = request.args.get("password"))
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect(url_for("leaderboard"))
    else:
        return redirect(url_for("home"))

@app.route('/leaderboard')
def leaderboard():
    users = sorted([user for user in User.query.all() if len(user.teams.all()) > 0], key=lambda user: user.teams[0].get_points())
    costs = [sum([handle.cost for handle in user.teams[0].handles]) for user in users]
    users = [(users[i], costs[i]) for i in range(len(users))]
    return render_template('leaderboard.html', users=users)

@app.route('/team')
def team():
    if g.user is None:
        return redirect(url_for('home'))

    if len(g.user.teams.all()) == 0:
        handles = Handle.query.all()
        team = None
    else:
        team = g.user.teams[0]
        handles = None

    return render_template('team.html', handles = handles, team = team)

@app.route('/createteam')
def create_team():

    if len(g.user.teams.all()) > 0:
        return redirect(url_for('team'))

    handles=[]
    for checkbox in request.args.get('check').split("|"):
        handles.append(Handle.query.filter_by(name = checkbox).first())
    print handles
    print sum([handle.cost for handle in handles])
    if sum([handle.cost for handle in handles]) <= 100:
        team = Team(user = g.user.id, handles = handles)

        db.session.add(team)
        db.session.commit()

        return redirect(url_for('team'))

    else:
        return redirect(url_for('team'))

@app.route('/deleteteam')
def delete_team():
    if g.user and len(g.user.teams.all()) == 1:
        db.session.delete(g.user.teams[0])
        db.session.commit()

    return redirect(url_for('team'))

@app.route('/RTData')
def RTData():
    users = sorted([user for user in User.query.all() if len(user.teams) > 0], key=lambda user: user.teams[0].get_points())
    return render_template('leaderboard.html', users=users)


@app.route('/')
def home():
    if g.user is None:
        return render_template('index.html')
    else:
        return redirect(url_for('leaderboard'))

if __name__ == "__main__":
	app.run(debug=True)

from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

import tweet_get
import datetime as DT
from time import sleep
from multiprocessing import Pool
import multiprocessing
import json

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

short_time_read = True
_pool = None


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
        
        
#update database and stuff
def get_retweet_info(time, name, past, delta):
	'''
	arguments : int(seconds), String name
	returns boolean

	function will be called periodically by thread
	and will update the database from 
	'''
	past_date = DT.datetime.today() - DT.timedelta(days=1)
	return None

def write_to_db():
	handles = Handle.query.all()

	total_retweets = 0
	r = []
	for handle in handles:
		retweets = getReweets(handle.name)#get the retweets
		r.append(retweets)#add to a list for further analysis

		handledata = HandleData(retweets=retweets, handle=handle)#add to database
		db.session.add(handledata)
		db.session.commit()
		total_retweets += r[-1]#get the most recently added tweet

	average_retweets = total_retweets / float(len(handles))

	i = 0
	while i<len(handles):
		cost = (r[i]/average_retweets) * 100) / 5
		person = Handle.query.filter_by(name=handles[i])
		person.update().values(cost=cost)
		db.session.commit()
		i+=1

	return True
	



@app.route('/')
def home():
	return render_template('index.html')

if __name__ == "__main__":
	_pool = Pool(processes=1)
	try:
		p = multiprocessing.Process(target=write_to_db, args=())
		p.start()
		app.run(debug=True)
	except KeyboardInterrupt:
		_pool.close()
		_pool.join()

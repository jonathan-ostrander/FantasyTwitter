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

def get_info_raw(name, past, delta):
	'''
	return json about the user from the name
	'''

	last_week = DT.datetime.today() - DT.timedelta(days=past['days'],
												   hours=past['hours'],
												   minutes=past['minutes']
													)

	return_dict = {
		'name': name,
		'retweets': tweet_get.getRetweets(name, last_week, delta),
		'date_start':last_week,
		'date_end':last_week + DT.timedelta(days=delta['days'],
										   hours=delta['hours'],
										   minutes=delta['minutes']
											)
	}

	return return_dict

def write_to_db(time, x):
	past = {
		'days':1,
		'hours':0,
		'minutes':0
	}

	delta = {
		'days':0,
		'hours':23,
		'minutes':0
	}
	with open("./top100.json") as twit_users:
		json_data = json.load(twit_users)
		while True:
			for user in json_data:
				data = get_info_raw(user[1:], past, delta)
				print data['name'], data['retweets']
			sleep(time)         


if __name__ == "__main__":
	_pool = Pool(processes=1)
	try:
		p = multiprocessing.Process(target=write_to_db, args=(1,10))
		p.start()
		app.run(debug=True)
	except KeyboardInterrupt:
		_pool.close()
		_pool.join()

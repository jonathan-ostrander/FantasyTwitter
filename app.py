from flask import Flask, render_template, redirect, request, url_for, jsonify
import tweet_get
import datetime as DT
from time import sleep
from multiprocessing import Pool
import multiprocessing
import json

app = Flask(__name__)
short_time_read = True
_pool = None


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


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/getinfo/<name>')
def getinfo(name):
	'''
	return json about the user from the name
	'''

	last_week = DT.datetime.today() - DT.timedelta(days=1)
	delta = 7

	return_dict = {
		'name': name,
		'retweets': tweet_get.getRetweets(name, last_week, delta),
		'date_start':last_week,
		'date_end':last_week + DT.timedelta(days=delta)
	}

	return jsonify(return_dict)

@app.route("/get/<int:x>")
def do_square(x):

	#f = _pool.apply_async(square,[x])
	#r = f.get(timeout=2)
	#return 'Result is %d'%r
	return jsonify({'yay':69})

@app.route('/buytweeter',methods=["POST"])
def buytweeter():
	'''
	this method buys a tweeter 
	'''
	pass


if __name__ == "__main__":
	_pool = Pool(processes=1)
	try:
		p = multiprocessing.Process(target=write_to_db, args=(1,10))
		p.start()
		app.run(debug=True)
	except KeyboardInterrupt:
		_pool.close()
		_pool.join()
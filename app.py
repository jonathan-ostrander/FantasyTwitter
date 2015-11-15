from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


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
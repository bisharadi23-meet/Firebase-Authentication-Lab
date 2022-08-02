from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyB1Kr9qRj5pbaQ_I5pN6j6_v_fHAy73PQs",
  "authDomain": "firstbase-ea13c.firebaseapp.com",
  "projectId": "firstbase-ea13c",
  "storageBucket": "firstbase-ea13c.appspot.com",
  "messagingSenderId": "461385299351",
  "appId": "1:461385299351:web:913cea040ee6b63ab2c0d2",
  "measurementId": "G-LQWGWSBHPY",
  "databaseURL":"https://firstbase-ea13c-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			return error
	else:
		return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		# try:
		email = request.form['email']
		password = request.form['password']
		login_session['user'] = auth.create_user_with_email_and_password(email, password)
		user = {"email":request.form["email"], "password":request.form["password"] ,"full_name":request.form["full_name"] ,"username":request.form["username"] ,"bio":request.form["bio"]}
		db.child("Users").child(login_session['user']['localId']).set(user)
		return redirect(url_for('add_tweet'))
		# except:
		#    error = "Authentication failed"
		   # return (error)
	else:
		return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		tweet = {"title" : request.form['title'], "text" : request.form['text'], "uid" : login_session['user']['localId']}
		db.child("tweet").push(tweet)
	return render_template("add_tweet.html")
	
@app.route("/all_tweet", methods=['GET', 'POST'])
def all_tweet():
	tweets = db.child("tweet").get().val()
	return render_template("all_tweets.html", tweets = tweets)

if __name__ == '__main__':
	app.run(debug=True)
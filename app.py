from flask import Flask,render_template,url_for,request,jsonify, redirect,session
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import pickle
import firebase_admin
from firebase_admin import credentials, auth 

cred = credentials.Certificate(r"C:\MLproject\rain-pred-995a7-firebase-adminsdk-pmlxr-5af299bf71.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__, template_folder="templates")
model = pickle.load(open("model_first.pkl", "rb"))
print("Model Loaded")

#sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(email=email, password=password)
            if user:
                return redirect(url_for('login'))
        except Exception as e:
            return render_template('signup.html', error='User already exist')
    return render_template('signup.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            if user:
                auth_user = auth.sign_in_with_email_and_password(email, password)
                session['user'] = auth_user['idToken']
                return redirect(url_for('/'))
        except Exception as e:
            return render_template('index.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/')
def home():
	return render_template("index.html")

@app.route("/predict",methods=['GET', 'POST'])
@cross_origin()
def predict():
	if request.method == "POST":
		# MinTemp
		minTemp = float(request.form['mintemp'])
		# MaxTemp
		maxTemp = float(request.form['maxtemp'])
		# Sunshine
		sunshine = float(request.form['sunshine'])
		# Wind Gust Speed
		windGustSpeed = float(request.form['windgustspeed'])
		# Humidity 9am
		humidity9am = float(request.form['humidity9am'])
		# Humidity 3pm
		humidity3pm = float(request.form['humidity3pm'])
		# Pressure 9am
		pressure9am = float(request.form['pressure9am'])
		# Pressure 3pm
		pressure3pm = float(request.form['pressure3pm'])
		#Temperature 9am
		temp9am = float(request.form['temp9am'])
		# Temperature 3pm
		temp3pm = float(request.form['temp3pm'])
		# Cloud 9am
		cloud9am = float(request.form['cloud9am'])
		# Cloud 3pm
		cloud3pm = float(request.form['cloud3pm'])
		# Rain Today
		rainToday = float(request.form['raintoday'])

		input_list = [ minTemp , maxTemp , sunshine , windGustSpeed , humidity9am , humidity3pm , 
               pressure9am , pressure3pm, temp9am , temp3pm , cloud9am , cloud3pm , rainToday ]
  
		pred = model.predict([input_list])
		output = pred 
		if output == 0:
			return render_template("sunny.html")
		else:
			return render_template("rainy.html")
	return render_template("predict.html")

if __name__=='__main__':
	app.run(debug=True)

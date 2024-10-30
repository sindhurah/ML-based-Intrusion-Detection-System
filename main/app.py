from flask import Flask, render_template, url_for, request, jsonify, session
import sqlite3
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from keras.models import load_model
from feature import FeatureExtraction
import os
model = load_model('model/model.h5')


file = open("model/model.pkl","rb")
gbc = pickle.load(file)
file.close()


connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

app = Flask(__name__)
app.secret_key = os.urandom(24)

def getData():
    while True:
        try:
            data = client_socket.recv(1024)
            break
        except:
            print("something went wrong")
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            session['user'] = result
            return render_template('userlog.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')

@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/get_data')
def get_data():
     data = getData()
     data = data.decode()
     print(data)

     obj = FeatureExtraction(data)
     x = np.array(obj.getFeaturesList()).reshape(1,30) 

     y_pred =gbc.predict(x)[0]
     y_pro_phishing = gbc.predict_proba(x)[0,0]
     y_pro_non_phishing = gbc.predict_proba(x)[0,1]
     perc = y_pro_phishing*100

     return jsonify([data, perc])
     
@app.route('/safe')
def safe():
    d = 'na'
    client_socket.sendall(d.encode())
    return render_template('userlog.html', sms="your data is safe")

@app.route('/Cancel')
def Cancel():
    d = 'na'
    client_socket.sendall(d.encode())
    return render_template('userlog.html', sms="your data is safe")

@app.route('/unsafe')
def unsafe():
    d = list(session['user'])
    print(d)
    data = 'name : {}, password : {}, mobile : {}, email : {}'.format(d[0], d[1], d[2], d[3])
    client_socket.sendall(data.encode())
    return render_template('userlog.html', sms="your data accessed by introdure")

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    import socket
    import os
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.103', 8000)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server is running and listening for connections...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    app.run(debug=True, use_reloader=False)

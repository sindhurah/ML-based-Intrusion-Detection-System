from flask import Flask, render_template, url_for, request, jsonify
import sqlite3
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from keras.models import load_model
# from feature import 
from feature import FeatureExtraction
model = load_model('model/model.h5')


file = open("model/model.pkl","rb")
gbc = pickle.load(file)
file.close()


connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

app = Flask(__name__)


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

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('userlog.html')

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

@app.route('/Send', methods=['GET', 'POST'])
def Send():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        Link = request.form['url']

        try:
            # Send the image data to the server
            client_socket.sendall(Link.encode())

            while True:
                try:
                    data = client_socket.recv(1024)
                    data = data.decode()
                    print(data)
                    break
                except:
                    print('something went wrong')
                return data
            if data == 'na':
                return render_template('userlog.html', msg="data not recieved")
            else:
                return render_template('userlog.html', data=data)
        except Exception as e:
            print(e)
            return render_template('userlog.html', msg="Can not send link")
    return render_template('userlog.html')
    
@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    import socket
    
    # Define the server's IP address and port
    SERVER_IP = '172.20.10.4'  # Replace with your server's IP address 
    SERVER_PORT = 8000  # Replace with your server's port

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to server.")
    app.run(debug=True, use_reloader=False)

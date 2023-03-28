from flask import Flask, render_template, request
import mysql.connector
import boto3
import os

os.environ['AWS_PROFILE'] = "default"
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
#from flask.ext.mysql import MySQL

#from werkzeug import generate_password_hash, check_password_hash


import json

app = Flask(__name__)
mydb = mysql.connector.connect(
  host="db-hungai.cqv94rykczmh.us-east-1.rds.amazonaws.com",
  user="admin",
  password="kieuhung123",
  database='users'
)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
        file = request.files['file']
        print(file)
        s3 = boto3.client('s3')
        # Upload a new file
        #data = open('test.jpg', 'rb')
        file = request.files['file']
        s3.Bucket('image-hung-001').put_object(Key=file.filename, Body=file)
        return json.dumps({'html':'<span>Successfully upload avatar</span>'})

@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI 
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values 
    if _name and _email and _password:
        mycursor = mydb.cursor()
        sql = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
        val = (_name, _password, _email)
        mycursor.execute(sql, val)
        mydb.commit()
        return json.dumps({'html':'<span>Successfully register users</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
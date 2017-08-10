
from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "ThisIsSecretadfasdfasdf!"

mysql = MySQLConnector(app,'email-validation')

@app.route('/')
def index():
    query = "SELECT email, DATE_FORMAT(created_at,'%M %d %Y') FROM emails"       # define your query, make sure you use the DATE_FORMAT stuff in your key 
    emails = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', email_list = emails)



@app.route('/email_validate', methods=['POST'])
def validate():
    input_email = request.form['email']
    email_query = "SELECT * FROM emails WHERE email = :email_id"
    query_data = {'email_id': input_email}
    stored_email = mysql.query_db(email_query, query_data)
    # print stored_email[0]['email']
    if not EMAIL_REGEX.match(input_email):
        flash("Email must be a valid email")
    elif stored_email:
        flash("Email already exists!")
    else:
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email1, NOW(), NOW())"
        # We'll then create a dictionary of data from the POST data received.
        data = {
                'email1': request.form['email']
            }
        # Run query, with dictionary values injected into the query.
        mysql.query_db(query, data)
        flash("This email address you entered " + input_email + " is a valid email address. Thank you!")
        return redirect('/success')
    return redirect('/')

@app.route('/success')
def success():
    query = "SELECT email, DATE_FORMAT(created_at,'%M %d %Y') FROM emails"       # define your query, make sure you use the DATE_FORMAT stuff in your key 
    emails = mysql.query_db(query)

    return render_template('success.html', email_list = emails)

app.run(debug=True)
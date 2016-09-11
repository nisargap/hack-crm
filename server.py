'''
Author: Nisarga Patel
Date Created: September 9, 2016

'''
from flask import Flask, redirect, url_for, request, Response, render_template, jsonify
from functools import wraps
from pymongo import MongoClient
import json
import config
from bson import ObjectId
import nexmo
from jsonschema import validate
import smtplib

import os
import binascii
import schemas
import datetime
app = Flask(__name__)

nexmo_client = nexmo.Client(key=config.creds["nexmo_key"], secret=config.creds["nexmo_secret"])

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == "admin" and password == "secret"

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Establish a connection to the Mongo Client
client = MongoClient()

# Connect to the HackCRM database
db = client.hack_crm_db


@app.route("/send_text", methods=['POST'])
def send_text():

	try:

		client_data = json.loads(request.data)

		response = nexmo_client.send_message({'from': config.creds["nexmo_from"], 'to': '1' + client_data['to'], 'text': client_data['msg']})

		return jsonify({'success' : 1})
	
	except Exception as e:

		print(e)

		return jsonify({'success' : 0})

'''
Params
to
subject
msg

'''
@app.route("/send_email", methods=['POST'])
def send_email():

	try:
		gmail_username = config.creds["email"]
		gmail_password = config.creds["password"]

		smtpserver = smtplib.SMTP("smtp.gmail.com",587)

		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo
		smtpserver.login(gmail_username, gmail_password)

		client_data = json.loads(request.data)

		header = 'To:' + client_data["to"] + '\n' + 'From: ' + gmail_username + '\n' + 'Subject:'+ client_data["subject"] + '\n'

		msg = header + client_data["msg"]

		smtpserver.sendmail(gmail_username, client_data["to"], msg)

		smtpserver.close()

		return jsonify({"success" : 1})

	except Exception as e:

		print(e)
		return jsonify({"success" : 0})



@app.route("/")
def hello():

    return "Hello World!"


'''

Add a record which is distinguised by the company name,
for example, if John Smith works at Some Company, and has
an email johnsmith@somecompany.com a record will be added to MongoDB
with fields:
	Name
	Company
	Email
	Phone Number (Optional)

'''

@app.route("/delete_contact/<email>")
def delete_contact(email):

	result = db.company_contacts.delete_one({'email': email})

	return jsonify({'deleted' : result.deleted_count })

@app.route("/add_contact", methods = ['POST'])
@requires_auth
def add_contact():

	contacts_table = db.company_contacts

	client_data = json.loads(request.data)

	contact_obj = { "name" : client_data['name'],

		"company" : client_data['company'],

		"email" : client_data['email'],

		"phone" : client_data['phone'],

		"datetime" : str(datetime.datetime.utcnow()),

	}

	if not client_data["address"] == "" :

		contact_obj["address"] = client_data["address"]

	if not client_data["profile_img"] == "" :

		contact_obj["profile_img"] = client_data["profile_img"]

	try:

		# validate the contact object
		validate(contact_obj, schemas.contact)

		contacts_table.insert_one(contact_obj)

		return jsonify({"success" : 1})

	except Exception as e:
		
		return jsonify({"error" : str(e), "success" : 0})


@app.route("/get_contacts")
def get_contacts():

	json_docs = []
	cursor = list(db.company_contacts.find().sort("name"))

	return JSONEncoder().encode(cursor)
'''
This is the view to interact with the contact addition controller
'''
@app.route("/add_contact")
def add_contact_view():

	return render_template('add_contact.html')

'''
This is the view to interact with the contact addition controller
'''
@app.route("/view_contacts")
def view_contacts():

	return render_template('view_contacts.html')


if __name__ == "__main__":
    app.run(debug=True)
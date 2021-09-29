import os
import re

from cs50 import SQL
from datetime import date, datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from flask_paginate import Pagination, get_page_args
from flask_sqlalchemy import Pagination
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure application
app = Flask(__name__)

# Ensure that all mail information is loaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///eatwhat.db")

@app.route("/about", methods=["GET"])
def about():
    """Show page explaining the app's purpose"""
    # Display contact form
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Display contact form for submission"""
    if request.method == "GET":
        # Display contact form
        return render_template("contact.html")
    else:
        # Assign all user's inputs to variables
        address = request.form.get("email")
        name = request.form.get("name")
        subject = request.form.get("subject")
        content = request.form.get("content")

        # Ensure user entered email
        if not address:
            return render_template("error.html", error = 'You did not enter an email address.')
        # Ensure email has nominal length
        if not len(address) >= 10 or not len(address) <= 75:
            return render_template("error.html", error = 'Please enter an email address with a valid length')
        # Ensure user entered their name
        if not name:
            return render_template("error.html", error = 'You did not enter your name.')
        # Ensure name has nominal length
        if not len(name) >= 2 or not len(name) <= 50:
            return render_template("error.html", error = 'The name you entered was an invalid length.')
        # Ensure user entered a subject
        if not subject:
            return render_template("error.html", error = 'You did not enter a subject for your message.')
        # Ensure subject line has nominal length
        if not len(subject) >= 20 or not len(subject) <= 100:
            return render_template("error.html", error = 'Your subject should be 10-30 characters long.')
        # Ensure user entered a message
        if not content:
            return render_template("error.html", error = 'You did not enter any message.')
        # Ensure content has nominal length
        if not len(content) >= 100 or not len(content) <= 1500:
            return render_template("error.html", error = 'Your message should be 100-1500 characters long.')

        # Create subject line for email
        raw_msg = f'EatWhat contact request. {name}: "{subject}"'
        # Initialize time for email time stamp
        time = str(datetime.utcnow().time())[:8]

        # Create message, including body formatted in HTML
        message = Message(raw_msg, sender=os.getenv("MAIL_DEFAULT_SENDER"), recipients=["zachariahjfrank@gmail.com"])
        message.body = f'Hello Zach, You have received an email from {name} on {date.today()} at {datetime.utcnow().time()} UTC. The subject is "{subject}." "{content}" In order to respond to this inquiry, please email {address}. This was an automatic message from EatWhat.app'
        message.html = f'Hello Zach, <br><br>You have received an email from <i>{name}</i> on {date.today()} at {time} UTC. <br><br>The subject is <b>"{subject}."</b> Content below:<br><i>"{content}"</i> <br><br>In order to respond to this inquiry, please email {address}. <br><br><i>This was an automatic message from EatWhat.app<i>'

        # Send message
        mail.send(message)

        # Notify user message successfully sent
        return render_template("contactsuccess.html")

# def get_choices(offset=0, per_page=5):

#     return choices[offset: offset + per_page]

@app.route("/", methods=["GET", "POST"])
def index():
    """Main web app to find and choose foods"""
    flavorinfo = ['not set', 'not set']

    if request.method == "GET":
        # Display form to find food
        return render_template("choose.html")
    else:
        # Choose 2 or 3 flavors only
        flavor_choices = []
        flavor = request.form.getlist('flavor')

        if len(flavor) > 3 or len(flavor) < 1:
            return render_template("error.html", error = 'Please choose from 1 - 3 flavors.')
        else:
            flavor_choices = flavor

        # Temp variable for error checking
        flavorinfo = flavor_choices

        # Initialize variables
        distance = 'not set'
        time = request.form.get('time')

        # Ensure user enters time
        if not time:
            return render_template("error.html", error = 'Please choose when you will eat.')

        # Convert time selection to distance in search query
        if time == "upto30":
            distance = '5+kilometers'
        elif time == "from1-2":
            distance = '10+kilometers'
        else:
            distance = '20+kilometers'

        hardness = request.form.get('hardness')

        # Ensure user chooses hardness
        if not hardness:
            return render_template("error.html", error = 'Please choose a solid or soft food- or any.')
        else:
            # Set variable for use with SQL
            if hardness == 'solid':
                hardness = 'solid'
            elif hardness == 'soft':
                hardness = 'soft'
            else:
                hardness = 'any'

        temp = request.form.get('heat')

        # Ensure user enters temperature
        if not temp:
            return render_template("error.html", error = 'Please choose between hot and cold- or both.')
        else:
            # Set variable for use with SQL
            if temp == 'hot':
                temp = 'hot'
            elif temp == 'cold':
                temp == 'cold'
            else:
                temp = 'any'

        address = request.form.get('address')
        city = request.form.get('city')

        # Ensure user enters temperature
        if not address:
            return render_template("error.html", error = 'Please enter an address.')
        # Ensure address is nominal length
        if not len(address) >= 10 or not len(address) <= 50:
            return render_template("error.html", error = 'Your address should be 10 - 50 characters long.')

        # Ensure user enters temperature
        if not city:
            return render_template("error.html", error = 'Please enter any city.')
        # Ensure city name is nominal length
        if not len(city) >= 3 or not len(city) <= 50:
            return render_template("error.html", error = 'The city name should be 3 - 50 characters long.')

        if len(flavor_choices) == 1:
            # Query for that 1 taste
            if temp == 'any':
                if hardness == 'any':
                     # 1 flavor- only flavor
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ?", '%%'+flavor_choices[0]+'%%')
                else:
                    # 1 flavor + hardness
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND hardness = ?", '%%'+flavor_choices[0]+'%%', hardness)
            else:
                # 1 flavor + temp
                if hardness == 'any':
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND temp = ?", '%%'+flavor_choices[0]+'%%', temp)
                else:
                    # 1 flavor + temp + hardness
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND hardness = ? AND temp = ?", '%%'+flavor_choices[0]+'%%', hardness, temp)
        elif len(flavor_choices) == 2:
            # Query for both tastes
            if temp == 'any':
                if hardness == 'any':
                    # 2 flavors - only flavors
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%')
                else:
                    # 2 flavors + hardness
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ? AND hardness = ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%', hardness)
            else:
                # 2 flavors + temp
                if hardness == 'any':
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ? AND temp = ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%', temp)
                else:
                    # 2 flavors + hardness + temp
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ? AND hardness = ? AND temp = ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%', hardness, temp)
        else:
            # Query for three tastes
            if temp == 'any':
                if hardness == 'any':
                    # 3 flavors - flavors only
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ? AND tastes LIKE ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%', '%%'+flavor_choices[2]+'%%')
                else:
                    # 3 flavors + hardness
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ? AND tastes LIKE ? AND hardness = ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%', '%%'+flavor_choices[2]+'%%', hardness)
            else:
                # 3 flavors + temp
                if hardness == 'any':
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ? AND tastes LIKE ? AND temp = ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%', '%%'+flavor_choices[2]+'%%', temp)
                else:
                    # 3 flavors + hardness + temp
                    choices = db.execute("SELECT * FROM foods WHERE tastes LIKE ? AND tastes LIKE ? AND tastes LIKE ? AND hardness = ?  AND temp = ?", '%%'+flavor_choices[0]+'%%', '%%'+flavor_choices[1]+'%%', '%%'+flavor_choices[2]+'%%', hardness, temp)

        # Initialize list for list of dicts to append to
        results = []

        # Loop through queries and adapt information for display
        for each in choices:
            # Initialize name for below
            name = each['name']
            # Format address, city and food name so can be added to a URL for a Google query
            link_add = re.sub(' ', '+', address.strip().lower())
            link_city = re.sub(' ', '+', city.strip().lower())
            link_name = re.sub(' ', '+', name.strip().lower())
            # Create a temporary dictionary with update inputs and insert into list "results"
            tmp_dict = {'name':name, 'country':each['country'], 'tastes':each['tastes'], 'contains':each['ingredients'], 'description':each['description'], 'image':each['image'], 'link':f'https://www.google.com/maps/search/{link_name}+within+{distance}+of+{link_add}+{link_city}/'}
            results.append(tmp_dict)

        choices = results

        # If there are no results, notify user
        if len(results) == 0:
            return render_template("noresults.html", choices=choices, flavorinfo=flavorinfo)
        else:
            return render_template("options.html", choices=choices)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template('error.html', error=(e.name))


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
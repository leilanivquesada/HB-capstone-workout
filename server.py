import json
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import json
from jinja2 import StrictUndefined

from pprint import pformat, pprint
import os
import requests

# url = 'https://wger.de/api/v2/....'
# data = '{"key": "value"}'
# headers = {'Accept': 'application/json',
#            'Authorization': 'Token 12345...'}

# r = requests.patch(url=url, data=data, headers=headers)



# app = Flask(__name__)
# app.secret_key = 'SECRETSECRETSECRET'


# API_KEY = os.environ['TICKETMASTER_KEY']


# @app.route('/')
# def homepage():
#     """Show homepage."""

#     return render_template('homepage.html')


# @app.route('/afterparty')
# def show_afterparty_form():
#     """Show event search form"""

#     return render_template('search-form.html')


# @app.route('/afterparty/search')
# def find_afterparties():
#     """Search for afterparties on Eventbrite"""

#     keyword = request.args.get('keyword', '')
#     postalcode = request.args.get('zipcode', '')
#     radius = request.args.get('radius', '')
#     unit = request.args.get('unit', '')
#     sort = request.args.get('sort', '')

#     url = 'https://app.ticketmaster.com/discovery/v2/events'
#     payload = {'apikey': API_KEY,
#                'keyword': keyword,
#                'postalCode': postalcode,
#                'radius': radius,
#                'unit': unit,
#                'sort': sort}

#     response = requests.get(url, params=payload)
#     data = response.json()

#     if '_embedded' in data:
#         events = data['_embedded']['events']
#     else:
#         events = []

#     return render_template('search-results.html',
#                            pformat=pformat,
#                            data=data,
#                            results=events)


# @app.route('/event/<id>')
# def get_event_details(id):
#     """View the details of an event."""

#     url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
#     payload = {'apikey': API_KEY}

#     response = requests.get(url, params=payload)
#     event = response.json()

#     if '_embedded' in event:
#         venues = event['_embedded']['venues']
#     else:
#         venues = []

#     return render_template('event-details.html',
#                            event=event,
#                            venues=venues)



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

# @app.route('/')
# def homepage():
    
#     return render_template('homepage.html')

# @app.route('/movies')
# def all_movies():
#     """View all movies"""
    
#     movies = crud.get_movies()
#     return render_template("all_movies.html",movies=movies)

# @app.route('/movies/<movie_id>')
# def show_movie(movie_id):
#     """Show details on a particular movie."""
#     movie = crud.get_movie_by_id(movie_id)
#     return render_template("movie_details.html", movie=movie)


# @app.route('/users')
# def all_users():
#     """"View all users"""
#     users = crud.get_users()
#     return render_template("all_users.html",users=users)

# #TODO for some reason would not route to USERS, so changed to user. unsure what is causing this
# @app.route('/user/<user_id>')
# def show_users(user_id):
#     """Show details on a particular user"""
#     user = crud.get_user_by_id(user_id)
#     return render_template("user_details.html",user=user)
    


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

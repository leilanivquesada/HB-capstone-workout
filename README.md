## Workout Planner App

This is a tool for planning and tracking strength building workouts. 

A user can log in to the site, schedule workouts, plan exercise routine based on desired muscle group focus, and log reps, weights and weight unit for each exercise set. In addition, a user can view their previously scheduled and recorded workouts. 

### Installation
Requires PostgreSQL
createdb users
git clone this repository

### Get your own API keys!
NewsAPI: https://newsapi.org/ 

Wger Workout Manager: https://wger.de/en/software/api

### Tech Stack
Python
SQLAlchemy
PostgreSQL
flask
jinja2
JavaScipt
Ajax
Bootstrap
HTML
CSS

### Features
The user dashboard features a graph that dynamically generates based on the user's exercise history. A user may select an exercise that they have previously scheduled, generating a line chart visualizing their strength progression over time.

The dashboard includes 3 cards for the most recent health and fitness news from NewsAPI.

The dashboard includes 1 random inspirational quote from FreeCodeCamp's inspirational quote API. A key is not needed to make a call to this API.


### For Version 2.0
Additional charts: more data visualization of user progress; a github-style grid to capture days worked out vs days not, for example. Additional formatting to existing chart to be even more dynamic. 

Additional User Control: add user ability to create and select their own exercises. This would require a separate table in the application model. Currently, exercises on the web application are called from the WGER Workout Manager API and are generally limited to strength training exercises. 

User Social Network: ability for users to add friends from Users. Ability for users to share workouts and exercises. 

Password Hashing: passwords will be hashed before saving. 

Images: The project could use more images and videos, to support informing the user how to perform the different exercises, for example.

Single Page Application: 

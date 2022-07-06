## Workout Planner App

This is a tool for planning and tracking strength building workouts. 

A user can log in to the site, schedule workouts, plan exercise routine based on desired muscle group focus, and log reps, weights and weight unit for each exercise set. In addition, a user can view their previously scheduled and recorded workouts. 

### Installation
<ul>
  <li>$virtualenv env</li>
  <li>$source env/bin/activate</li>
  <li>$pip3 install -r requirements</li>
  <li>Get your own API keys for APIs referenced below and add them to your own secrets.sh file</li>
  <li>$source secrets.sh</li>
  <li>$createdb users</li>
  <li>$python3 server.py</li>
</ul>

### Get your own API keys!
NewsAPI: https://newsapi.org/ <br>
Wger Workout Manager: https://wger.de/en/software/api

### Tech Stack
Python | 
SQLAlchemy | 
PostgreSQL |
flask |
jinja2 |
JavaScipt |
Ajax |
Bootstrap |
HTML |
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

![Screen Shot 2022-07-05 at 11 08 55 PM](https://user-images.githubusercontent.com/62270422/177480895-d8030e42-d221-41a9-84fc-d6b7c55a9e91.png)
![Screen Shot 2022-07-05 at 11 09 35 PM](https://user-images.githubusercontent.com/62270422/177480927-e7b83bb9-a253-4c28-86f8-7a0083fd8987.png)
![Screen Shot 2022-07-05 at 11 12 02 PM](https://user-images.githubusercontent.com/62270422/177481139-cbe71ec0-2ab8-478f-9d72-412e3ca4f3b7.png)
![Screen Shot 2022-07-05 at 11 12 46 PM](https://user-images.githubusercontent.com/62270422/177481259-bb8673e3-decf-484c-bc6c-f657c633e102.png)
![Screen Shot 2022-07-05 at 11 13 23 PM](https://user-images.githubusercontent.com/62270422/177481354-bf3a331f-aebf-4367-8ea4-3d11e2a8b7b6.png)
![Screen Shot 2022-07-05 at 11 13 35 PM](https://user-images.githubusercontent.com/62270422/177481378-09f5f7fe-e952-485b-8058-f32d6fda7fc3.png)

404 Not Found Error Screen:
![Screen Shot 2022-07-05 at 11 14 55 PM](https://user-images.githubusercontent.com/62270422/177481588-32bde1a9-b2de-4615-803d-15320929c53c.png)

500 Internal Error Screen:
![Screen Shot 2022-07-05 at 11 11 01 PM](https://user-images.githubusercontent.com/62270422/177481022-ec8c1e1b-d13a-4c3e-a295-8484368b8684.png)



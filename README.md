# GagaDict
-----

## Introduction
GagaDict(or Gaga Dictionary) is a web-based personal dictionary system. It was designed to help language learner to effectively manage and remember words. It was built for the purpose of:
* get/add/delete/revise words to the dictionary.
* generate questions from the stored words. 
* register answers of the users to the generated questions. 
* store the answer records. 


## Table of contents
  - [Overview](#Overview)
  - [Table of contents](#table-of-contents)
  - [Teck Stack](#Tech-Stack-(Dependencies))
  - [Project Structure](#project-structure)
  - [How to use the application](#how-to-use-the-application)
  - [Screenshot of the application](#screenshot-of-the-application)
  - [Licensing, Authors, Acknowledgements](#licensing-authors-acknowledgements)

## Overview
### Database
The application use PostgreSQL database in the backend. Through the defined API:
* A **normal user** can:
  * get/delete/post/patch words to the dictionary.
  * get/post answers to the answer record.
* An **Admin user** can:
  * get an overview of users and users records.
  * delete a user. 

### Inloggning and user management
The application uses **Auth0** to manage the inloggning. A new user can visit the following url to register as a new user. 
```
https://hellogaga.eu.auth0.com/authorize?audience=dictionary&response_type=token&client_id=iK5BxRKuFhZfddNMqKxERu9Tjdg95gsL&redirect_uri=https://gagadict.herokuapp.com
```

### Roles and Permission
The application has two roles:
* A normal user, with the following permissions:
  * get:words
  * patch:words
  * delete:words
  * post:words
  * get:questions
  * post:answers
  * get:answers
* An Admin user is also a normal user, on top of it, this role has additional permission of managing users:
  * get:uers
  * delete:users

### Hosting
The application is hosted at `https://gagadict.herokuapp.com`

### Brief introduction of API endpoints and required permission. 
* Endpoints for a normal user:
  * Get /, No permission needed
  * GET /categories, No permission needed. 
  * GET /words, Permission needed: 'get:words'
  * GET /words/<word_id>, Permission needed: 'get:words'
  * DELETE /words/<word_id>, Permission needed: 'delete:words'
  * PATCH /words/<word_id>, Permission needed: 'patch:words'
  * POST /words/, Permission needed: 'post:words'
  * GET /questions/, Permission needed: 'get:questions'
  * GET /words/<word_id>/answers, Permission needed: 'get:answers'
  * POST /words/<word_id>/answers, Permission needed: 'post:answers'
  
* Endpoints for a normal user:
  * GET /users, Permission needed: 'get:users'
  * DELETE /users/<user_id>, Permission needed: 'delete:users'

### Example user TOKEN
Normal User:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmODkwOWM4ZWZlMDIwMDY4YzBjMWQ1IiwiYXVkIjoiZGljdGlvbmFyeSIsImlhdCI6MTYxMzMzMzgzNiwiZXhwIjoxNjEzMzQxMDM2LCJhenAiOiJpSzVCeFJLdUZoWmZkZE5NcUt4RVJ1OVRqZGc5NWdzTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOndvcmRzIiwiZ2V0OmFuc3dlcnMiLCJnZXQ6cXVlc3Rpb25zIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.V4NViBhTvfkhGx28F_HRdkX-ewFQuoXieZQfcTpbZ0sNo-_29xDF-MdLVDR9AYKBUTtPPHTGBDmu5HcpT0kX0YIB2bAYa1Q3gj1rn2p4ZarDJxOOW34nWzvPXJIATBdbx1WBzeWOY4_Q9XF9bjXLE_CttvCwRtrtna6hYGR1WrMRimuZ_yvGgKRl7fZFbo-Gvro_fkOuFcjyMYPZPWGKlSp6T6hNLzuysEIPtLu8Ax7K1mVMX9GdUuhbQTw2MgJqSic9VeLdYNL5BUxlv2u9c05hKV7JyxczunM7OqFLwbPOWQw4ZggUAMBiJ3dQ7CUs5L72RGkPbuAZgwsxgZZkDQ
```

Admin:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDYzNDc1Nzg1MjAzNDQyOTMzNDMiLCJhdWQiOlsiZGljdGlvbmFyeSIsImh0dHBzOi8vaGVsbG9nYWdhLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTMzMzQwNDQsImV4cCI6MTYxMzM0MTI0NCwiYXpwIjoiaUs1QnhSS3VGaFpmZGROTXFLeEVSdTlUamRnOTVnc0wiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnVzZXJzIiwiZGVsZXRlOndvcmRzIiwiZ2V0OmFuc3dlcnMiLCJnZXQ6cXVlc3Rpb25zIiwiZ2V0OnVzZXJzIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.NCYnYs0eaC__mNqKUwyiEv7e09VzNa0VXhhutFXMBuWVfEeyd0XqTmWRg2J2k60jlN53lI5-8Ix4R2pCo9f-MLDNHVNyE0K5z0UWGOO2vKWLpUQAuXNhdMkQKrji3E7AEGEKlr7_Es2A24HDqLX4HNbTMRfWZTRyIMS5auCO5Hu1LQQg29DjroKFVLrOapTBuxNLCgY-3cBar9jJ_ceUeRswYIiPVYjuJe7BbBYF2R4Pw6dIxF4WOo5bKug0vhNiziJiKxYc2A75had6_BLT5vGu-6ypaCd6kH7f6n3eByGrCVz05jCypNURXmnrTvJDx1p47zLQsPb9X-VNlFydOg
```
**NOTE**: The above token will expire in a very short time.


## Tech Stack (Dependencies)
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip install -r requirements.txt`

## Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── manage.py *** file to manage the database migration. Important for the database configuration in Heroku
  ├── test_app.py *** file to test the API locally. 
  ├── add_records.py *** python file to add data to the database.
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── setup.sh *** environment variables
  ├── auth
  │   ├── auth.py *** code to manage authorization 
  │   └── __init__.py
  └── migrations *** folder that contains the database migration. 
  ```

Overall:
* Models are located in the `models.py`
* Controllers are also located in `app.py`
* Authorization are located in `auth`

## How to use the application locally
1. Understand the Project Structure (explained above) and where important files are located.
2. Install all the dependencies according to the instructions before. 
3. git clone this repo to your local folder using `https://github.com/hellogaga/FSD_capstone.git`
4. Navigate to **model.py** and revise **local database setting** section with your own PostgreSQL username and password. 
5. Login to your PostgreSQL through `psql -U yourusername` and build a local database named **dict** through the following in the computer console `CREATE DATABASE dict;`
6. Navigate to the local folder and run the following commands. They will initiate the required tables in the application. 
```sh
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```  
7. run the following code `python add_data.py dict` to add some pseudo data to the database.  
7. Run `python app.py`  
8. Navigate to project homepage [http://127.0.0.1:5000](http://127.0.0.1:5000) or [http://localhost:5000](http://localhost:5000) 
9. Enjoy the application.
10. Use the following code to bear token
```
curl --request GET http://localhost:5000/words -H "Authorization: Bearer A_VERY_LONG TOKEN"
```

## How to test the application
1. Login to your PostgreSQL through `psql -U yourusername` and build a test database named **dict_test** through the following in the computer console `CREATE DATABASE dict_test;`
2. run the following code `python add_data.py dict_test` to add some pseudo data to the database.  
3. please visit `auth0.com` and set up a new application as well new API. 
4. navigate to `test_app.py` and replace the token variables.
5. run `python test_app.py`

## Deploy to Heroku
1. set up a new application in heroku
2. run the following code to add heroku Postgres addons.
```
heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
```
3. deploy to Heroku. This can be done through linking the github repo with Heroku repo. Please do this in the Heroku dashboard.
4. run the database migration through `heroku run python manage.py db upgrade --app name_of_your_application`
5. After the database migration, a blank database will be created. To add data to the database. Please use 'PGadmin4' to manage it. The database credentials can be found from `data.heroku.com`.
6. Enjoy the application. 

## Licensing, Authors, Acknowledgements
The code released subjects to the MIT license. The author appreciates the code structure from [Udacity](www.udacity.com)
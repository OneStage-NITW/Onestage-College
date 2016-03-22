# Onestage-College
Onestage platform for other colleges


##Initial setup

Run the following commands

* virtualenv onestage
* source onestage/bin/activate
* pip install -r requirements.txt
* go to college/settings.py
* go to databases and in the password and user name for mysql add your own mysql username and password
* python manage.py makemigrations
* python manage.py migrate
* python manage.py runserver

If you see the starting blue page you are good to go

You are ready to go

Current apps : authentication,cap,homeapp

Currently completed: Base Site, CAP invites, registrations and organisation requests

Our site is hosted at www.onestage.org Please check it out and offer feedback.

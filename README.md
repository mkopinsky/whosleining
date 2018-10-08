Who's Leining: Sign-ups and reminders for Torah reading
=======================================================

**Who's Leining** is a Flask-based web application for synagogues to coordinate Torah reading.

In many synagogues, the weekly Torah portion is read by a different member of the congregation each week. Coordinating that is often done with a Google doc or the like, which works well but has some limitations:

1. Someone needs to set up the Google doc in advance, and keep it updated.
2. Google docs are purely passive. People can forget they've signed up, or someone needs to be on top of reminding people.

Wouldn't it be great if there were an app that:
1. Had automatic reminders
2. Could send out an email in advance if no one has signed up
3. Had an display of which portions someone has read, to help motivate you to Gotta Read em All?

**Who's Leining** is (or will be) that app.


## Getting started with development.

This repo is set up to be used with [pipenv](https://pipenv.readthedocs.io/en/latest/).

- Install pipenv 
  - For the time being, you may need to use the workaround at [https://github.com/pypa/pipenv/issues/2924#issuecomment-427351356]() to get around a pip/pipenv issue.
- `pipenv install` to create a virtualenv and install all dependencies
- `FLASK_APP=main.py pipenv run flask run` to run the application in dev mode


from flask import Flask, render_template, request, url_for, redirect, flash
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Shuls, Weeks

from flask_dance.contrib.google import make_google_blueprint, google

import requests, datetime

app = Flask(__name__)
app.secret_key = "supersekrit"

engine = create_engine('sqlite:///leining.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# helper function - create user and return user id
def createUser(login_session):
    newUser = Users(name=login_session['name'], email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id

# helper function - take in user id and return user object
def getUserInfo(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user

# helper function - take in user email and return user id
def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None


# Flask_Dance code for Google sign-in
blueprint = make_google_blueprint(
    client_id="427424805365-ss8sjd94ocgts504dd6d3ahe3335ea1h.apps.googleusercontent.com",
    client_secret="VvRDm1HDvhfHPr1XmTMSU8W5",
    scope=[
        "https://www.googleapis.com/auth/plus.me", "https://www.googleapis.com/auth/userinfo.email"
        ],
    offline=True,
    redirect_url="http://localhost:5000/google/login"
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/google/login")
def googleLogin():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    login_session['provider'] = 'google'
    login_session['name'] = resp.json()['name']
    login_session['email'] = resp.json()['email']
    # check to see if user exists, if not then create one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    # store user_id in session
    login_session['user_id'] = user_id
    assert resp.ok, resp.text
    return "You are now logged in"

@app.route("/logout")
def logout():
    if login_session['provider'] == 'google':
        try:
            token = blueprint.token["access_token"]
            resp = google.post(
                "https://accounts.google.com/o/oauth2/revoke",
                params={"token": token},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
        except:
            return "Logout was unsuccessful"
        login_session.clear()
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shul-info/', methods=['GET', 'POST'])
def shul_info():
    if request.method == 'POST':
        newShul = Shuls(
            name=request.form['name'],
            address=request.form['address'],
            city=request.form['city'],
            state=request.form['state'],
            zip=request.form['zip'],
            calendar_type=request.form['calendar-type'],
            major_holidays=request.form['major'],
            visibility=request.form['visibility'],
            accessibility=request.form['accessibility']
        )
        # add current user object to user attribute of newShul instance
        newShul.user.append(getUserInfo(login_session['user_id']))
        session.add(newShul)
        session.commit()
        flash('Shul added successfully')
        return redirect(url_for('home'))
    else:
        return render_template('shulInfo.html')

@app.route('/my-shuls/')
def my_shuls():
    user = getUserInfo(login_session['user_id'])
    return render_template('myShuls.html', user=user)

@app.route('/<shul_id>/signup/', methods=['GET', 'POST'])
def signup(shul_id):
    shul = session.query(Shuls).filter_by(id=shul_id).one()
    israel = shul.calendar_type
    major = shul.major_holidays
    # Make api call to hebcal
    hebcal = requests.get('https://www.hebcal.com/hebcal/?v=1&cfg=json&year=now&month=x&s=on&maj=' + major + '&i=' + israel)
    hebcal_items = hebcal.json()['items']
    # today's datetime object
    today = datetime.datetime.now()
    # today's date object
    today_date = datetime.date(today.year, today.month, today.day)

    for item in hebcal_items:
        # convert item's date to date object
        item_date = datetime.datetime.strptime(item['date'], '%Y-%m-%d').date()
        if item_date >= today_date:
            week_in_db = session.query(Weeks).filter_by(date=item_date, shul_id=shul.id).all()
            # if that week does not yet exist for that shul, create new object
            if not week_in_db:
                newWeek = Weeks(date=item_date, parasha=item['hebrew'])
                shul.weeks.append(newWeek)
                session.add(newWeek)
                session.commit()
    weeks = session.query(Weeks).filter_by(shul_id=shul.id).all()
    return render_template('signup.html', shul=shul, weeks=weeks, today_date=today_date, datetime=datetime)

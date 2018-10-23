from flask import Flask, render_template, request, url_for
from flask import session as login_session

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Shuls, Weeks

from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)

engine = create_engine('sqlite:///leining.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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
            shabbos_signup=request.form['shabbos'],
            yomtov_signup=request.form['yom-tov'],
            visibility=request.form['visibility'],
            accessibility=request.form['accessibility']
        )
        session.add(newShul)
        session.commit()
        return 'Shul added successfully'
    else:
        return render_template('shulInfo.html')

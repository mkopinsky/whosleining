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


# Flask_Dance code for Google sign-in
blueprint = make_google_blueprint(
    client_id="427424805365-ss8sjd94ocgts504dd6d3ahe3335ea1h.apps.googleuser\
        content.com",
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
    assert resp.ok, resp.text
    return "You are now logged in"


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

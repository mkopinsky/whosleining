from flask import Flask, render_template, request

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Shuls, Weeks

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
    # if request.method == 'POST':
        # stuff
    # else:
    return render_template('shulInfo.html')

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shul-info/', methods=['GET', 'POST'])
def shul_info():
    # if request.method == 'POST':
        # stuff
    # else:
    return render_template('shulInfo.html')

from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import sys
import os
from forms import InputForm
from dotenv import load_dotenv
import requests
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
import ssl
from flask_wtf.csrf import generate_csrf
import json
load_dotenv()
sys.path.append('./')
from Proceslaag.ORC.conf import urls_tokens
conf = urls_tokens()

current_directory = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_directory, 'localhost+2.pem')
key_path = os.path.join(current_directory, 'localhost+2-key.pem')

#context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#context.load_cert_chain(cert_path, key_path)

def getObjectsZorgtoeslag(headers = {"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json"}):
    
    response = requests.get(f"{conf['base_url_objects_zorgtoeslag']}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def find_closest_income(income, data, partner_confirmed, age_confirmed, user_assets):
    closest = None
    min_diff = float('inf')
    for item in data:
        record_data = item['record']['data']
        if record_data['Toeslagpartner?'] == partner_confirmed and \
           record_data['18 jaar of ouder?'] == age_confirmed and \
           record_data['Vermogen'] >= user_assets:
            income_diff = abs(record_data['Inkomen'] - income)
            if income_diff < min_diff:
                min_diff = income_diff
                closest = item

    if closest is None:
        print("Geen geschikte data gevonden voor de gegeven criteria.")
        return None

    return closest


app = Flask(__name__, template_folder='templates', static_folder='static')

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain(cert_path, key_path)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

csrf = CSRFProtect(app)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = app.secret_key
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CSRF_TRUSTED_ORIGINS'] = ['https://127.0.0.1:5002', 'https://localhost:8002']
#app.config['SESSION_COOKIE_SAMESITE'] = 'None'
csrf.init_app(app)

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
    
@app.after_request
def after_request(response):
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response 
   
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid Credentials. Please try again.')  
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/testpage')
def testpage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('test.html')

@app.route('/iframetest')
@csrf.exempt
def test():
    return render_template('iframetest.html')

@app.route('/form_page', methods=['GET', 'POST'])
def form_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    form = InputForm()
    if request.method == 'POST' and form.validate_on_submit():
        age_confirmed = 'ja' if form.age_confirmation.data else 'nee'
        partner_confirmed = 'ja' if form.partner_confirmation.data else 'nee'
        annual_income = int(round(form.annual_income.data))
        assets = int(round(form.assets.data))

        api_data = getObjectsZorgtoeslag()
        if api_data:
            closest_data = find_closest_income(annual_income, api_data, partner_confirmed, age_confirmed, assets)
            if closest_data:
                session['result_data'] = closest_data['record']['data']
                return redirect(url_for('resultaat'))
            else:
                return render_template('geen_zorgtoeslag.html')
        else:
            return render_template('error.html', message="Fout bij het ophalen van de data.")
    return render_template('form_page.html', form=form)

@app.route('/subsidie')
def subsidie():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('subsidie.html')

@app.route('/resultaat')
def resultaat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = session.get('result_data', {})
    if not data:
        return redirect(url_for('geen_zorgtoeslag'))
    return render_template('resultaat.html', data=data)

@app.route('/geen_zorgtoeslag')
def geen_zorgtoeslag():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('geen_zorgtoeslag.html')


@app.route('/output')
def output():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('output.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True, ssl_context=context)
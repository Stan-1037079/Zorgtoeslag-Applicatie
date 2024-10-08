from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import sys
import os
from forms import InputForm, InputFormkinderbijslag, ChildForm
from dotenv import load_dotenv
import requests
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
import ssl
from flask_wtf.csrf import generate_csrf
import json
import psycopg2
from wtforms import FormField
from datetime import datetime
load_dotenv()
#sys.path.append('./')
#from Datalaag.azuredb_connect import get_db_connection
#from Proceslaag.ORC.conf import urls_tokens
from confies import zorgtoeslagurl
conf = zorgtoeslagurl()

current_directory = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_directory, 'localhost+2.pem')
key_path = os.path.join(current_directory, 'localhost+2-key.pem')

def getObjectsZorgtoeslag(headers = {"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json"}):
    
    response = requests.get(f"{conf['base_url_objects_zorgtoeslag']}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def getObjectsKinderbijslag(headers = {"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json"}):
    
    response = requests.get(f"{conf['base_url_objects_kinderbijslag']}", headers=headers)
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

def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

app = Flask(__name__, template_folder='templates', static_folder='static')

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain(cert_path, key_path)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
    return conn

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

@app.route('/gebruikers_data_zorgtoeslag')
def gebruikers_data_zorgtoeslag():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM subsidie.gebruikers_data")
    data = cur.fetchall()  
    cur.close()
    conn.close()
    
    return render_template('gebruikers_data_zorgtoeslag.html', data=data)

@app.route('/testpage')
def testpage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('test.html')

@app.route('/iframetest')
@csrf.exempt
def test():
    return render_template('iframetest.html')

@app.route('/zorgtoeslag_voorwaarden')
def zorgtoeslag_voorwaarden():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('zorgtoeslag_voorwaarden.html')

@app.route('/kinderbijslag_voorwaarden')
def kinderbijslag_voorwaarden():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('kinderbijslag_voorwaarden.html')

@app.route('/kinderbijslag_resultaat')
def kinderbijslag_resultaat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('kinderbijslag_resultaat.html')

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

        session['user_input'] = {
            '18_jaar_of_ouder': age_confirmed,
            'Toeslagpartner': partner_confirmed,
            'Inkomen': annual_income,
            'Vermogen': assets
        }
        print(session['user_input'])
        if age_confirmed == 'nee':
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO subsidie.gebruikers_data ("18_jaar_of_ouder", "Toeslagpartner", "Inkomen", "Vermogen", "Zorgtoeslag")
                VALUES (%s, %s, %s, %s, 0)
            """, (age_confirmed, partner_confirmed, annual_income, assets))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('geen_zorgtoeslag.html')

        
        api_data = getObjectsZorgtoeslag()
        if api_data:
            closest_data = find_closest_income(annual_income, api_data, partner_confirmed, age_confirmed, assets)
            if closest_data:
                zorgtoeslag = closest_data['record']['data']['Zorgtoeslag']
                session['result_data'] = closest_data['record']['data']
                print(session['result_data'])
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO subsidie.gebruikers_data ("18_jaar_of_ouder", "Toeslagpartner", "Inkomen", "Vermogen", "Zorgtoeslag") 
                    VALUES (%s, %s, %s, %s, %s)
                """, (age_confirmed, partner_confirmed, annual_income, assets, zorgtoeslag))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('resultaat'))
            else:
                return render_template('geen_zorgtoeslag.html')
        else:
            return render_template('home.html', message="Fout bij het ophalen van de data.")
    return render_template('form_page.html', form=form)

@app.route('/form_page_kinderbijslag', methods=['GET', 'POST'])
def form_page_kinderbijslag():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    form = InputFormkinderbijslag()

    if request.method == 'POST':
        how_much_children = request.form.get('how_much_children', type=int)

        if how_much_children:
            while len(form.children) < how_much_children:
                form.children.append_entry()
            while len(form.children) > how_much_children:
                form.children.pop_entry()

        form.process(request.form)

        if form.validate_on_submit():
            children_data = form.children.data
            api_data = getObjectsKinderbijslag()

            if api_data is None:
                return render_template('form_page_kinderbijslag.html', form=form, error="Fout bij het ophalen van de API-gegevens.")

            total_amount = 0
            children_results = []

            for child in children_data:
                birthdate = child['date_of_birth']
                age = calculate_age(birthdate)
                matched = False
                for item in api_data:
                    if int(item['record']['data']['Leeftijd kind']) == age:
                        amount = item['record']['data']['Bedrag']
                        total_amount += amount
                        children_results.append({
                            'birthdate': birthdate,
                            'age': age,
                            'amount': amount
                        })
                        matched = True
                        break
                if not matched:
                    children_results.append({
                        'birthdate': birthdate,
                        'age': age,
                        'amount': 0  
                    })

            return render_template('kinderbijslag_resultaat.html', form=form, children=children_results, total_amount=total_amount)
        else:
            print("Formulier validatie mislukt.")
            print(form.errors)
    
    return render_template('form_page_kinderbijslag.html', form=form)

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
    user_input = session.get('user_input', {}) 
    if not data:
        return redirect(url_for('geen_zorgtoeslag'))
    return render_template('resultaat.html', data=data, user_input=user_input)


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
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import os
#from forms import InputForm
from dotenv import load_dotenv
import requests
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
import ssl
from flask_wtf.csrf import generate_csrf
load_dotenv()

current_directory = os.path.dirname(os.path.abspath(__file__))
cert_path = os.path.join(current_directory, 'localhost+2.pem')
key_path = os.path.join(current_directory, 'localhost+2-key.pem')

#context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#context.load_cert_chain(cert_path, key_path)

app = Flask(__name__, template_folder='templates', static_folder='static')

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain(cert_path, key_path)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

CORS(app)
csrf = CSRFProtect(app)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = app.secret_key
csrf.init_app(app)

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
    
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

@app.route('/iframetest')
def test():
    return render_template('iframetest.html')

#@app.route('/form_page', methods=['GET', 'POST'])
#def form_page():
#    if not session.get('logged_in'):
#        return redirect(url_for('login'))
#    form = InputForm()
#    if form.validate_on_submit():
#        return redirect(url_for('subsidie'))  
#    return render_template('form_page.html', form=form)

@app.route('/subsidie')
def subsidie():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('subsidie.html')

@app.route('/output')
def output():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('output.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True, ssl_context=context)
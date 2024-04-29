import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

DB_HOST = "cg1.postgres.database.azure.com"
DB_NAME = "subsidie"
DB_USER = "stan"
DB_PASS = "g9jflc1mtXF7H0q2IFF"
DB_PORT = "5432"

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
    return conn

@app.route('/')
def res():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id FROM subsidie.test')  
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('res.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5200)

from flask import Flask, request, g
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'ips.db'

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Ensure the database and table are created
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reversed_ip TEXT NOT NULL
            )
        ''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function to reverse the IP address
def reverse_ip(ip):
    return '.'.join(ip.split('.')[::-1])

# Route to handle incoming requests and store reversed IPs
@app.route('/')
def index():
    ip = request.remote_addr
    reversed_ip = reverse_ip(ip)

    # Store the reversed IP in the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO ips (reversed_ip) VALUES (?)", (reversed_ip,))
    db.commit()

    return f"Your reversed IP is: {reversed_ip}"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')

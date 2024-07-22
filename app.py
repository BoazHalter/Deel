from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'ips.db'

# Ensure the database and table are created
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reversed_ip TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to reverse the IP address
def reverse_ip(ip):
    return '.'.join(ip.split('.')[::-1])

# Route to handle incoming requests and store reversed IPs
@app.route('/')
def index():
    ip = request.remote_addr
    reversed_ip = reverse_ip(ip)

    # Store the reversed IP in the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ips (reversed_ip) VALUES (?)", (reversed_ip,))
    conn.commit()
    conn.close()

    return f"Your reversed IP is: {reversed_ip}"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')

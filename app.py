from flask import Flask, request, g
import sqlite3
import os
import ipaddress

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
    if ':' in ip:
        return ip  # Skip reversing if it's an IPv6 address
    return '.'.join(ip.split('.')[::-1])

# Function to extract the client's real IP address
def get_real_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_list = x_forwarded_for.split(',')

    for ip in ip_list:
        ip = ip.strip()
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.version == 4 and not ip_obj.is_private:
                return ip
        except ValueError:
            continue

    # Fall back to the first IP in the list or request.remote_addr
    return ip_list[0].strip() if ip_list else request.remote_addr

# Route to handle incoming requests and store reversed IPs
@app.route('/')
def index():
    ip = get_real_ip()
    reversed_ip = reverse_ip(ip)

    # Store the reversed IP in the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO ips (reversed_ip) VALUES (?)", (reversed_ip,))
    db.commit()

    return f"Your reversed IP is: {reversed_ip}"

@app.before_request
def before_request():
    if 'ips' not in g:
        print("Initializing the database.")
        init_db()
        g.ips = True

if __name__ == '__main__':
    print(f"Database path: {os.path.abspath(DATABASE)}")
    init_db()
    app.run(debug=True, host='0.0.0.0')

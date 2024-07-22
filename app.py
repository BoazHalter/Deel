from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Function to reverse the IP address
def reverse_ip(ip):
    return '.'.join(ip.split('.')[::-1])

# Route to handle incoming requests and store reversed IPs
@app.route('/')
def index():
    ip = request.remote_addr
    reversed_ip = reverse_ip(ip)

    # Store the reversed IP in the database
    conn = sqlite3.connect('ips.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ips (reversed_ip) VALUES (?)", (reversed_ip,))
    conn.commit()
    conn.close()

    return f"Your reversed IP is: {reversed_ip}"

if __name__ == '__main__':
    app.run(debug=True)

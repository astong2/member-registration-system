from flask import flash, get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask import session
from flask import redirect, url_for
from flask import Flask, render_template, request

def get_db_connection():
    conn = sqlite3.connect('members.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

@app.route('/users')
def users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()

    return render_template('users.html', users=users)


@app.route('/')
def home():
    username = session.get('username')
    return render_template('home.html' , username=username)
# This route renders a simple HTML page with a form for user registration

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Error: passwords do not match!", 400
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            flash('Email already registered. Try again.')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                  (username, email, hashed_password))
        conn.commit()
        conn.close()
       
        print(f"Username: {username}, Email: {email}, Password: {password}")
        return redirect(url_for('thank_you'))          
    return render_template('register.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
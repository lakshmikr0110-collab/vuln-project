from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Setup simple DB
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def home():
    return '''
    <h1>Vulnerable App is Live!</h1>
    <p>Project by Lakshmi</p>
    <hr>
    <h2>Try These:</h2>
    <a href="/login">1. Login Page - SQL Injection Demo</a><br><br>
    <a href="/search">2. Search Page - XSS Demo</a>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        # VULNERABLE QUERY - for learning only
        query = f"SELECT * FROM users WHERE username='{user}' AND password='{pwd}'"
        try:
            cur.execute(query)
            result = cur.fetchone()
        except Exception as e:
            return f"SQL Error: {e} <br><a href='/login'>Back</a>"
        if result:
            return f"<h1>Welcome {user} ! Login Success!</h1><a href='/'>Home</a>"
        else:
            return "<h1>Login Failed</h1><a href='/login'>Try Again</a>"
    return '''
    <h1>Login</h1>
    <form method="POST">
    Username: <input name="username"><br><br>
    Password: <input name="password"><br><br>
    <button>Login</button>
    </form>
    <p>Hint: Real user is admin / admin123</p>
    <a href="/">Home</a>
    '''

@app.route('/search')
def search():
    q = request.args.get('q', '')
    # VULNERABLE - XSS for learning only
    return f'''
    <h1>Search</h1>
    <form>
    <input name="q" placeholder="Search here">
    <button>Search</button>
    </form>
    <h3>You searched for: {q}</h3>
    <a href="/">Home</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

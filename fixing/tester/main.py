from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'mysecretkey' # Set a secret key for session cookie security

# Dictionary to hold registered users
users = {}

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            error = 'Username already exists.'
            return render_template('register.html', error=error)
        else:
            users[username] = password
            return redirect('/login')
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            error = 'Invalid username.'
            return render_template('login.html', error=error)
        elif users[username] != password:
            error = 'Incorrect password.'
            return render_template('login.html', error=error)
        else:
            session['username'] = username # Set session cookie
            return redirect('/home')
    return render_template('login.html')

# Home page route (requires login)
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect('/login')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None) # Remove session cookie
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

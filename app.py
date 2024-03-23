import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/google-login')
def google_login():
    # Create a Google authentication provider
    provider = auth.GoogleAuthProvider()

    # Specify additional scopes if needed
    provider.add_scope('profile')
    provider.add_scope('email')

    # Authenticate with Firebase using the Google provider
    try:
        user = auth.verify_id_token(request.form['idToken'], check_revoked=True)
        # Successfully authenticated with Firebase
        session['user_id'] = user['uid']  # Store user ID in session
        return redirect(url_for('dashboard'))
    except Exception as e:
        # Authentication failed
        return str(e)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        return render_template('dashboard.html', user_id=user_id)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

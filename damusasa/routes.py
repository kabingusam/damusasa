from damusasa import app
from flask_login import LoginManager
from flask import render_template
from flask import abort, session, Flask, redirect, request
import requests
import os
import pathlib
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from .models import User
from google.oauth2 import id_token
import google.auth.transport.requests
from google.oauth2 import id_token


load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('NEWS_API_KEY')
google_key = os.getenv('GOOGLE_KEY')
secret_key = os.getenv('APP_KEY')


app = Flask(__name__, template_folder='templates')

app.secret_key = secret_key
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = google_key
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback" 
)

# function to check if user is authenticated
def login_is_required():
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper

@app.route('/login')
def login():
    # asking the flow class for the authorization (login) url
    authorization_url, state = flow.authorization_url(prompt="consent")
    session["state"] = state
    return redirect(authorization_url)
    # return render_template('Login.html')

@app.route('/logout')
def logout():
    session.clear
    return redirect('/')

#add user to the database
def add_user_to_database(db, google_id, name):
    #check if the user exists
    user = User.query.filter_by(google_id=google_id).first()

    if not user:
        # If user doesnt exist , create a new user
        user = User(google_id=google_id, username=name)
        db.session.add(user)
        db.session.commit()

#this is the page that will handle the callback process meaning process after the authorization
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        token_request,
        GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    # retrieve the google_id and name from the session
    google_id = session.get("google_id")
    name = session.get("name")
    print(google_id)
    print(name)

    return redirect("/dashboard")

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register_patient')
def register_patient():
    return render_template('index.html')

@app.route('/record_vitals')
def record_vitals():
    return render_template('index.html')
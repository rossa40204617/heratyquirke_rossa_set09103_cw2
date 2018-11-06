from flask import Flask, g, render_template, session, url_for, request, redirect
from functools import wraps
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'super duper secret key'


db_location = 'var/booking.db'

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
      db = sqlite3.connect(db_location)
      g.db = db
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def home():
  return render_template('base.html')

@app.route('/logout/')
def logout():
  session['logged_in'] = False
  return redirect(url_for('.home'))
  
@app.route('/login/', methods=['POST'])
def login():
  if login_user(request.form):
    session['logged_in'] = True
  return redirect(url_for('.home'))

def login_user(request):
  user_email = request['user_email']
  user_password = request['user_password']
  
  return verify_user(user_email, user_password)

def verify_user(email, password):
  db = get_db()
  cur = db.cursor()
  
  cur.execute("SELECT user_password FROM users WHERE user_email=?", (email,))
 
  hashed_password = cur.fetchone()[0]
  
  if hashed_password == bcrypt.hashpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
    return True
  else:
    return False
  
@app.route('/register/', methods=['POST'])
def register_user():
  add_new_user(request.form)
  return redirect(url_for('.home'))

def add_new_user(request):
  
  username = request['username']
  user_email = request['user_email']
  user_password = request['user_password']
  
  hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
  
  db = get_db()
  db.cursor().execute('insert into users (username, user_email, user_password) VALUES (?,?,?)', (username, user_email, hashed_password)) 
  db.commit()
  

def requires_login(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    status= session.get('logged_in', False)
    if not status: 
      return redirect(url_for('.home'))
    return f(*args, **kwargs)
  return decorated
  
@app.route('/db/')
@requires_login
def db():

  db = get_db()
  
  page = []
  page.append('<html><ul>')
  sql = "SELECT rowid, * FROM users ORDER BY username" 
  for row in db.cursor().execute(sql):
    page.append('<li >') 
    page.append(str(row))
    page.append('</li >')
  page.append('</ul><html>')
  return ''.join(page)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)




from flask import Flask, g, render_template
import sqlite3

app = Flask(__name__)

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

@app.route('/login/', methods=['POST'])
def login():
  return "login" 

@app.route('/register/', methods=['POST'])
def register_user():
  add_new_user(request.form)


def add_new_user(request):
  
  username = request['username']
  user_email = request['user_email']
  user_password = request['user_password']
  
  db = get_db()
  db.cursor().execute('insert into users (username, user_email, user_password) VALUES (?,?,?)', (username, user_email, user_password)) 
  db.commit()
  
@app.route('/db/')
def db():

  db = get_db()
  
  db.cursor().execute("INSERT INTO users (username, user_email, user_password) VALUES (?,?,?)", ("username", "email", "password"))
  db.commit()
  
  page = []
  page.append('<html><ul>')
  sql = "SELECT rowid, * FROM users ORDER BY username" 
  for row in db.cursor().execute(sql):
    page.append('<li >') 
    page.append(str(row))
    page.append('</li >')
  page.append('</ul><html>')
  return ''.join(page)



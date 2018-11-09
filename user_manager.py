import bcrypt
from database import get_db
from user import User

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

def get_user(email):
  db = get_db()
  cur = db.cursor()

  cur.execute("SELECT username, user_email, user_id FROM users WHERE user_email=?", (email,))
  
  user_entry = cur.fetchone() 
  user = User(user_entry[0], user_entry[1], user_entry[2])  
 
  return user

def add_new_user(request):
  username = request['username']
  user_email = request['user_email']
  user_password = request['user_password']

  hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

  db = get_db()
  db.cursor().execute('INSERT into users (username, user_email, user_password) VALUES (?,?,?)', (username, user_email, hashed_password))
  db.commit()

def add_new_user(request):
  username = request['username']
  user_email = request['user_email']
  user_password = request['user_password']

  hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

  db = get_db()
  db.cursor().execute('INSERT into users (username, user_email, user_password) VALUES (?,?,?)', (username, user_email, hashed_password))
  db.commit()


from flask import Flask, render_template, session, url_for, request, redirect
from functools import wraps
from database import get_db, init_db
import booking_manager
import bcrypt

app = Flask(__name__)
app.secret_key = 'super duper secret key'

@app.route('/')
def home():
  return render_template('home_page.html')

@app.route('/logout/')
def logout():
  session['logged_in'] = False
  session['user'] = None
  session['admin'] = False
  return redirect(url_for('.home'))
  
@app.route('/login/', methods=['POST'])
def login():
  if login_user(request.form):
    session['logged_in'] = True
    email = request.form['user_email']
    session['user'] = get_username(email)
    if email == 'admin':
      session['admin'] = True
    
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

def get_username(email):
  db = get_db()
  cur = db.cursor()
  
  cur.execute("SELECT username FROM users WHERE user_email=?", (email,))
  
  return cur.fetchone()[0]
  
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
  
def requires_admin(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    status = session.get('admin', False)
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
  sql = "SELECT rowid, * FROM booking_ads ORDER BY booking_ad_id" 
  for row in db.cursor().execute(sql):
    page.append('<li >') 
    page.append(str(row))
    page.append('</li >')
  page.append('</ul><html>')
  return ''.join(page)

@app.route('/admin_editor/')
@requires_admin
def admin_editor():
  return render_template('admin_editor.html')

@app.route('/admin_editor/add_booking_ad/', methods=['GET', 'POST'])
@requires_admin
def add_booking_ad():
   
  if request.method == 'POST':
    image = request.files['image']  
    booking_manager.add_booking_ad(request.form, image)

  return render_template('add_booking_ad.html')

@app.route('/admin_editor/remove_booking_ad/', methods=['GET', 'POST'])
@requires_admin
def remove_booking_ad():
   
  if request.method == 'POST':
    booking_ad_id = request.form['booking_ad_id']
    booking_manager.remove_booking_ad(booking_ad_id)
  
  return render_template('remove_booking_ad.html')

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)




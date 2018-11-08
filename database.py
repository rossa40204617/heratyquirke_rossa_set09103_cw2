from flask import Flask, g
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



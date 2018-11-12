from database import get_db
import colony_manager
from bookings import Bookings

def create_booking(request, booking_owner_id, colony_id):

  number_of_people = request['number_of_people']
  cost = request['cost']

  total_cost = int(cost) * int(number_of_people)

  db = get_db() 
  db.cursor().execute('INSERT into bookings (colony_id, booking_owner_id, number_of_people, total_cost) VALUES(?,?,?,?)', (colony_id, booking_owner_id, number_of_people, total_cost))
  db.commit()
  
  update_colony_ad_spaces(colony_id, number_of_people)

def remove_booking(booking_id):
  
  db = get_db()
  db.cursor().execute('DELETE FROM bookings WHERE booking_id=?', (booking_id,))
  db.commit()

def get_bookings_for_user(user_id):
  
   db = get_db()
   cur = db.cursor()
   
   cur.execute("SELECT * FROM bookings WHERE booking_owner_id=?  COLLATE NOCASE", (user_id,))
   
   db_entries = cur.fetchall()  
  
   bookings = convert_db_entries_to_bookings(db_entries)

   return bookings

def convert_db_entries_to_bookings(entries):
  
  bookings = [Bookings( 
               entry[0], entry[1],
               entry[2], entry[3], entry[4]) 
               for entry in entries]
  return bookings  

def update_colony_ad_spaces(colony_id, spaces):
 
  db = get_db()
  cur = db.cursor()
   
  colony_ad = colony_manager.get_colony(colony_id)
 
  spaces_left = colony_ad.spaces_available - int(spaces)

  if spaces_left >= 1:
    cur.execute("UPDATE colony_ads SET spaces_available=? WHERE colony_ad_id=?", (spaces_left, colony_id))
    db.commit()
  else:
    colony_manager.remove_colony_ad(colony_id)
  
  

from database import get_db
import colony_manager

def create_booking(request, booking_owner_id, colony_id):

  number_of_people = request['number_of_people']
  cost = request['cost']

  total_cost = int(cost) * int(number_of_people)

  db = get_db() 
  db.cursor().execute('INSERT into bookings (colony_id, booking_owner_id, number_of_people, total_cost) VALUES(?,?,?,?)', (colony_id, booking_owner_id, number_of_people, total_cost))
  db.commit()
  
  update_colony_ad_spaces(colony_id, number_of_people)

def update_colony_ad_spaces(colony_id, spaces):
 
  db = get_db()
  cur = db.cursor()
   
  colony_ad = colony_manager.get_colony(colony_id)
 
  spaces_left = colony_ad.spaces_available - int(spaces)

  print(spaces_left)
   
  if spaces_left >= 1:
    cur.execute("UPDATE colony_ads SET spaces_available=? WHERE colony_ad_id=?", (spaces_left, colony_id))
    db.commit()
    print("not none")
  else:
    print("None")
    colony_manager.remove_colony_ad(colony_id)
  
  

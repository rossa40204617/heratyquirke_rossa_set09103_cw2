from database import get_db

def create_booking(request, booking_owner_id, colony_id):

  number_of_people = request['number_of_people']

  dg = get_db() 
  db.cursor().execute('INSERT into bookings (colony_id, booking_owner_id, number_of_people) VALUES(?,?,?)', (colony_id, booking_owner_id, number_of_people))
  db.commit()


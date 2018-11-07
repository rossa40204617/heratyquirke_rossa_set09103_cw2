from database import get_db

def add_booking_ad(request, image):
  
  booking_destination = request['booking_destination']
  booking_description = request['booking_description']
  spaces_available = request['spaces_available']
  booking_journey_time = request['journey_time']
  
  db = get_db()

  db.cursor().execute('INSERT into booking_ads (booking_destination, booking_description, booking_journey_time, spaces_available, image) VALUES (?,?,?,?,?)', (booking_destination, booking_description, booking_journey_time, spaces_available, image.filename))  
  
  db.commit()

def remove_booking_ad(ad_id):

  db = get_db()
  db.cursor.execute('DELETE FROM bookings_ads WHERE booking_ad_id=?', (ad_id,))

  db.commit()

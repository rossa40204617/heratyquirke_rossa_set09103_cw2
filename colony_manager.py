from database import get_db

def add_colony_ad(request, image):
  
  colony_name = request['colony_name']
  colony_location = request['colony_location']
  colony_description = request['colony_description']
  spaces_available = request['spaces_available']
  colony_journey_time = request['journey_time']
  
  db = get_db()

  db.cursor().execute('INSERT into colony_ads (colony_name, colony_location, colony_description, colony_journey_time, spaces_available, image) VALUES (?,?,?,?,?)', (colony_name, colony_location, colony_description, colony_journey_time, spaces_available, image.filename))  
  
  db.commit()

def remove_colony_ad(ad_id):

  db = get_db()
  db.cursor().execute('DELETE FROM colony_ads WHERE colony_ad_id=?', (ad_id,))

  db.commit()

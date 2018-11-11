from database import get_db
from colony_ad import Colony_Ad

def add_colony_ad(request, image):
  
  colony_name = request['colony_name']
  colony_location = request['colony_location']
  colony_description = request['colony_description']
  spaces_available = request['spaces_available']
  colony_journey_time = request['journey_time']
  cost = request['cost']

  image_path = 'img/' + image.filename
  image.save('static/' + image_path)
    
  db = get_db()

  db.cursor().execute('INSERT into colony_ads (colony_name, colony_location, colony_description, colony_journey_time, spaces_available, cost, image) VALUES (?,?,?,?,?,?,?)', (colony_name, colony_location, colony_description, colony_journey_time, spaces_available, cost, image_path))  
  
  db.commit()

def remove_colony_ad(ad_id):

  db = get_db()
  db.cursor().execute('DELETE FROM colony_ads WHERE colony_ad_id=?', (ad_id,))

  db.commit()

def get_colony_ads(location):
  
  db = get_db()
  cur = db.cursor()
  
  if location == 'all':
    cur.execute("SELECT * FROM colony_ads") 
  else:
    cur.execute("SELECT *  FROM colony_ads WHERE colony_location=? COLLATE NOCASE", (location,))

  database_entries = cur.fetchall()
  
  colony_ads = convert_db_entries_to_colony_ads(database_entries)
  
  return colony_ads

def get_colony(colony_id):
  
  db = get_db()
  cur = db.cursor()
  
  cur.execute("SELECT * FROM colony_ads WHERE colony_ad_id=?", (colony_id,))
  
  entry = cur.fetchone()
 
  colony = Colony_Ad(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7])

  return colony

def search_colony_ads(term):

  db = get_db()
  cur = db.cursor()
  
  cur.execute("SELECT * FROM colony_ads WHERE (colony_name LIKE ? or colony_location LIKE ?)", ('%' + term + '%', '%' + term + '%'))
  
  entries = cur.fetchall()

  colony_ads = convert_db_entries_to_colony_ads(entries)
  
  return colony_ads

def convert_db_entries_to_colony_ads(entries):
  
  colony_ads = [Colony_Ad(
                 entry[0], entry[1], 
                 entry[2], entry[3],
                 entry[4], entry[5],
                 entry[6], entry[7]
               ) for entry in entries]
   
  return colony_ads

def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x.uid in seen or seen_add(x.uid))]



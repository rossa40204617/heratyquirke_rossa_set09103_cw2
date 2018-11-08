CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    user_email TEXT UNIQUE,
    user_password TEXT,
    user_id INTEGER PRIMARY KEY AUTOINCREMENT 
);

CREATE TABLE IF NOT EXISTS bookings ( 
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    colony_id INTEGER,
    booking_owner_id INTEGER,
    number_of_people INTEGER,
     
    FOREIGN KEY (booking_owner_id) REFERENCES users (user_id)
    FOREIGN KEY (colony_id) REFERENCES destinations (colony_ad_id)
);

CREATE TABLE IF NOT EXISTS colony_ads (
    colony_ad_id INTEGER PRIMARY KEY AUTOINCREMENT,
    colony_name TEXT,
    colony_location TEXT,
    colony_description TEXT,
    colony_journey_time TEXT,
    cost INTEGER,
    spaces_available INTEGER,
    image TEXT
);


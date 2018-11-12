from flask import Flask, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": 'solarstart.bookings@gmail.com',
        "MAIL_PASSWORD": 'Test123!'
}

app.config.update(mail_settings)
mail = Mail(app)

def send_confirmation_email(request, email, username):
      total_cost = int(request['cost']) * int(request['number_of_people'])
      colony_name = request['colony_name']
      number_of_people = request['number_of_people']

      with app.app_context():
        msg = message(subject="solarstart booking confirmation",
                      sender=app.config.get("mail_username"),
                      recipients=[email])
        msg.html = render_template('email_confirmation.html', username=username, spaces=number_of_people, total_cost=total_cost, colony_name=colony_name)
        mail.send(msg)


def send_registration_email(email):
      with app.app_context():
        msg = Message(subject="SolarStart Registration Confirmation",
                      sender=app.config.get("MAIL_USERNAME"), 
                      recipients=[email])
        msg.body = "Thank you for registering with SolarStart"
        mail.send(msg) 

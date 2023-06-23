from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from flask_mail import Message
from flask_mail import Mail

views = Blueprint('views', __name__)
mail = Mail()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

            return jsonify({})



@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Send email
        send_email(name, email, message)

        # Store in database
        save_contact(name, email, message)

        return "Thank you for contacting us! We will get back to you soon."

    return render_template('contact.html', user=current_user)

def send_email(name, email, message):
    msg = Message("Contact Form Submission", sender=email, recipients=["winbit30@gmail.com"])
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    mail.send(msg)


def save_contact(name, email, message):
    # Save the contact form data in the database
    # You can use the Note model or create a separate Contact model for this purpose
    contact = Contact(name=name, email=email, message=message)
    db.session.add(contact)
    db.session.commit()


@views.route("/about")
def about():
    return render_template("about.html", user=current_user)

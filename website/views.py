from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Question
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('question')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Add Question !!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    question = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    QuestionID = question['noteId']
    question = question.query.get(QuestionID)
    if question:
        if question.user_id == current_user.id:
            db.session.delete(question)
            db.session.commit()

    return jsonify({})

        
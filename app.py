from io import BytesIO
import os
from flask import Flask, Response, jsonify, redirect, render_template, request, send_file, url_for
from database import load_db_contacts, engine, Session, Base
from sqlalchemy import Column, Integer, LargeBinary, String, text
from werkzeug.utils import secure_filename
import spacy   
import textstat
app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")


class Contact(Base):
    __tablename__ = 'contacts2'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(254), nullable=False)
    message = Column(String(250), nullable=False)
    photo_name = Column(String(50))
    photo = Column(LargeBinary)
    
Base.metadata.create_all(engine)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aboutMe')
def about():
    return render_template('aboutMe.html')

@app.route('/contactMe' , methods=['GET','POST'])
def contact():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        photo = request.files.get('photo')
        
        if photo:
            photo_data = photo.read()
            photo_name = photo.filename
            mimetype = photo.mimetype
        else:
            photo_data = None
            photo_name = None
            mimetype = None
              
        session = Session()
        
        new_contact = Contact(name=name, email=email, message=message, photo_name=photo_name,photo=photo_data)
        session.add(new_contact)
        
        session.commit()
        
        session.close()
        
        
        return redirect(url_for('contact'))
    
    session = Session()
    contacts = load_db_contacts()
    session.close()
    
    return render_template('contactMe.html',contacts=contacts)

@app.route('/photo/<int:id>')
def download(id):
    session = Session()
    contact = session.query(Contact).filter_by(id=id).first()
    session.close()
    picID = id
    if contact and contact.photo:
        download_name = contact.photo_name if contact.photo_name else "default.jpg"
        return send_file(BytesIO(contact.photo),mimetype='image/jpeg',as_attachment=True, download_name=download_name)
    else:
        return 'Photo Not Found!',404
    
@app.route('/contactMe/api/contacts')
def list_contacts():
    contacts = load_db_contacts()
    return jsonify(contacts)

@app.route('/readability', methods=['GET','POST'])
def readability():
    text = ""
    if request.method == 'POST':
        text = request.form['text']
        doc = nlp(text)
        readability_score = textstat.flesch_reading_ease(text)
        return render_template('readability.html', text=text, readability_score=readability_score)
    return render_template('readability.html', text=text, readability_score=None) 
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# print(__name__)
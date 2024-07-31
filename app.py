from io import BytesIO
import os
from flask import Flask, Response, jsonify, redirect, render_template, request, send_file, url_for
from database import load_db_contacts, engine, Session, Base
from sqlalchemy import Column, Integer, LargeBinary, String, text
from werkzeug.utils import secure_filename
import spacy   
import textstat

app = Flask(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def ruben_readability(text):
    def count_syllables(word):
        word = word.lower()
        syllables = 0 
        vowels = "aeiouy"
        
        if len(word) <= 3:
            return 1
        
        if word[0] in vowels:
            syllables += 1
        
        for index in range(1, len(word)):
            if word[index] in vowels and word[index -1] not in vowels:
                if not (index == len(word) - 1 and word[index] == 'e' and word[-2:] != 'le'):
                    syllables += 1
                
        if word.endswith('es') or word.endswith('ed'):
            syllables -= 1
        if word.endswith('e') and not word.endswith('le'):
            syllables -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            syllables += 1
        
        return max(syllables, 1)
    
    #Sentence counter 
    sentence_count = 0
    sentence_end = '.!?;:'
    for char in text:
        if char in sentence_end:
            sentence_count += 1
    
    #Word counter
    words = text.split()
    word_count = len(words)
    
    in_word = False
    vowels = "aeiou"
    
    #Syllable counter
    syllable_count = sum(count_syllables(word) for word in words)
    
    if sentence_count == 0 or word_count == 0:
        return 0
    
    read_index_formula = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
    read_index = format(read_index_formula, ".2f")
    return read_index,syllable_count, word_count,sentence_count

def grade_level(text):
    read_stats = ruben_readability(text)
    
    grade_formula = 0.39 * (read_stats[2] / read_stats[3]) + 11.8 * (read_stats[1] / read_stats[2]) - 15.59
    grade = round(grade_formula)
    
    return grade
    
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
    spacy_results = None
    ruben_results = None
    text = ""
    
    if request.method == 'POST':
        text = request.form['text']
        
        if text:
        #SpaCy/textstat readability
            doc = nlp(text)
            spacy_results = textstat.flesch_reading_ease(text)
            
            #Basic Ruben readability
            ruben_results = ruben_readability(text)
            
            #Grade Equivalent
            grade_result = grade_level(text)
            
            
        
        return render_template('readability.html', text=text, spacy_results=spacy_results,ruben_results=ruben_results,grade_result=grade_result)
    return render_template('readability.html', text=text, spacy_results=None,basic_results=None,grade_result=None) 
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

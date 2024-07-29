from flask import Flask, jsonify, redirect, render_template, request,url_for
from database import load_db_contacts, engine, Session, Base
from sqlalchemy import Column, Integer, String, text

app = Flask(__name__)

class Contact(Base):
    __tablename__ = 'contacts2'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(254), nullable=False)
    message = Column(String(250), nullable=False)
    
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
        
        session = Session()
        
        new_contact = Contact(name=name, email=email, message=message)
        session.add(new_contact)
        
        session.commit()
        
        session.close()
        
        return redirect(url_for('contact'))
    
    session = Session()
    contacts = load_db_contacts()
    session.close()
    
    return render_template('contactMe.html',contacts=contacts)

# @app.route("/api/contacts")
# def list_contacts():
#     contacts = load_db_contacts()
#     return jsonify(contacts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# print(__name__)
from flask import Flask, render_template,url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aboutMe')
def about():
    return render_template('aboutMe.html')

@app.route('/contactMe')
def contact():
    return render_template('contactMe.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# print(__name__)
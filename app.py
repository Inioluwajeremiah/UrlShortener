from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import string

# create flask app
app = Flask(__name__)

# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorturl.db'
db = SQLAlchemy(app)

# create database class model
class UrlStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longUrl = db.Column(db.String(), unique=True, nullable=False)
    shortUrl = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'Real url => {self.shortUrl} \n Short url => {self.shortUrl}'

with app.app_context():
    db.create_all()

# generate a short url
def generate_short_url():
    letters_digits = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(letters_digits) for _ in range(7))
    url = UrlStore.query.filter_by(shortUrl=short_url).first()
    if  url:
        # If the generated short URL already exists in the database,
        # generate a new one recursively
        return generate_short_url()
    return short_url

# create root for home page
@app.route('/')
def index():
    return render_template("index.html")

# shorten endpoint
@app.route('/shorten', methods=['POST'])
def shorten():
    if request.method == 'POST':
        long_url = request.form['url']
        # check if user inputs long url and url does not exist in database
        if long_url and UrlStore.query.filter_by(longUrl=long_url).first() is None:      
            short_url = generate_short_url()
            url = UrlStore(longUrl=long_url, shortUrl=short_url)
            db.session.add(url)
            db.session.commit()
            return render_template('result.html', short_url = short_url )
        else:
            return render_template("index.html")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


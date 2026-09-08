from datetime import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

from flask_sqlalchemy.session import Session

from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

#Create Tables --- Only needed the first time running
#with app.app_context():
#    db.create_all()

@app.route('/')
def home():  # put application's code here
    return 'Hello World!'

@app.route('/add_author' , methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
            name=request.form.get('name')
            birth_date_str = request.form.get('birth_date')
            date_of_death_str = request.form.get('date_of_death')

            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
            date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

            author = Author(
                name = name,
                birth_date = birth_date,
                date_of_death = date_of_death
            )
            db.session.add(author)
            db.session.commit()
            return f"<p>Author {author.name} added successfully!</p>"
    else:
        return render_template('add_author.html')


if __name__ == '__main__':
    app.run()

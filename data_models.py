from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'Author{self.id}(Name: {self.name}, Birthday: {self.birth_date}, Date of Death: {self.date_of_death})'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Book{self.id}(ISBN: {self.isbn}, Title: {self.title}, Author: {self.author_id} Publication Year: {self.publication_year})'

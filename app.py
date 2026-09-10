from datetime import datetime

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

from flask_sqlalchemy.session import Session
from sqlalchemy import or_

from data_models import db, Author, Book

app = Flask(__name__)
app.secret_key = "ein-geheimer-schluessel-fuer-sessions"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

#Create Tables --- Only needed the first time running
#with app.app_context():
#    db.create_all()

@app.route('/')
def index():
    sort_by = request.args.get("sort")
    search_term = request.args.get("search")
    query = db.session.query(Book)

    if search_term:
        search_filter = f"%{search_term}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_filter),
                Author.name.ilike(search_filter),
                Book.isbn.ilike(search_filter),
            )
        )

    if sort_by == "title":
        query = query.order_by(Book.title)
    elif sort_by == "author":
        query = query.join(Author).order_by(Author.name.asc())
    elif sort_by == "publication_year":
        query = query.order_by(Book.publication_year)

    books = query.all()
    return render_template('home.html', books=books, search_term=search_term)

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
            flash(f"<p>Author {author.name} added successfully!", "success")
            return redirect(url_for('index'))
    else:
        return render_template('add_author.html')

@app.route('/add_book' , methods=['GET', 'POST'])
def add_book():
    result = db.session.query(Author).order_by(Author.name.asc()).all()
    print(result)
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        author_id = request.form.get('author_id')
        publication_year = request.form.get('publication_year')

        book = Book(
            isbn = isbn,
            title = title,
            author_id = author_id,
            publication_year = publication_year
        )
        db.session.add(book)
        db.session.commit()
        flash(f"<p>Book {book.title} added successfully!", "success")
        return redirect(url_for('index'))
    else:
        return render_template('add_book.html', result=result)

@app.route('/delete_book/<int:book_id>' , methods=['POST'])
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if not book:
        flash("Buch nicht gefunden.", "danger")
        return redirect(url_for("index"))

    author_id = book.author_id
    author_name = book.author.name
    book_title = book.title

    # 2. Buch löschen und Transaktion abschließen
    db.session.delete(book)
    db.session.commit()

    # 3. Prüfen, wie viele verbleibende Bücher dieser Autor noch hat und löschen falls keine mehr da sind
    remaining_books_count = (
        db.session.query(Book).filter(Book.author_id == author_id).count()
    )

    if remaining_books_count == 0:
        flash(
            f"Buch „{book_title}“ gelöscht. Hinweis: {author_name} hat nun keine weiteren Bücher im Bestand!",
            "warning",
        )

        author = db.session.get(Author, author_id)
        db.session.delete(author)
        db.session.commit()
    else:
        flash(
            f"Buch „{book_title}“ gelöscht. {author_name} hat noch {remaining_books_count} weiteres/weitere Buch/Bücher im System.",
            "success",
        )

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()

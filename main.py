from flask import Flask, abort, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

all_books = []

class Base(DeclarativeBase):
    pass    

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)

##CREATE TABLE
class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250),nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=False)
    
    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    with app.app_context():
        books=db.session.scalars(db.select(Books).order_by(Books.id)).all()
    print(books)
    return render_template ("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method== "POST":
        with app.app_context():
            new_book = Books(
                title=request.form["title"],
                author=request.form["author"],
                rating=request.form["rating"]
            )
            db.session.add(new_book)
            db.session.commit()
            all_books.append(new_book)
            return redirect(url_for('home'))
        
    return render_template("add.html")

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    book = db.session.get(Books, book_id)
    if book is None:
        abort(404)

    if request.method=="POST":
        book.rating=float(request.form["rating"])
        db.session.commit() 
        return redirect(url_for('home'))

    return render_template("edit.html",book=book)

@app.route("/delete/<int:book_id>", methods=["GET", "POST"])
def delete(book_id):
    book_to_delete = db.get_or_404(Books, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    app.run(debug=True)


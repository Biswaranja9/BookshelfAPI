# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/library_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published_date = db.Column(db.String(10), nullable=False)

# Endpoint 1: Retrieve All Books
@app.route('/api/books', methods=['GET'])
def getall_books():
    try:
        books = Book.query.all()
        book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date} for book in books]
        return jsonify(book_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint 2: Add a New Book
@app.route('/api/books', methods=['POST'])
def addnew_book():
    try:
        data = request.get_json()
        new_book = Book(title=data['title'], author=data['author'], published_date=data['published_date'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint 3: Update Book Details
@app.route('/api/books/<int:id>', methods=['PUT'])
def updatebook_details(id):
    try:
        book = Book.query.get(id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        data = request.get_json()
        book.title = data['title']
        book.author = data['author']
        book.published_date = data['published_date']

        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

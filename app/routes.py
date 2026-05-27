from flask import Blueprint, request, jsonify
from app import db
from app.models import Book

bp = Blueprint('api', __name__)

# 1. Ендпоінт для додавання книги (щоб було що тестувати)
@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Некоректні дані'}), 400
    
    new_book = Book(title=data['title'], author=data['author'], year=data.get('year'))
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

# 2. ОБОВ'ЯЗКОВИЙ ЕНДПОІНТ: GET /books з Limit-Offset пагінацією
@bp.route('/books', methods=['GET'])
def get_books():
    # Отримуємо параметри з URL-запиту, наприклад: /books?limit=10&offset=0
    # Навіть якщо користувач їх не вказав, задаємо значення за замовчуванням: limit=10, offset=0
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    # Валідація параметрів (захист від негативних значень)
    if limit < 0 or offset < 0:
        return jsonify({'error': 'Параметри limit та offset повинні быть позитивними числами'}), 400

    # Запит до БД з використанням методів .offset() та .limit() від SQLAlchemy
    query = Book.query.offset(offset).limit(limit).all()
    
    # Рахуємо загальну кількість книг у базі, щоб клієнт знав, скільки всього сторінок є
    total_books = Book.query.count()

    # Формуємо результат
    books_list = [book.to_dict() for book in query]

    return jsonify({
        'books': books_list,
        'total': total_books,
        'limit': limit,
        'offset': offset
    }), 200
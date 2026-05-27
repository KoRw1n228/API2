import base64
from flask import Blueprint, request, jsonify
from app import db
from app.models import Book

bp = Blueprint('api', __name__)

# 1. Ендпоінт для створення книги (потрібен для наповнення бази перед тестами)
@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Некоректні дані. Поля title та author є обов\'язковими.'}), 400
    
    new_book = Book(title=data['title'], author=data['author'], year=data.get('year'))
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201


# 2. ОНОВЛЕНИЙ ЕНДПОІНТ: GET /books з Cursor-пагінацією
@bp.route('/books', methods=['GET'])
def get_books():
    # Отримуємо ліміт (кількість елементів) та сам курсор з URL-параметрів
    limit = request.args.get('limit', default=10, type=int)
    cursor = request.args.get('cursor', default=None, type=str)

    if limit <= 0:
        return jsonify({'error': 'Параметр limit має бути більшим за 0'}), 400

    # Базовий запит: сортуємо книги за зростанням їхнього унікального первинного ключа (id)
    query = Book.query.order_by(Book.id.asc())

    # Якщо користувач передав маркер курсору, декодуємо його
    if cursor:
        try:
            # Декодуємо рядок з Base64 назад у звичайне число (ID останньої книги)
            decoded_cursor = base64.b64decode(cursor).decode('utf-8')
            last_id = int(decoded_cursor)
            
            # Головна фішка Cursor пагінації: відсікаємо все, що менше або дорівнює цьому ID.
            # База даних робить це миттєво через індекси.
            query = query.filter(Book.id > last_id)
        except Exception:
            return jsonify({'error': 'Некоректний маркер курсору (Invalid cursor)'}), 400

    # Запитуємо на 1 елемент більше, ніж просив клієнт (limit + 1).
    # Це трюк, який дозволяє дізнатися, чи є ще книги на наступній сторінці без зайвого запиту COUNT(*).
    books = query.limit(limit + 1).all()

    # Перевіряємо, чи знайшлося більше книг, ніж наш ліміт
    has_more = len(books) > limit
    next_cursor = None

    if has_more:
        # Якщо є наступна сторінка, відрізаємо той самий "+1" зайвий елемент, щоб повернути рівно стільки, скільки просили
        books = books[:limit]
        
        # Беремо ID найостаннішої книги у поточному відфільтрованому списку
        last_book_id = str(books[-1].id)
        
        # Кодуємо цей ID у формат Base64, щоб віддати клієнту як безпечний маркер
        next_cursor = base64.b64encode(last_book_id.encode('utf-8')).decode('utf-8')

    # Перетворюємо об'єкти книг у список словників (JSON)
    books_list = [book.to_dict() for book in books]

    return jsonify({
        'books': books_list,
        'limit': limit,
        'next_cursor': next_cursor,
        'has_more': has_more
    }), 200
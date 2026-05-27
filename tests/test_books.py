import pytest
from app import create_app, db
from app.models import Book

@pytest.fixture
def client():
    """Фікстура, яка створює тимчасовий додаток та базу даних у пам'яті для кожного тесту"""
    app = create_app()
    app.config['TESTING'] = True
    # Використовуємо SQLite в пам'яті для швидких тестів, щоб не чіпати основну базу
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_pagination(client):
    # 1. Додаємо 5 тестових книг у нашу чисту базу
    for i in range(1, 6):
        client.post('/books', json={'title': f'Book {i}', 'author': f'Author {i}'})

    # 2. Тестуємо першу сторінку: limit=2, offset=0 (маємо отримати Book 1 та Book 2)
    response = client.get('/books?limit=2&offset=0')
    data = response.get_json()
    
    assert response.status_code == 200
    assert len(data['books']) == 2
    assert data['total'] == 5
    assert data['books'][0]['title'] == 'Book 1'
    assert data['books'][1]['title'] == 'Book 2'

    # 3. Тестуємо наступну сторінку: limit=2, offset=2 (маємо отримати Book 3 та Book 4)
    response = client.get('/books?limit=2&offset=2')
    data = response.get_json()
    
    assert response.status_code == 200
    assert len(data['books']) == 2
    assert data['books'][0]['title'] == 'Book 3'
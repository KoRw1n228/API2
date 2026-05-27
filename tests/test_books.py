import pytest
from app import create_app, db
from app.models import Book

@pytest.fixture
def client():
    """Фікстура для створення ізольованої бази даних у пам'яті для тестів"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_cursor_pagination_flow(client):
    # 1. Наповнюємо тимчасову базу 5-ма тестовими книгами
    for i in range(1, 6):
        client.post('/books', json={'title': f'Книга {i}', 'author': f'Автор {i}'})

    # 2. Запитуємо ПЕРШУ сторінку (limit=2, без курсору)
    response = client.get('/books?limit=2')
    data = response.get_json()
    
    assert response.status_code == 200
    assert len(data['books']) == 2
    assert data['has_more'] is True
    assert data['next_cursor'] is not None
    assert data['books'][0]['title'] == 'Книга 1'
    assert data['books'][1]['title'] == 'Книга 2'

    # Зберігаємо маркер для переходу на другу сторінку
    first_page_cursor = data['next_cursor']

    # 3. Запитуємо ДРУГУ сторінку, передаючи отриманий курсор
    response = client.get(f'/books?limit=2&cursor={first_page_cursor}')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data['books']) == 2
    assert data['books'][0]['title'] == 'Книга 3'
    assert data['books'][1]['title'] == 'Книга 4'
    assert data['has_more'] is True
    assert data['next_cursor'] is not None

    second_page_cursor = data['next_cursor']

    # 4. Запитуємо ТРЕТЮ (останню) сторінку
    response = client.get(f'/books?limit=2&cursor={second_page_cursor}')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data['books']) == 1  # Залишилася тільки остання 5-та книга
    assert data['books'][0]['title'] == 'Книга 5'
    # Сторінка остання, тому наступних елементів немає
    assert data['has_more'] is False
    assert data['next_cursor'] is None

def test_invalid_cursor_error(client):
    """Тест на перевірку захисту від битих або неправильних курсорів"""
    response = client.get('/books?limit=2&cursor=not_a_base64_string_123')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Некоректний маркер курсору (Invalid cursor)'
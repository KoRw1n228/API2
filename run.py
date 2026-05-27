from app import create_app

app = create_app()

if __name__ == '__main__':
    # Вказуємо host='0.0.0.0', щоб Flask реагував на запити ззовні Docker-контейнера
    app.run(host='0.0.0.0', port=5000, debug=True)
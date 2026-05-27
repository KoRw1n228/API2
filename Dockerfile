# Використовуємо офіційний легкий образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл із залежностями
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . .

# Відкриваємо порт 5000 для доступу до Flask
EXPOSE 5000

# Команда для запуску нашого додатку
CMD ["python", "run.py"]
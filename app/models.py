from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        """Метод для зручної конвертації об'єкта книги в JSON-формат"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year
        }
from apps import db
from apps.base import BaseModel


class Blog(BaseModel):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    thumbnail = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    def __repr__(self):
        return f"<Blog {self.title}>"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "thumbnail": self.thumbnail,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "category_id": self.category_id,
            "author_id": self.author_id,
        }

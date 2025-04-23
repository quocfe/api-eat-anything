from apps import db
from apps.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'blog' or 'project'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    blogs = db.relationship("Blog", backref="category", lazy=True)
    projects = db.relationship("Project", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name} ({self.type})>"

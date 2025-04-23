from apps import db
from apps.base import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    slug = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(500))
    thumbnail = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(500), nullable=True)
    year = db.Column(db.String(8), nullable=True)
    customer = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    items = db.relationship(
        "ProjectItem",
        backref="project",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<Project {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "thumbnail": self.thumbnail,
            "content": self.content,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat(),
        }


def serialize_project(project: Project):
    return {
        "id": project.id,
        "image": project.thumbnail or "/project_card.png",
        "name": project.name,
        "title": project.name or "",
        "category": project.category.name if project.category else "UNKNOWN",
        "detailBlocks": [
            {
                "image": item.image,
                "description": item.description,
            }
            for item in project.items
        ],
    }

from apps import db
from apps.base import BaseModel


class ProjectItem(BaseModel):
    __tablename__ = "projectItem"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String(500), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<ProjectItem {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "image": self.image,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat(),
        }

from apps.base_repository import BaseRepository
from apps.project.models import Project


class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)

    def get_by_category(self, category_id):
        try:
            return self.model.query.filter_by(category_id=category_id).all()
        except Exception as e:
            print("Error in get_by_category:", e)
            return []

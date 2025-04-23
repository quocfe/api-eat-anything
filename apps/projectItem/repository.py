from apps.base_repository import BaseRepository
from .models import ProjectItem


class ProjectItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProjectItem)

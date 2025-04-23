from apps.base_repository import BaseRepository
from apps.blog.models import Blog


class BlogRepository(BaseRepository):
    def __init__(self):
        super().__init__(Blog)

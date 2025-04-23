from apps.auth.models import Users
from apps.base_repository import BaseRepository


class AuthRepository(BaseRepository):
    def __init__(self):
        super().__init__(Users)

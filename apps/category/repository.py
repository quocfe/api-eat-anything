from apps.base_repository import BaseRepository
from apps.category.models import Category


class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(Category)

    def get_all_categories_by_type(self, type_):
        try:
            return Category.query.filter_by(type=type_).all()
        except Exception as e:
            print("Error in get_all_categories_by_type:", e)
            return []

from apps import db
from flask_sqlalchemy import Pagination


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        try:
            return self.model.query.all()
        except Exception as e:
            print(f"[{self.model.__name__}] Error in get_all:", e)
            return []

    def get_by_id(self, item_id):
        try:
            return self.model.query.get(item_id)
        except Exception as e:
            print(f"[{self.model.__name__}] Error in get_by_id:", e)
            return None

    def create(self, data):
        try:
            item = self.model(**data)
            item.save()
            return item
        except Exception as e:
            db.session.rollback()
            print(f"[{self.model.__name__}] Error in create:", e)
            raise e

    def update(self, data):
        try:
            # accept dict
            if isinstance(data, dict):
                item_id = data.get("id")
                if not item_id:
                    return {"msg": "ID is required for update", "status": "error"}

                item = self.get_by_id(item_id)
                if not item:
                    return {"msg": "Item not found", "status": "error"}

                for key, value in data.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
            # accept instance
            else:
                item = data
            item.save()
            return data
        except Exception as e:
            db.session.rollback()
            print(f"[{self.model.__name__}] Error in update:", e)
            raise e

    def delete(self, item_id):
        try:
            item = self.get_by_id(item_id)
            if not item:
                return {"msg": "Item not found", "status": "error"}

            item.save()
            return {"msg": "Deleted successfully", "status": "success"}
        except Exception as e:
            db.session.rollback()
            print(f"[{self.model.__name__}] Error in delete:", e)
            raise e

    def get_paginated(self, page=1, per_page=10, order_by=None, filters=None):
        try:
            query = self.model.query

            if filters:
                for f in filters:
                    query = query.filter(f)

            if order_by:
                query = query.order_by(order_by)

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            return pagination

        except Exception as e:
            print(f"[{self.model.__name__}] Error in get_paginated: {e}")
            return Pagination(
                query=self.model.query, page=page, per_page=per_page, total=0, items=[]
            )

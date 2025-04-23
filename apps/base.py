from . import db


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            else:
                db.session.merge(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error in save:", e)
            raise (e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error in delete:", e)
            raise (e)

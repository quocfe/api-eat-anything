from .models import Category
from apps import db
from apps.utils import slugify


def get_all_categories():
    try:
        return Category.query.all()
    except Exception as e:
        print("Error in get_all_categories:", e)
        return []


def get_all_categories_by_type(type_):
    try:
        return Category.query.filter_by(type=type_).all()
    except Exception as e:
        print("Error in get_all_categories_by_type:", e)
        return []


def get_category_by_id(category_id):
    try:
        return Category.query.get(category_id)
    except Exception as e:
        print("Error in get_category_by_id:", e)
        return None


def create_category(name, type_):
    try:
        new_cat = Category(
            name=name,
            type=type_,
            slug=slugify(name),
            created_at=db.func.current_timestamp(),
            updated_at=db.func.current_timestamp(),
        )
        db.session.add(new_cat)
        db.session.commit()
        return new_cat
    except Exception as e:
        db.session.rollback()
        print("Error in create_category:", e)
        raise


def update_category(category_id, name, type_):
    try:
        cat = Category.query.get(category_id)
        if cat:
            cat.name = name
            cat.type = type_
            cat.slug = slugify(name)
            cat.updated_at = db.func.current_timestamp()
            db.session.commit()
        return cat
    except Exception as e:
        db.session.rollback()
        print("Error in update_category:", e)
        raise


def delete_category(category_id):
    try:
        cat = Category.query.get(category_id)
        if cat:
            db.session.delete(cat)
            db.session.commit()
        return cat
    except Exception as e:
        db.session.rollback()
        print("Error in delete_category:", e)
        raise

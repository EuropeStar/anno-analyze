from numpy import array
from sqlalchemy import func
from app.configs import VECTOR_SEPARATOR
from app.models import User, db


def build_dataset(usr_list):
    return array(list(
        map(lambda x: list(map(int, x.sparse_vector.split(VECTOR_SEPARATOR))),
        usr_list)
    ))

def build_user_ids(usr_list):
    return list(
        map(lambda x: x.id, usr_list)
    )


def get_random_user(exclude_id):
    return db.session\
        .query(User)\
        .filter(User.id.notin_((exclude_id,)))\
        .order_by(func.random())\
        .first()


def get_recommend_user_list(cluster_index, exclude_id):
    return db.session\
        .query(User)\
        .filter_by(cluster_index=int(cluster_index))\
        .filter(User.id.notin_((exclude_id,)))\
        .order_by(func.random())\
        .limit(10)\
        .all()
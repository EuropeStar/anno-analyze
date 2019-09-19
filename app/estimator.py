from sklearn.cluster import MeanShift
from app.models import User, ClusterInfo, db
from app.db_utls import build_dataset, build_user_ids, get_random_user, get_recommend_user_list
from dataset_builder import DataSetCreator
from app.configs import REQUIRE_REBUILD_CONST


ESTIMATOR = None


def estimate_bandwidth(data):
    pass


def check_required_rebuild():
    info = db.session.query(ClusterInfo).first()
    usrs = db.session.query(User).count()
    return info.users * (1 + REQUIRE_REBUILD_CONST) < usrs


def teach(use_help_data_set=False):
    if use_help_data_set:
        X = DataSetCreator(1500).create_data_set()
    else:
        usr_list = db.session.query(User).all()
        X = build_dataset(usr_list)
    ms = MeanShift(bandwidth=estimate_bandwidth(X))
    ms.fit(X)
    return ms


def reindex_users(ms):
    usrs = db.session.query(User).all()
    clstrs = set()
    for x in usrs:
        [indx] = ms.predict(build_dataset([x]))
        x.cluster_index = int(indx)
        clstrs.add(int(indx))
        db.session.add(x)
        db.session.commit()
    cl_info = db.session.query(ClusterInfo).get(1)
    if cl_info is None:
        cl_info = ClusterInfo(id=1)
    cl_info.clusters_count = len(clstrs)
    cl_info.users = len(usrs)
    db.session.add(cl_info)
    db.session.commit()


def get_estimator():
    global ESTIMATOR
    if not ESTIMATOR or check_required_rebuild():
        ESTIMATOR = teach(True)
        reindex_users(ESTIMATOR)
    return ESTIMATOR


def predict_for(user_id):
    usr = db.session.query(User).get(user_id)
    ms = get_estimator()
    [clst_indx] = ms.predict(build_dataset([usr]))
    if clst_indx is not None:
        usr.cluster_index = int(clst_indx)
        db.session.add(usr)
        db.session.commit()
        found_users = get_recommend_user_list(clst_indx, user_id)
        if not found_users:
            found_users = get_random_user(user_id)
            found_users = [found_users] if found_users else []
        return build_user_ids(found_users)
    return build_user_ids([get_random_user(user_id)])

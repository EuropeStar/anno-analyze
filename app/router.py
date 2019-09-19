from flask import jsonify, Blueprint
from app.decorators import validate_params
from app.estimator import predict_for
from app.models import User, db
from app.analyzer import analyze_for_user


analyzer = Blueprint('analyzer', __name__)


@analyzer.route('/recommend', methods=['POST'])
@validate_params(userID=int)
def get_similar_users(**kwargs):
    user_id = kwargs['userID']
    if db.session.query(User).get(user_id) is None:
        return jsonify({"success": False, "error": "User does not exists with ID: %s" % user_id})
    data = predict_for(user_id)
    return jsonify({
        "success": True,
        "userIDs": ",".join(list(map(str, data)))
    })


@analyzer.route('/sign-up', methods=['POST'])
@validate_params(userID=int, vector=str)
def register_new_user(**kwargs):
    user = User(id=kwargs['userID'], sparse_vector=kwargs['vector'])
    if db.session.query(User).get(user.id) is not None:
        return jsonify({"success": False, "error": "User with ID: %s already exists" % user.id})
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": True})


@analyzer.route('/analyze', methods=['POST'])
@validate_params(userID=int, text=str)
def analyze_user_dialog(**kwargs):
    analyze_for_user(kwargs['userID'], kwargs['text'])
    return jsonify({'success': True})

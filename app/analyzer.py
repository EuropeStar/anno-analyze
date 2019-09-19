import requests
from app.decorators import required_to_evaluate
from app.models import User, db
from app.configs import API_URL, API_TOKEN, VECTOR_SEPARATOR, RANGE, CHANGE_STEP
from app.categories import ACTIVE_CATEGORIES


def analyze_for_user(user_id, text):
    user = User.query.get_or_404(user_id)
    tsp = TextSemanticParser(text, API_TOKEN, API_URL)
    titles, categories = tsp.extract_entities()
    vHandler = VectorUpdateHandler(user.sparse_vector, categories, titles)
    newV = vHandler.get_updated_vector()
    user.sparse_vector = newV
    db.session.add(user)
    db.session.commit()


class VectorUpdateHandler:
    """
    Class for update user vector based on incoming categories
    """
    def __init__(self, vector, in_cats=None, titles=None):
        """
        :param vector: can be a string of int (1029341) or list of ints
        :param in_cats: list of words
        """
        if not vector:
            raise ValueError('Vector should be provided!')
        self.vector = self._extract_vector(vector)
        self.computed_titles = in_cats or []
        self.computed_cats_list = titles or []

    @staticmethod
    def _extract_vector(vector):
        if isinstance(vector, str):
            return vector.split(VECTOR_SEPARATOR)
        return vector

    @staticmethod
    def item_in_list(item, search_list):
        return any(filter(lambda x: x.lower().find(item.lower()) != -1, search_list))

    def active_category_noticed(self, category):
        sub = category.lower()
        # check only categories titles
        if self.item_in_list(sub, self.computed_cats_list):
            return True
        # continue to search deeply
        for x in self.computed_titles:
            if self.item_in_list(sub, x):
                return True
        # nothing found
        return False

    def get_change_vector(self):
        change_vector = []
        for cat_title, cat_related in ACTIVE_CATEGORIES.items():
            val = -1
            if self.active_category_noticed(cat_title) or any(filter(self.active_category_noticed, cat_related)):
                val = CHANGE_STEP
            change_vector.append(val)
        return change_vector

    @staticmethod
    def _sum_of(prev, plus):
        if RANGE[0] <= prev + plus <= RANGE[1]:
            return prev + plus
        return prev

    @required_to_evaluate
    def get_updated_vector(self, to_string=True):
        _change_vector = self.get_change_vector()
        out = []
        if len(self.vector) < len(_change_vector):
            raise ValueError("Current vector len is less than update_vector")
        for i in range(len(_change_vector)):
            val = int(self.vector[i])
            out.append(self._sum_of(val, _change_vector[i]))
        return ",".join((str(x) for x in out)) if to_string else out


class TextSemanticParser:

    def __init__(self, text, token, api_url):
        self._token = token
        self._text = text
        self._api_url = api_url

    def extract_entities(self, text=None):
        if not text and not self._text:
            raise ValueError("text not provided")
        resp = self._make_request(self._text or text)
        if resp.status_code == 200:
            resp = resp.json()
            annotations = resp.get('annotations')
            titles = self._extract(annotations, 'title')
            types = self._extract(annotations, 'categories')
            return titles, types

    @staticmethod
    def _extract(annotation_list, selector):
        return [x.get(selector, None) for x in annotation_list]

    def _make_request(self, text):
        data = {
            "text": text,
            "token": self._token,
            "include": 'categories'
        }
        return requests.get(self._api_url, params=data)

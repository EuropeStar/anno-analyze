from flask import request, Response
from functools import wraps


"""
Decorator, checks required data contains in 
request json POST data. Checks its type 
"""
def validate_params(**kwargs):
    def forward_user_data(view):
        @wraps(view)
        def wrapper():
            data = request.get_json()
            if not data:
                return Response('No json body provided', status=400)
            try:
                for x in kwargs.keys():
                    if not data.get(x, False) or kwargs[x] != type(data[x]):
                        raise ValueError("Parameter \"%s\" is not provided or "
                                         "it's type is not march: required \"%s\"" % (x, kwargs[x].__name__))
            except ValueError as e:
                return Response(str(e), status=400)
            return view(**data)
        return wrapper
    return forward_user_data


def required_to_evaluate(fn):
    def wrapper(scope, to_string=True):
        if getattr(scope, 'computed_cats_list', False) or getattr(scope, 'computed_titles', False):
            return fn(scope, to_string)
        return ",".join((str(x) for x in scope.vector)) if to_string else scope.vector
    return wrapper
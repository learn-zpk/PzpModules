from flask.json import JSONEncoder


class FlaskJsonEncoder(JSONEncoder):
    """set to json encoder implement
    """

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, tuple):
            return list(obj)
        return JSONEncoder.default(self, obj)


def init(app):
    app.json_encoder = FlaskJsonEncoder

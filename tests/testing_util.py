import json
from collections import namedtuple


class TestingUtil:
    @classmethod
    def __json_object_hook(cls, d): return namedtuple('X', d.keys())(*d.values())

    @classmethod
    def json2obj(cls, data): return json.loads(data, object_hook=cls.__json_object_hook)

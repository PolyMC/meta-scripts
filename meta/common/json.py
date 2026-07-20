import ujson as _ujson

dump = _ujson.dump
load = _ujson.load
loads = _ujson.loads


def dumps(obj, **kwargs):
    kwargs.setdefault("escape_forward_slashes", False)
    return _ujson.dumps(obj, **kwargs)

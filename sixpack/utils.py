import json
import re

import decorator
from redis import ConnectionError
from werkzeug.wrappers import Response


@decorator.decorator
def service_unavailable_on_connection_error(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except ConnectionError:
        return json_error({"message": "redis is not available"}, None, 503)

def json_error(resp, request, status=None):
    default = {'status': 'failed'}
    resp.update(default)

    return _json_resp(resp, request, status)


def json_success(resp, request):
    default = {'status': 'ok'}
    resp.update(default)

    return _json_resp(resp, request, 200)  # Always a 200 when success is called


def _json_resp(in_dict, request, status=None):
    print(in_dict)
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(in_dict)
    callback = request and request.args.get('callback')
    print(callback)
    if callback and re.match(r"^\w[\w'\-\.]*$", callback):
        headers["Content-Type"] = "application/javascript"
        data = "%s(%s)" % (callback, data)

    return Response(data, status=status, headers=headers)


def number_to_percent(number, precision=2):
    return "%.2f%%" % round(number * 100, precision)


def number_format(number):
    return "{:,}".format(number)

def to_bool(val):
    return val.lower() in ['y', 'true', 'yes']

def regex_replace(s, find, replace):
    return re.sub(find, replace, s)

def sanitize_experiment(experiment):
    matches = re.findall(r"\w+", experiment)
    return "-".join(matches)

def decode_if_bytes(data: str) -> str:
    if isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        return data

def validate_required_args_and_get_body(required_args: list, request_body_json: dict) -> str:
    pass
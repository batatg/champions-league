import functools
import datetime
from decimal import Decimal
from flask import jsonify
from flask_jsontools import DynamicJSONEncoder
from werkzeug.exceptions import UnprocessableEntity


def query_result_handler(success_status_code=200, error_status_code=500):
    def result_hanlderf(f):
        @functools.wraps(f)
        def f_result_hanlder(*args, **kwargs):
            return_value = {}
            try:
                result = f(*args, **kwargs)
                #add success
                return_value["data"] = result
                return jsonify(return_value), success_status_code
                # return result
            #webargs exception
            except UnprocessableEntity as e:
                return_value["error"] = e.exc.messages
                return jsonify(return_value), e.code
            #buisness exception
            except Exception as e:
                message = e.description if hasattr(e, "description") else str(e)
                return_value["error"] = message
                status_code = e.status_code if hasattr(e, "status_code") else e.code if hasattr(e, "code") else error_status_code
                return jsonify(return_value), status_code
        return f_result_hanlder
    return result_hanlderf


class ApiJSONEncoder(DynamicJSONEncoder):
    def default(self, obj):
        # Custom formats
        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S")

        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        return super(ApiJSONEncoder, self).default(obj)
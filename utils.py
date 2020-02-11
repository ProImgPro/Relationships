from flask import jsonify
from webargs.flaskparser import FlaskParser
from marshmallow import fields
import re

parser = FlaskParser()


def parse_req(argmap):
    """

    :param argmap:
    :return:
    """
    return parser.parse(argmap)


def send_result(data=None, message="OK", code=200, status=True):
    """
    Args:
        data: simple result object like dict, string or list
        message: message send to client, default = OK
        code: code default = 200
        version: version of api
    :param data:
    :param message:
    :param code:
    :param version:
    :param status:
    :return:
    json rendered sting result
    """
    res = {
        "jsonrpc": "2.0",
        "status": status,
        "code": code,
        "message": message,
        "data": data,
    }

    return jsonify(res), 200


# class FieldString(fields.String):
#     """
#         validate string field, max length = 1024
#         Args:
#             des:
#
#         Return:
#     """
#
#     DEFAULT_MAX_LENGTH = 1024  # 1 kB
#
#     def __init__(self, validate=None, requirement=None, **metadata):
#         """
#
#         :param validate:
#         :param requirement:
#         :param metadata:
#         """
#         if validate is None:
#             validate = validate.Length(max=self.DEFAULT_MAX_LENGTH)
#         if requirement:
#             validate= validate.Noneof(error='Invalid Input', iterable={'full_name'})
#         super(FieldString, self).__init__(validate=validate, required=requirement, **metadata)


def check_email1(str_email):
    return re.match(
        r"^[A-Za-z0-9]*[A-Za-z]+[A-Za-z0-9]*(\.)[A-Za-z]+(@)(BOOT|BOOt|BOot|Boot|boot|booT|boOT|bOOT|bOOt|bOot|boOt|bOoT|BoOT|BOoT|BooT|BoOt)(\.)(ai|AI|Ai|aI)$",
        str_email)


def check_email2(str_email):
    return re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', str_email)

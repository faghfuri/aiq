import typing
import json


def generateUpdateStatement(base: typing.Dict, mutation: typing.Dict) -> typing.Dict:
    """
    generateUpdateStatement translates a mutation to a request understandable by DBMS.
    Suported actions in mutation are:
    - Update: e.g. { "posts": [{"_id": 2, "value": "too"}] }
    - Append: e.g. { "posts": [{"value": "four"}] }
    - Remiove: e.g. { "$remove" : {"posts.0" : true} }
    Returns:
        Output would be a DBMS command dictionary that will use any of the valid
    command ($add, $remove or $update)
    Excetption:
        Will raise aiq.Exception
    """
    return {}

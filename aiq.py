from collections import defaultdict
import typing
import json
import logging


class Error(Exception):
    pass


MENTION_FIELDS = ['text']


def generateUpdateStatement(base: typing.Dict, mutation: typing.Dict) -> typing.Dict:
    """
    generateUpdateStatement translates a mutation to a request understandable by DBMS.
    Suported actions in mutation are:
    - Update: e.g. { "posts": [{"_id": 2, "value": "too"}] }
    - Append: e.g. { "posts": [{"value": "four"}] }
    - Remive: e.g. { "posts": [{"_id": 2, "_delete": true}] }
    Returns:
        Output would be a DBMS command dictionary that will use any of the valid
    command ($add, $remove or $update)
    Excetption:
        Will raise aiq.Exception
    """
    # Return if no mutation is requested, and throw an expection if the
    # object is invalid.
    if not mutation.get('posts'):
        return {}

    post_indexes = generate_post_indexes(base)
    cmds = {
        "$add": defaultdict(list),
        "$remove": defaultdict(dict),
        "$update": defaultdict(dict),
    }

    for post in mutation['posts']:
        if post.get('_id'):
            post_index = post_indexes[post['_id']]
            if post.get('_delete'):
                cmds['$remove'][f'posts.{post_index}'] = True
                continue

            # Post level updates:
            if post.get('value'):
                cmds['$update'][f'posts.{post_index}.value'] = post['value']
            # Mention level updates:
            if post.get('mentions'):
                mention_mutations(
                    cmds, base['posts'][post_index], post['mentions'], post_index)
            continue

        cmds['$add']['posts'].append(post)

    return cleanup(cmds)


def mention_mutations(cmds, base_post, mutation: typing.Dict, post_index: int):
    """mention_mutations: processes mention level mutations
    e.g. {'_id': 6, '_delete': True} will generate {"$remove": {"posts.1.mentions.1": true}}
    """
    # Generate mention index for the current post:
    indexes = {}
    if base_post.get('mentions'):
        for index, mention in enumerate(base_post['mentions']):
            indexes[mention['_id']] = index

    for mention in mutation:
        # If mention has an _id, it should either be updated or deleted:
        if mention.get('_id'):
            mention_index = indexes[mention['_id']]
            # If a mention has deleted field, we ignore rest of its fields.
            if mention.get('_delete'):
                cmds['$remove'][f'posts.{post_index}.mentions.{mention_index}'] = True
                continue

            # Basically copy all the fields.
            # TODO: Compare with the existing data and don't update current fields.
            for key in MENTION_FIELDS:
                if mention.get(key):
                    update_cmd = f'posts.{post_index}.mentions.{mention_index}.{key}'
                    cmds['$update'][update_cmd] = mention[key]
            continue

        # If mention has no _id, it means, we need to add this to the post.
        cmds['$add'][f'posts.{post_index}.mentions'].append(mention)


def cleanup(cmds: typing.Dict) -> typing.Dict:
    """cleanup cleans up the commands that will be sent to DBMS"""
    empty_keys = []
    for key, value in cmds.items():
        if not value:
            empty_keys.append(key)
    for key in empty_keys:
        cmds.pop(key)
    return cmds


def generate_post_indexes(base: typing.Dict) -> typing.Dict[int, int]:
    """generate_post_indexes returns a map of post id to index"""
    res = {}
    for index, post in enumerate(base['posts']):
        res[post['_id']] = index
    return res

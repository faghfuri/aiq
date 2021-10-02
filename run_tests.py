import json
import os
import sys
import typing

import aiq


def format_dict(d: typing.Dict) -> str:
    """return a multi-line string representation of the dict"""
    return json.dumps(d, indent="  ", sort_keys=True)


if __name__ == '__main__':
    base = json.load(open('testdata/base.json'))
    for test in range(7):
        print(f'Running test #{test}')
        mutation = json.load(open(f'testdata/input_{test}.json'))
        want = format_dict(json.load(open(f'testdata/output_{test}.json')))
        try:
            got = format_dict(aiq.generateUpdateStatement(base, mutation))
        except Exception as e:
            print(f'Test for test #{test}:')
            print(f'  generateUpdateStatement() failed with {e}')
            print('  Mutation:\n', json.dumps(mutation, indent="  "))
            sys.exit(os.EX_SOFTWARE)

        if got != want:
            print(f'Test for test #{test}:')
            print('Mutation:\n', json.dumps(mutation, indent="  "))
            print('Want:\n', json.dumps(want, indent="  "))
            print('Got:\n', json.dumps(got, indent="  "))
            sys.exit(os.EX_SOFTWARE)

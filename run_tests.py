import sys
import json
import os

import aiq


if __name__ == '__main__':
    base = json.load(open('testdata/base.json'))
    for test in range(2):
        mutation = json.load(open(f'testdata/input_{test}.json'))
        want = json.load(open(f'testdata/output_{test}.json'))
        got = aiq.generateUpdateStatement(base, mutation)
        if got != want:
            print(f'Test for test #{test}:')
            print('Mutation:\n', json.dumps(mutation, indent="  "))
            print('Want:\n', json.dumps(want, indent="  "))
            print('Got:\n', json.dumps(got, indent="  "))
            sys.exit(os.EX_OSERR)

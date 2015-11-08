import live
import json
import sys

# live.clear()


def diff_data(x, y):
    if x == y:
        return None, None
    elif type(x) != type(y):
        return x, y
    elif isinstance(x, dict):
        return {
            key: diff_data(x.get(key), y.get(key))
            for key in set(x.keys()) | set(y.keys())
        }
    elif isinstance(x, list):
        diff = [diff_data(xi, yi) for xi, yi in zip(x, y)]
        if len(x) > len(y):
            for i in range(len(y), len(x)):
                diff.append((x, None))
        elif len(x) < len(y):
            for i in range(len(x), len(y)):
                diff.append((None, y))
        return diff


def print_data(data):
    return json.dumps(data, indent=4, sort_keys=True)


@live.once
def test_example():
    x = {
        'a': [1, 2, 3, 4],
        'b': 0,
        'c': 'qwer',
    }

    y = {
        'a': [1, 3, 5],
        'b': 'asdf',
        'd': None,
    }

    print('x = {}'.format(print_data(x)))
    print('y = {}'.format(print_data(x)))
    print('x - y = {}'.format(print_data(diff_data(x, y))))


# @live.always
def print_dot():
    sys.stderr.write('.')
    sys.stderr.flush()


live.log('__name__ = {}\n'.format(__name__))
live.log('DEBUG DEBUG DEBUG\n')


sys.stderr.write('live = {}'.format(dir()))
sys.stderr.flush()

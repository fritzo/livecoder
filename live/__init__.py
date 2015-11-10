import functools
import os
import pep8
import pyflakes.api
import pytest
import re
import sys
import time
import traceback

# Python 2/3 shim for reload.
try:
    reload
except NameError:
    from imp import reload

__all__ = ['log', 'keep', 'clear', 'once', 'always', 'cached']

FRAMERATE_HZ = 60


def log(message):
    sys.stderr.write('LIVE {}\n'.format(message))
    sys.stderr.flush()


def log_debug(message):
    sys.stderr.write('DEBUG {}\n'.format(message))
    sys.stderr.flush()


def log_error(message):
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb)
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]
    sys.stderr.write('ERROR {}\n'.format(message))
    if isinstance(message, Exception):
        sys.stderr.write('  {}\n'.format(type(message)))
    sys.stderr.write('  in {}:{} {}\n'.format(filename, line, func))
    sys.stderr.write('  {}\n'.format(text))
    sys.stderr.flush()


def import_module_by_path(path):
    path = os.path.relpath(path)
    assert os.path.exists(path), path
    assert path.endswith('.py'), path
    module_name = path[:-3].replace(os.sep, '.')
    log_debug('Importing {}'.format(module_name))
    module = __import__(module_name)
    return module


def name_of_function(fun):
    assert callable(fun), fun
    return '{}.{}'.format(fun.__module__, fun.__name__)


class State:
    def __init__(self):
        self.keep = object()
        self.cache = {}
        self.once = {}
        self.once_done = set()
        self.always = {}


_state = State()
keep = _state.keep


def _clear_all():
    for key in dir(keep):
        if not key.startswith('__'):
            delattr(keep, key)
    _state.once.clear()
    _state.once_done.clear()
    _state.always.clear()
    _state.cached.clear()


def _clear_if(pred):
    for key in dir(keep):
        if pred(key) and not key.startswith('__'):
            delattr(keep, key)
    for key in filter(pred, _state.once.keys()):
        del _state.once[key]
    for key in filter(pred, _state.once_done):
        _state.once_done.remove(key)
    for key in filter(pred, _state.always.keys()):
        del _state.always[key]
    for key in filter(pred, _state.cached.keys()):
        del _state.cached[key]


def clear(pattern=None):
    if pattern is None:
        _clear_all()
    else:
        try:
            pred = re.compile(pattern).match
        except Exception as e:
            log_error(e)
            return
        _clear_if(pred)


def cached(fun):
    cache = _state.cache.setdefault(name_of_function(fun), {})

    @functools.wraps(fun)
    def cached_fun(*args, **kwargs):
        key = tuple(args) + tuple(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = fun(*args, **kwargs)
        return cache[key]

    return cached_fun


def once(fun):
    assert callable(fun), fun
    _state.once[name_of_function(fun)] = fun
    return fun


def always(fun):
    assert callable(fun), fun
    _state.always[name_of_function(fun)] = fun
    return fun


def _tick():
    for name in _state.once.keys():
        if name not in _state.once_done:
            try:
                _state.once[name]()
                _state.once_done.add(name)
            except Exception as e:
                log_error(e)
        _state.once.clear()
    for name in list(_state.always.keys()):
        try:
            _state.always[name]()
        except Exception as e:
            del _state.always[name]
            log_error(e)


pytest_status_ok = [
    None,
    0,  # EXIT_OK
    5,  # EXIT_NOTESTSCOLLECTED
]


def _reload(script_path, module=None):
    script_path = os.path.realpath(script_path)
    try:
        log_debug('Running static analysis (pyflakes)')
        reporter = pyflakes.reporter._makeDefaultReporter()
        warnings = pyflakes.api.checkPath(script_path, reporter)
        assert warnings == 0, 'Failed static analysis'
        log_debug('Running tests (pytest)')
        status = pytest.main('-vx {}'.format(script_path))
        assert status in pytest_status_ok, 'Failed tests ({})'.format(status)
        log_debug('Checking style (pep8)')
        pep8._main()
        if module is None:
            log_debug('Loading')
            module = import_module_by_path(script_path)
        # Some things only get called on reload.
        log_debug('Reloading')
        return reload(module)
    except Exception as e:
        log_error(e)
        return module


class Reloader:
    def __init__(self, script_path):
        script_path = os.path.realpath(script_path)
        assert os.path.exists(script_path), script_path
        self.script_path = script_path
        self.mtime = 0
        self.module = None

    def update(self):
        # This allows for temporary unavailability of the edited file.
        if os.path.exists(self.script_path):
            mtime = os.stat(self.script_path).st_mtime
            if mtime != self.mtime:
                self.mtime = mtime
                self.module = _reload(self.script_path, self.module)


def main(script_path, framerate_hz=FRAMERATE_HZ):
    reloader = Reloader(script_path)
    while True:
        start = time.time()
        reloader.update()
        _tick()
        stop = time.time()
        sleep_duration = max(0.0, start - stop + 1.0 / framerate_hz)
        if sleep_duration > 0:
            time.sleep(sleep_duration)

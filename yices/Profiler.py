"""Profiler is for measuring how much time (nanoseconds) spent in the Yices shared library."""

import functools

import time

from .StringBuilder import StringBuilder

def profile(func):
    """Record the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        if Profiler.is_enabled():
            start = time.perf_counter_ns()
            value = func(*args, **kwargs)
            stop = time.perf_counter_ns()
            Profiler.delta(func.__name__, start, stop)
            return value
        return func(*args, **kwargs)
    return wrapper_timer


class Profiler:

    __enabled = True

    """maps (yices API) function names to the total accumulated time spent within them."""
    __line_items = {}

    """keeps track of the total time spent in the shared library."""
    __total = 0

    __max_len = 0

    @staticmethod
    def set_enabled(value):
        Profiler.__enabled = bool(value)


    @staticmethod
    def is_enabled():
        return Profiler.__enabled

    @staticmethod
    def get_time(fname):
        return Profiler.__line_items.get(fname, 0)

    @staticmethod
    def delta(fname, start, stop):
        nanos = stop - start
        Profiler.__total += nanos
        if Profiler.__max_len < len(fname):
            Profiler.__max_len = len(fname)
        if fname in Profiler.__line_items:
            Profiler.__line_items[fname] += nanos
        else:
            Profiler.__line_items[fname] = nanos

    @staticmethod
    def dump():
        def percent(nanos):
            return (nanos * 100) // Profiler.__total
        def pad(fname):
            return ' ' * (Profiler.__max_len - len(fname))
        sb = StringBuilder()
        sb.append('\nYices API Call Profile:\n')
        for fname, cost in Profiler.__line_items.items():
            pc = percent(cost)
            if pc > 0:
                sb.append(f'\t{fname}{pad(fname)}\t\t{pc}%\n')
        sb.append(f'\n\tTotal:{pad("Total:")}\t\t{int(Profiler.__total / 10e6)} milliseconds\n')
        return str(sb)

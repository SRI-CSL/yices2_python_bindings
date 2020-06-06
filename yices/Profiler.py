"""Profiler is for mesuring how much time (nanoseconds) spent in the Yices shared library."""

from .StringBuilder import StringBuilder

class Profiler:

    __enabled = True

    """maps (yices API) function names to the total accumulated time spent within them."""
    __line_items = {}


    @staticmethod
    def set_enabled(value):
        Profiler.__enabled = bool(value)


    @staticmethod
    def is_enabled():
        return Profiler.__enabled


    @staticmethod
    def delta(fname, start, stop):
        nanos = stop - start
        if fname in Profiler.__line_items:
            Profiler.__line_items[fname] += nanos
        else:
            Profiler.__line_items[fname] = nanos

    @staticmethod
    def dump():
        sb = StringBuilder()
        sb.append('\n')
        for fname, cost in Profiler.__line_items.items():
            sb.append(f'{fname}\t\t{cost}\n')
        return str(sb)

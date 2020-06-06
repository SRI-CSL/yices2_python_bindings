"""Profiler is for mesuring how much time (nanoseconds) spent in the Yices shared library."""

from .StringBuilder import StringBuilder

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
        sb.append('\n')
        for fname, cost in Profiler.__line_items.items():
            pc = percent(cost)
            if pc > 0:
                sb.append(f'{fname}{pad(fname)}\t\t{pc}%\n')
        sb.append(f'\nTotal:{pad("Total:")}\t\t{int(Profiler.__total / 10e6)} milliseconds\n')
        return str(sb)

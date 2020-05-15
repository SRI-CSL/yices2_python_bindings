import yices_api as yapi

class Yices:

    version = yapi.yices_version

    build_arch = yapi.yices_build_arch

    build_mode = yapi.yices_build_mode

    build_date = yapi.yices_build_date

    @staticmethod
    def has_mcsat():
        """Return true if the underlying libyices has been compiled with mcsat support, false otherwise."""
        return yapi.yices_has_mcsat() == 1

    @staticmethod
    def is_thread_safe():
        """Return true if the underlying libyices has been compiled with thread safety enabled, false otherwise."""
        return yapi.yices_is_thread_safe() == 1


    # new in 2.6.2
    @staticmethod
    def has_delegate(delegate):
        """Returns True if the underlying libyices has been compiled with the given delegate supported.

        Valid delegates are "cadical", "cryptominisat", and "y2sat".
        """
        return yapi.yices_has_delegate(delegate) == 1

    @staticmethod
    def error_code():
        """Return the last error code, see yices_types.h for a full list."""
        return yapi.yices_error_code()

    @staticmethod
    def error_string():
        """Returns a string explaining the last error."""
        return yapi.yices_error_string()

    @staticmethod
    def error_report():
        """Return the latest error report, see yices.h."""
        return yapi.yices_error_report()

    @staticmethod
    def clear_error():
        """Clears the error reprt structure."""
        return yapi.yices_clear_error()

    @staticmethod
    def print_error(fd):
        """Prints the error report out to the given file descriptor."""
        return yapi.yices_print_error_fd(fd)

    @staticmethod
    def init():
        """Must be called before any other API routine (other than is_inited), to initialize internal data structures."""
        yapi.yices_init()

    @staticmethod
    def is_inited():
        """Return True if the library has been initialized, False otherwise."""
        return yapi.yices_is_inited()

    @staticmethod
    def exit():
        """Deletes all the internal data structure, must be called on exiting to prevent leaks."""
        yapi.yices_exit()

    @staticmethod
    def reset():
        """Resets all the internal data structures."""
        yapi.yices_reset()

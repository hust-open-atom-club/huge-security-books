import traceback
import sys

from types import TracebackType
from typing import Any, Optional, Union
from Timeout import Timeout

class ExpectError:
    """Execute a code block expecting (and catching) an error."""

    def __init__(self, exc_type: Optional[type] = None, 
                 print_traceback: bool = True, mute: bool = False):
        """
        Constructor. Expect an exception of type `exc_type` (`None`: any exception).
        If `print_traceback` is set (default), print a traceback to stderr.
        If `mute` is set (default: False), do not print anything.
        """
        self.print_traceback = print_traceback
        self.mute = mute
        self.expected_exc_type = exc_type

    def __enter__(self) -> Any:
        """Begin of `with` block"""
        return self

    def __exit__(self, exc_type: type, 
                 exc_value: BaseException, tb: TracebackType) -> Optional[bool]:
        """End of `with` block"""
        if exc_type is None:
            # No exception
            return

        if (self.expected_exc_type is not None
            and exc_type != self.expected_exc_type):
            raise  # Unexpected exception

        # An exception occurred
        if self.print_traceback:
            lines = ''.join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    tb)).strip()
        else:
            lines = traceback.format_exception_only(
                exc_type, exc_value)[-1].strip()

        if not self.mute:
            print(lines, "(expected)", file=sys.stderr)
        return True  # Ignore it



class ExpectTimeout(Timeout):
    """Execute a code block expecting (and catching) a timeout."""

    def __init__(self, timeout: Union[int, float],
                 print_traceback: bool = True, mute: bool = False):
        """
        Constructor. Interrupt execution after `seconds` seconds.
        If `print_traceback` is set (default), print a traceback to stderr.
        If `mute` is set (default: False), do not print anything.
        """
        super().__init__(timeout)

        self.print_traceback = print_traceback
        self.mute = mute

    def __exit__(self, exc_type: type,
                 exc_value: BaseException, tb: TracebackType) -> Optional[bool]:
        """End of `with` block"""

        super().__exit__(exc_type, exc_value, tb)

        if exc_type is None:
            return

        # An exception occurred
        if self.print_traceback:
            lines = ''.join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    tb)).strip()
        else:
            lines = traceback.format_exception_only(
                exc_type, exc_value)[-1].strip()

        if not self.mute:
            print(lines, "(expected)", file=sys.stderr)

        return True  # Ignore exception

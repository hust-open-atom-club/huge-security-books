import time
from types import FrameType, TracebackType

import signal
from typing import Any, Callable, Optional, Type, Union

class SignalTimeout:
    """Execute a code block raising a timeout."""

    def __init__(self, timeout: Union[int, float]) -> None:
        """
        Constructor. Interrupt execution after `timeout` seconds.
        """
        self.timeout = timeout
        self.old_handler: Any = signal.SIG_DFL
        self.old_timeout = 0.0

    def __enter__(self) -> Any:
        """Begin of `with` block"""
        # Register timeout() as handler for signal 'SIGALRM'"
        self.old_handler = signal.signal(signal.SIGALRM, self.timeout_handler)
        self.old_timeout, _ = signal.setitimer(signal.ITIMER_REAL, self.timeout)
        return self

    def __exit__(self, exc_type: Type, exc_value: BaseException,
                 tb: TracebackType) -> None:
        """End of `with` block"""
        self.cancel()
        return  # re-raise exception, if any

    def cancel(self) -> None:
        """Cancel timeout"""
        signal.signal(signal.SIGALRM, self.old_handler)
        signal.setitimer(signal.ITIMER_REAL, self.old_timeout)

    def timeout_handler(self, signum: int, frame: Optional[FrameType]) -> None:
        """Handle timeout (SIGALRM) signal"""
        raise TimeoutError()
    

import sys

class GenericTimeout:
    """Execute a code block raising a timeout."""

    def __init__(self, timeout: Union[int, float]) -> None:
        """
        Constructor. Interrupt execution after `timeout` seconds.
        """

        self.seconds_before_timeout = timeout
        self.original_trace_function: Optional[Callable] = None
        self.end_time: Optional[float] = None

    def check_time(self, frame: FrameType, event: str, arg: Any) -> Callable:
        """Tracing function"""
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        current_time = time.time()
        if self.end_time and current_time >= self.end_time:
            raise TimeoutError

        return self.check_time

    def __enter__(self) -> Any:
        """Begin of `with` block"""
        start_time = time.time()
        self.end_time = start_time + self.seconds_before_timeout

        self.original_trace_function = sys.gettrace()
        sys.settrace(self.check_time)
        return self

    def __exit__(self, exc_type: type, 
                 exc_value: BaseException, tb: TracebackType) -> Optional[bool]:
        """End of `with` block"""
        self.cancel()
        return None  # re-raise exception, if any

    def cancel(self) -> None:
        """Cancel timeout"""
        sys.settrace(self.original_trace_function)


Timeout: Type[SignalTimeout] = SignalTimeout if hasattr(signal, 'SIGALRM') else GenericTimeout

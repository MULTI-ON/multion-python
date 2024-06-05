import typing
from typing import Callable
from typing_extensions import ParamSpec

P = ParamSpec("P")
T = typing.TypeVar("T")


def wraps_function(
    _fun: Callable[P, T]
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(wrapped) -> Callable[P, T]:
        return wrapped
    return decorator

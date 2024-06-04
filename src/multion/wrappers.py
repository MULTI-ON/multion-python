import typing
from typing import Callable
from typing_extensions import ParamSpec, Concatenate

P = ParamSpec('P')
T = typing.TypeVar('T')

def wraps_function(
    _fun: Callable[P, T]
) -> Callable[[Callable[Concatenate[Callable[P, T], P], T]], Callable[P, T]]:
    def decorator(
        wrapped_fun: Callable[Concatenate[Callable[P, T], P], T]
    ) -> Callable[P, T]:
        def decorated(*args: P.args, **kwargs: P.kwargs) -> T:
            return wrapped_fun(*args, **kwargs)
        return decorated
    return decorator
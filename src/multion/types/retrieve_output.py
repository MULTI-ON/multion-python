# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import pydantic_v1
from ..core.unchecked_base_model import UncheckedBaseModel


class RetrieveOutput(UncheckedBaseModel):
    message: str = pydantic_v1.Field()
    """
    information relating to response
    """

    url: str = pydantic_v1.Field()
    """
    The last accessed URL during the session.
    """

    screenshot: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    image url of the screenshot taken during the session.
    """

    session_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    The unique identifier for the session.
    """

    status: str = pydantic_v1.Field()
    """
    The current status of the session.
    """

    data: typing.List[typing.Dict[str, typing.Any]] = pydantic_v1.Field()
    """
    Array of data objects, each containing data requested in fields.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}

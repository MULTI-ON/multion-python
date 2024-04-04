# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import pydantic_v1


class BrowseOutput(pydantic_v1.BaseModel):
    message: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    The final message or result of the browsing session.
    """

    status: str = pydantic_v1.Field()
    """
    The final status of the browsing session.
    """

    url: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    The last accessed URL during the session.
    """

    page_content: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Extracted text content from the final page.
    """

    screenshot: str = pydantic_v1.Field()
    """
    image url of the screenshot taken during the session.
    """

    session_id: str = pydantic_v1.Field()
    """
    The unique identifier for the session.
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

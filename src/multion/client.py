import typing

from .base_client import AsyncBaseMultiOn, BaseMultiOn
from .sessions.wrapped_client import (
    WrappedAsyncSessionsClient,
    WrappedSessionsClient,
)
import agentops  # type: ignore
import os

from .wrappers import wraps_function


# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class MultiOn(BaseMultiOn):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: MultiOnEnvironment. The environment to use for requests from the client. from .environment import MultiOnEnvironment

                                           Defaults to MultiOnEnvironment.DEFAULT

        - api_key: typing.Optional[str].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

        - follow_redirects: typing.Optional[bool]. Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

        - httpx_client: typing.Optional[httpx.Client]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from multion.client import MultiOn

    client = MultiOn(
        api_key="YOUR_API_KEY",
    )
    """

    @wraps_function(BaseMultiOn.__init__)  # type: ignore
    def __init__(self, *args, agentops_api_key: typing.Optional[str] = os.getenv("AGENTOPS_API_KEY"), **kwargs):
        super().__init__(*args, **kwargs)
        self.sessions = WrappedSessionsClient(client_wrapper=self._client_wrapper)
        if agentops_api_key is not None:
            agentops.init(
                api_key=agentops_api_key,
                parent_key=os.getenv("AGENTOPS_PARENT_KEY"),
                auto_start_session=False,
            )

    @agentops.record_function(event_name="browse")  # type: ignore
    @wraps_function(BaseMultiOn.browse)
    def browse(self, *args, **kwargs):
        agentops.start_session(tags=["multion-sdk"])
        return super().browse(*args, **kwargs)


class AsyncMultiOn(AsyncBaseMultiOn):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: MultiOnEnvironment. The environment to use for requests from the client. from .environment import MultiOnEnvironment

                                           Defaults to MultiOnEnvironment.DEFAULT

        - api_key: typing.Optional[str].

        - agentops_api_key: typing.Optional[str].

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

        - follow_redirects: typing.Optional[bool]. Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

        - httpx_client: typing.Optional[httpx.AsyncClient]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from multion.client import AsyncMultiOn

    client = MultiOn(
        api_key="YOUR_API_KEY",
        agentops_api_key="YOUR_AGENTOPS_API_KEY",
    )
    """

    @wraps_function(AsyncBaseMultiOn.__init__)  # type: ignore
    def __init__(self, *args, **kwargs):
        agentops_api_key = kwargs.pop("agentops_api_key", None)
        super().__init__(*args, **kwargs)
        self.sessions = WrappedAsyncSessionsClient(client_wrapper=self._client_wrapper)
        if agentops_api_key is not None:
            agentops.init(
                api_key=agentops_api_key,
                parent_key=os.getenv("AGENTOPS_PARENT_KEY"),
                auto_start_session=False,
            )

    @agentops.record_function(event_name="browse")  # type: ignore
    @wraps_function(AsyncBaseMultiOn.browse)
    async def browse(self, *args, **kwargs):
        agentops.start_session(tags=["multion-sdk"])
        return super().browse(*args, **kwargs)

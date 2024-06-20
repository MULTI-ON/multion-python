import typing
from .base_client import AsyncBaseMultiOn, BaseMultiOn
from .sessions.wrapped_client import (
    WrappedAsyncSessionsClient,
    WrappedSessionsClient,
)
import agentops  # type: ignore
import os

from .wrappers import wraps_function
from .types.browse_output import BrowseOutput
from .types.retrieve_output import RetrieveOutput

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

        - agentops_api_key: typing.Optional[str]. If you wish to visualize your MultiOn agent's execution at app.agentops.ai

        - timeout: typing.Optional[float]. The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

        - follow_redirects: typing.Optional[bool]. Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

        - httpx_client: typing.Optional[httpx.Client]. The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    ---
    from multion.client import MultiOn

    client = MultiOn(
        api_key="YOUR_API_KEY",
        agentops_api_key="YOUR_AGENTOPS_API_KEY",
    )
    """

    @wraps_function(BaseMultiOn.__init__)  # type: ignore
    def __init__(
        self,
        *args,
        agentops_api_key: typing.Optional[str] = os.getenv("AGENTOPS_API_KEY"),
        **kwargs
    ):

        super().__init__(*args, **kwargs)
        self._agentops_api_key = agentops_api_key

        self.sessions = WrappedSessionsClient(
            client_wrapper=self._client_wrapper, use_agentops=self._agentops_api_key is not None)

        if self._agentops_api_key is not None:
            agentops.init(
                api_key=agentops_api_key,
                parent_key=os.getenv("AGENTOPS_PARENT_KEY"),
                auto_start_session=False,
            )

    @wraps_function(BaseMultiOn.browse)  # type: ignore
    def _browse(self, *args, **kwargs) -> BrowseOutput:
        return super().browse(*args, **kwargs)

    @wraps_function(BaseMultiOn.retrieve)  # type: ignore
    def _retrieve(self, *args, **kwargs) -> RetrieveOutput:
        return super().retrieve(*args, **kwargs)

    def browse(self, *args, **kwargs) -> BrowseOutput:
        if self._agentops_api_key is not None:
            agentops.start_session(tags=["multion-sdk"])

            @agentops.record_function(event_name="browse")
            def wrapped_browse(*args, **kwargs):
                return self._browse(*args, **kwargs)
            return wrapped_browse(*args, **kwargs)
        return self._browse(*args, **kwargs)

    def retrieve(self, *args, **kwargs) -> RetrieveOutput:
        if self._agentops_api_key is not None:
            agentops.start_session(tags=["multion-sdk"])

            @agentops.record_function(event_name="retrieve")
            def wrapped_retrieve(*args, **kwargs):
                return self._retrieve(*args, **kwargs)
            return wrapped_retrieve(*args, **kwargs)
        return self._retrieve(*args, **kwargs)


class AsyncMultiOn(AsyncBaseMultiOn):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters:
        - base_url: typing.Optional[str]. The base url to use for requests from the client.

        - environment: MultiOnEnvironment. The environment to use for requests from the client. from .environment import MultiOnEnvironment

                                           Defaults to MultiOnEnvironment.DEFAULT

        - api_key: typing.Optional[str].

        - agentops_api_key: typing.Optional[str]. If you wish to visualize your MultiOn agent's execution at app.agentops.ai

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
    def __init__(
        self,
        *args,
        agentops_api_key: typing.Optional[str] = os.getenv("AGENTOPS_API_KEY"),
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._agentops_api_key = agentops_api_key
        self.sessions = WrappedAsyncSessionsClient(client_wrapper=self._client_wrapper,
                                                   use_agentops=self._agentops_api_key is not None)
        if agentops_api_key is not None:
            agentops.init(
                api_key=agentops_api_key,
                parent_key=os.getenv("AGENTOPS_PARENT_KEY"),
                auto_start_session=False,
            )

    @wraps_function(AsyncBaseMultiOn.browse)  # type: ignore
    async def _browse(self, *args, **kwargs) -> BrowseOutput:
        return await super().browse(*args, **kwargs)

    @wraps_function(BaseMultiOn.retrieve)  # type: ignore
    async def _retrieve(self, *args, **kwargs) -> RetrieveOutput:
        return await super().retrieve(*args, **kwargs)

    async def browse(self, *args, **kwargs) -> BrowseOutput:
        if self._agentops_api_key is not None:
            agentops.start_session(tags=["multion-sdk"])

            @agentops.record_function(event_name="browse")
            async def wrapped_browse(*args, **kwargs):
                return await self._browse(*args, **kwargs)
            return await wrapped_browse(*args, **kwargs)
        return await self._browse(*args, **kwargs)

    async def retrieve(self, *args, **kwargs) -> RetrieveOutput:
        if self._agentops_api_key is not None:
            agentops.start_session(tags=["multion-sdk"])

            @agentops.record_function(event_name="retrieve")
            async def wrapped_retrieve(*args, **kwargs):
                return await self._retrieve(*args, **kwargs)  # type: ignore
            return await wrapped_retrieve(*args, **kwargs)
        return await self._retrieve(*args, **kwargs)  # type: ignore

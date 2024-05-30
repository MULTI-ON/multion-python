from nis import cat

from multion.sessions.client import AsyncSessionsClient, SessionsClient
import agentops
from agentops import ActionEvent
from agentops.enums import EndState

import json
import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx_sse

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.remove_none_from_dict import remove_none_from_dict
from ..core.request_options import RequestOptions
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from ..types.optional_params import OptionalParams
from ..types.retrieve_output import RetrieveOutput
from ..types.session_created import SessionCreated
from ..types.session_step_stream_chunk import SessionStepStreamChunk
from ..types.session_step_success import SessionStepSuccess
from .types.create_session_input_browser_params import CreateSessionInputBrowserParams
from .types.sessions_close_response import SessionsCloseResponse
from .types.sessions_list_response import SessionsListResponse
from .types.sessions_screenshot_response import SessionsScreenshotResponse
from .types.sessions_step_request_browser_params import SessionsStepRequestBrowserParams
from .types.sessions_step_stream_request_browser_params import SessionsStepStreamRequestBrowserParams

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class WrappedSessionsClient(SessionsClient):
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)

    def create(
        self,
        *,
        url: str,
        local: typing.Optional[bool] = OMIT,
        browser_params: typing.Optional[CreateSessionInputBrowserParams] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SessionCreated:
        agentops.start_session(tags=["multion-sdk"])
        return super().create(url=url, local=local, browser_params=browser_params, include_screenshot=include_screenshot, request_options=request_options)
    
    def step_stream(
        self,
        session_id: str,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        browser_params: typing.Optional[SessionsStepStreamRequestBrowserParams] = OMIT,
        optional_params: typing.Optional[OptionalParams] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[SessionStepStreamChunk]:
            pass

    def step(
        self,
        session_id: str,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        browser_params: typing.Optional[SessionsStepRequestBrowserParams] = OMIT,
        optional_params: typing.Optional[OptionalParams] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SessionStepSuccess:
        step_response = super().step(...)

        # Begin agentops recording
        action_event = ActionEvent(params=locals())
        action_event.returns = step_response.dict()
        action_event.screenshot = step_response.screenshot
        agentops.record(action_event)
        
        return step_response
    
    def close(
        self, session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> SessionsCloseResponse:
        try:
            close_response = super().close(...)
            agentops.end_session(EndState.SUCCESS, end_state_reason=close_response.status_code)
            return close_response
        except Exception as e:
            agentops.end_session(EndState.FAIL, end_state_reason=e)
            raise e
        
    def retrieve(
        self,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        session_id: typing.Optional[str] = OMIT,
        page_number: typing.Optional[int] = OMIT,
        fields: typing.Optional[str] = OMIT,
        format: typing.Optional[typing.Literal["json"]] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> RetrieveOutput:
                pass


class WrappedAsyncSessionsClient(AsyncSessionsClient):
    async def create(
        self,
        *,
        url: str,
        local: typing.Optional[bool] = OMIT,
        browser_params: typing.Optional[CreateSessionInputBrowserParams] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SessionCreated:
        agentops.start_session(tags=["multion-sdk"])
        return super().create()
    
    async def step_stream(
        self,
        session_id: str,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        browser_params: typing.Optional[SessionsStepStreamRequestBrowserParams] = OMIT,
        optional_params: typing.Optional[OptionalParams] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[SessionStepStreamChunk]:
        pass
    
    async def step(
        self,
        session_id: str,
        *,
        cmd: str,
        url: typing.Optional[str] = OMIT,
        browser_params: typing.Optional[SessionsStepRequestBrowserParams] = OMIT,
        optional_params: typing.Optional[OptionalParams] = OMIT,
        include_screenshot: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SessionStepSuccess:
        step_response = await super().step(...)

        # Begin agentops recording
        action_event = ActionEvent(params=locals())
        action_event.returns = step_response.dict()
        action_event.screenshot = step_response.screenshot
        agentops.record(action_event)
        
        return step_response

    async def close(
        self, session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> SessionsCloseResponse:
        try:
            close_response = super().close(...)
            agentops.end_session(EndState.SUCCESS, end_state_reason=close_response.status_code)
            return close_response
        except Exception as e:
            agentops.end_session(EndState.FAIL, end_state_reason=e)
            raise e
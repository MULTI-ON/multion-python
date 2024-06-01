from nis import cat

from multion.sessions.client import AsyncSessionsClient, SessionsClient
import agentops
from agentops import ActionEvent, LLMEvent, ErrorEvent

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
        try:
            return super().create(url=url, local=local, browser_params=browser_params, include_screenshot=include_screenshot, request_options=request_options)
        except Exception as e:
            error_event = ErrorEvent(exception=e)
            agentops.record(error_event)
            raise e

    # TODO: test step_stream
    @agentops.record_function(event_name="step_stream")
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
        params = {"session_id": session_id, "cmd": cmd}
        if url is not OMIT:
            params["url"] = url
        if browser_params is not OMIT:
            params["browser_params"] = browser_params.json()
        if optional_params is not OMIT:
            params["optional_params"] = optional_params.json()
        if request_options is not None:
            params["request_options"] = request_options

        # TODO: Add LLMEvent
        if action_event is None:
            action_event = ActionEvent(action_type="step_stream",params=params)
            action_event.returns = ""
        try:
            step_stream_response = super().step_stream(session_id=session_id, cmd=cmd, url=url, browser_params=browser_params, optional_params=optional_params, include_screenshot=include_screenshot, request_options=request_options)
            
            if isinstance(step_stream_response, SessionStepStreamChunk.SessionStepStreamChunk_Event):
                action_event.returns += step_stream_response.data.delta.content
            elif isinstance(step_stream_response, SessionStepStreamChunk.SessionStepStreamChunk_FinalEvent):
                action_event.returns += step_stream_response.data.delta.content
                action_event.screenshot = step_stream_response.screenshot
                agentops.record(action_event)
            return step_stream_response
        except Exception as e:
            error_event = ErrorEvent(trigger_event=action_event, exception=e)
            agentops.record(error_event)
            raise e

    @agentops.record_function(event_name="step")
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
        llm_event = LLMEvent()
        step_response = super().step(session_id=session_id, cmd=cmd, url=url, browser_params=browser_params, optional_params=optional_params, include_screenshot=include_screenshot, request_options=request_options)
        llm_event.prompt = step_response.message
        agentops.record(llm_event)
        return step_response
    
    def close(
        self, session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> SessionsCloseResponse:
        close_response = super().close(session_id=session_id, request_options=request_options)
        agentops.end_session("Success", end_state_reason=close_response.status)
        return close_response
    
    @agentops.record_function(event_name="retrieve")
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
        return super().retrieve(cmd=cmd, url=url, session_id=session_id, page_number=page_number, fields=fields, format=format, include_screenshot=include_screenshot, request_options=request_options)

# TODO: Test async
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
        try:
            return super().create(url=url, local=local, browser_params=browser_params, include_screenshot=include_screenshot, request_options=request_options)
        except Exception as e:
            error_event = ErrorEvent(exception=e)
            agentops.record(error_event)
            raise e
    
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
        params = {"session_id": session_id, "cmd": cmd}
        if url is not OMIT:
            params["url"] = url
        if browser_params is not OMIT:
            params["browser_params"] = browser_params.json()
        if optional_params is not OMIT:
            params["optional_params"] = optional_params.json()
        if request_options is not None:
            params["request_options"] = request_options

        # TODO: Add LLMEvent
        if action_event is None:
            action_event = ActionEvent(action_type="step_stream",params=params)
            action_event.returns = ""
        try:
            step_stream_response = super().step_stream(session_id=session_id, cmd=cmd, url=url, browser_params=browser_params, optional_params=optional_params, include_screenshot=include_screenshot, request_options=request_options)
            
            if isinstance(step_stream_response, SessionStepStreamChunk.SessionStepStreamChunk_Event):
                action_event.returns += step_stream_response.data.delta.content
            elif isinstance(step_stream_response, SessionStepStreamChunk.SessionStepStreamChunk_FinalEvent):
                action_event.returns += step_stream_response.data.delta.content
                action_event.screenshot = step_stream_response.screenshot
                agentops.record(action_event)
            return step_stream_response
        except Exception as e:
            error_event = ErrorEvent(trigger_event=action_event, exception=e)
            agentops.record(error_event)
            raise e
    
    @agentops.record_function(event_name="step")
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
        llm_event = LLMEvent()
        step_response = super().step(session_id=session_id, cmd=cmd, url=url, browser_params=browser_params, optional_params=optional_params, include_screenshot=include_screenshot, request_options=request_options)
        llm_event.prompt = step_response.message
        agentops.record(llm_event)
        return step_response

    @agentops.record_function(event_name="retrieve")
    async def retrieve(
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
        return super().retrieve(cmd=cmd, url=url, session_id=session_id, page_number=page_number, fields=fields, format=format, include_screenshot=include_screenshot, request_options=request_options)



    async def close(
        self, session_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> SessionsCloseResponse:
        close_response = super().close(session_id=session_id, request_options=request_options)
        agentops.end_session("Success", end_state_reason=close_response.status)
        return close_response
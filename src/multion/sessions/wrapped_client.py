from multion.sessions.client import AsyncSessionsClient, SessionsClient
import agentops
from agentops import ActionEvent, LLMEvent, ErrorEvent

import typing
from ..types.retrieve_output import RetrieveOutput
from ..types.session_created import SessionCreated
from ..types.session_step_stream_chunk import SessionStepStreamChunk
from ..types.session_step_success import SessionStepSuccess
from .types.sessions_close_response import SessionsCloseResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class WrappedSessionsClient(SessionsClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, *args, **kwargs) -> SessionCreated:
        agentops.start_session(tags=["multion-sdk"])
        try:
            return super().create(*args, **kwargs)
        except Exception as e:
            error_event = ErrorEvent(exception=e)
            agentops.record(error_event)
            raise e

    # TODO: test step_stream
    @agentops.record_function(event_name="step_stream")
    def step_stream(self, *args, **kwargs) -> typing.Iterator[SessionStepStreamChunk]:
        # TODO: Add LLMEvent
        if action_event is None:
            action_event = ActionEvent(action_type="step_stream", params=kwargs)
            action_event.returns = ""
        try:
            step_stream_response = super().step_stream(*args, **kwargs)

            if isinstance(
                step_stream_response,
                SessionStepStreamChunk.SessionStepStreamChunk_Event,
            ):
                action_event.returns += step_stream_response.data.delta.content
            elif isinstance(
                step_stream_response,
                SessionStepStreamChunk.SessionStepStreamChunk_FinalEvent,
            ):
                action_event.returns += step_stream_response.data.delta.content
                action_event.screenshot = step_stream_response.screenshot
                agentops.record(action_event)
            return step_stream_response
        except Exception as e:
            error_event = ErrorEvent(trigger_event=action_event, exception=e)
            agentops.record(error_event)
            raise e

    @agentops.record_function(event_name="step")
    def step(self, *args, **kwargs) -> SessionStepSuccess:
        llm_event = LLMEvent()
        step_response = super().step(*args, **kwargs)
        llm_event.prompt = step_response.message
        agentops.record(llm_event)
        return step_response

    def close(self, *args, **kwargs) -> SessionsCloseResponse:
        close_response = super().close(*args, **kwargs)
        agentops.end_session("Success")
        return close_response

    @agentops.record_function(event_name="retrieve")
    def retrieve(self, *args, **kwargs) -> RetrieveOutput:
        return super().retrieve(*args, **kwargs)


# TODO: Test async
class WrappedAsyncSessionsClient(AsyncSessionsClient):
    async def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, *args, **kwargs) -> SessionCreated:
        agentops.start_session(tags=["multion-sdk"])
        try:
            return super().create(*args, **kwargs)
        except Exception as e:
            error_event = ErrorEvent(exception=e)
            agentops.record(error_event)
            raise e

    # TODO: test step_stream
    @agentops.record_function(event_name="step_stream")
    async def step_stream(
        self, *args, **kwargs
    ) -> typing.Iterator[SessionStepStreamChunk]:
        # TODO: Add LLMEvent
        if action_event is None:
            action_event = ActionEvent(action_type="step_stream", params=kwargs)
            action_event.returns = ""
        try:
            step_stream_response = super().step_stream(*args, **kwargs)

            if isinstance(
                step_stream_response,
                SessionStepStreamChunk.SessionStepStreamChunk_Event,
            ):
                action_event.returns += step_stream_response.data.delta.content
            elif isinstance(
                step_stream_response,
                SessionStepStreamChunk.SessionStepStreamChunk_FinalEvent,
            ):
                action_event.returns += step_stream_response.data.delta.content
                action_event.screenshot = step_stream_response.screenshot
                agentops.record(action_event)
            return step_stream_response
        except Exception as e:
            error_event = ErrorEvent(trigger_event=action_event, exception=e)
            agentops.record(error_event)
            raise e

    @agentops.record_function(event_name="step")
    async def step(self, *args, **kwargs) -> SessionStepSuccess:
        llm_event = LLMEvent()
        step_response = super().step(*args, **kwargs)
        llm_event.prompt = step_response.message
        agentops.record(llm_event)
        return step_response

    async def close(self, *args, **kwargs) -> SessionsCloseResponse:
        close_response = super().close(*args, **kwargs)
        agentops.end_session("Success")
        return close_response

    @agentops.record_function(event_name="retrieve")
    async def retrieve(*args, **kwargs) -> RetrieveOutput:
        return super().retrieve(*args, **kwargs)

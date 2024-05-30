from nis import cat

from multion.sessions.client import AsyncSessionsClient, SessionsClient
import agentops
from agentops import ActionEvent
from agentops.enums import EndState


class WrappedSessionsClient(SessionsClient):
    def create(...):
        agentops.start_session(tags=["multion-sdk"])
        return super().create()

    def step(...):
        step_response = super().step(...)

        # Begin agentops recording
        action_event = ActionEvent(params=locals())
        action_event.returns = step_response.dict()
        action_event.screenshot = step_response.screenshot
        agentops.record(action_event)
        
        return step_response
    
    def close(...):
        try:
            close_response = super().close(...)
            agentops.end_session(EndState.SUCCESS, end_state_reason=close_response.status_code)
            return close_response
        except Exception as e:
            agentops.end_session(EndState.FAIL, end_state_reason=e)
            raise e


class WrappedAsyncSessionsClient(AsyncSessionsClient):
    async def create():
        agentops.start_session(tags=["multion-sdk"])
        return super().create()
    
    async def step(...):
        step_response = await super().step(...)

        # Begin agentops recording
        action_event = ActionEvent(params=locals())
        action_event.returns = step_response.dict()
        action_event.screenshot = step_response.screenshot
        agentops.record(action_event)
        
        return step_response

    def close(...):
        try:
            close_response = super().close(...)
            agentops.end_session(EndState.SUCCESS, end_state_reason=close_response.status_code)
            return close_response
        except Exception as e:
            agentops.end_session(EndState.FAIL, end_state_reason=e)
            raise e
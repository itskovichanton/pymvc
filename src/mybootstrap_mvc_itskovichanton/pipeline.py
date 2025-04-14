import inspect
from dataclasses import dataclass
from typing import Any, Callable, Protocol

from src.mybootstrap_core_itskovichanton.alerts import AlertService
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.error_provider import Err, ErrorProvider


@dataclass
class Call:
    request: Any
    ip: str = None
    user_agent: str = None


@dataclass
class Result:
    result: Any = None
    error: Err = None


class Action:
    def run(self, args: Any = None) -> Any:
        """Run action"""


@dataclass
class CallableAction(Action):
    call: Callable[[Any], Any]
    unbox_call: bool = False

    def run(self, args: Any = None) -> Any:
        if self.unbox_call:
            return self.call(**args)
        return self.call(args)


class ActionRunner(Protocol):

    async def run(self, *actions: Action | Callable[[Any], Any], call: Any = None, unbox_call: bool = False,
                  error_provider: ErrorProvider = None) -> Result:
        ...


@bean
class ActionRunnerImpl(ActionRunner):
    default_error_provider: ErrorProvider
    alert_service: AlertService

    async def run(self,
                  *actions: Action | Callable[[Any], Any],
                  call: Any = None,
                  unbox_call: bool = False,
                  error_provider: ErrorProvider = None) -> Result:

        r = Result()
        r.result = call
        for action in actions:
            if callable(action) and not isinstance(action, Action):
                action = CallableAction(call=action, unbox_call=unbox_call)
            coroutine = inspect.iscoroutinefunction(action.run)
            try:
                if coroutine:
                    r.result = await action.run(r.result)
                else:
                    r.result = action.run(r.result)
            except BaseException as e:
                self.alert_service.handle(e)
                if error_provider is None:
                    error_provider = self.default_error_provider
                r.error = error_provider.provide_error(e)
                r.result = None
                break

        return r

import inspect
from dataclasses import dataclass
from typing import Any, Callable

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
    def run(self, args: Any = None, prev_result: Any = None) -> Any:
        """Run action"""


@dataclass
class CallableAction(Action):
    call: Callable[[Any, Any], Any]

    def run(self, args: Any = None, prev_result: Any = None) -> Any:
        return self.call(args, prev_result)


class ActionRunner:

    async def run(self, *actions: Action | Callable[[Any, Any], Any], call: Any = None,
                  error_provider: ErrorProvider = None) -> Result:
        """runs action"""


@bean
class ActionRunnerImpl(ActionRunner):
    default_error_provider: ErrorProvider
    alert_service: AlertService

    async def run(self, *actions: Action | Callable[[Any, Any], Any], call: Any = None,
                  error_provider: ErrorProvider = None) -> Result:
        r = Result()
        for action in actions[0]:
            if callable(action) and not isinstance(action, Action):
                action = CallableAction(call=action)
            try:
                if inspect.iscoroutinefunction(action.run):
                    r.result = await action.run(call, r.result)
                else:
                    r.result = action.run(call, r.result)
            except BaseException as e:
                self.alert_service.handle(e)
                if error_provider is None:
                    error_provider = self.default_error_provider
                r.error = error_provider.provide_error(e)
                break

        return r

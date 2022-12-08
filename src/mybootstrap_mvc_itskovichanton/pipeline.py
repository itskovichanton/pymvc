from dataclasses import dataclass
from typing import Protocol, Any

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


class Action(Protocol):
    def run(self, args: Any) -> Any:
        """Run action"""


class ActionRunner:

    async def run(self, action: Action, call: Any, error_provider: ErrorProvider = None) -> Result:
        """runs action"""


@bean
class ActionRunnerImpl(ActionRunner):
    default_error_provider: ErrorProvider
    alert_service: AlertService

    async def run(self, action: Action, call: Any, error_provider: ErrorProvider = None) -> Result:
        r = Result()
        try:
            r.result = action.run(call)
        except BaseException as e:
            await self.alert_service.handle(e)
            if error_provider is None:
                error_provider = self.default_error_provider
            r.error = error_provider.provide_error(e)

        # todo: добавь логгирование
        return r

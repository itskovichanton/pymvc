from typing import Any

from src.mybootstrap_ioc_itskovichanton.ioc import bean

from src.mybootstrap_mvc_itskovichanton.error_provider import ErrorProvider
from src.mybootstrap_mvc_itskovichanton.pipeline import ActionRunner, Action
from src.mybootstrap_mvc_itskovichanton.result_presenter import ResultPresenter


@bean
class Controller:
    action_runner: ActionRunner
    default_result_presenter: ResultPresenter

    async def run(self, *actions: Action, call: Any = None,
                  error_provider: ErrorProvider = None,
                  result_presenter: ResultPresenter = None) -> Any:
        result = await self.action_runner.run(actions, call=call, error_provider=error_provider)
        if result_presenter is None:
            result_presenter = self.default_result_presenter
        return result_presenter.present(result)

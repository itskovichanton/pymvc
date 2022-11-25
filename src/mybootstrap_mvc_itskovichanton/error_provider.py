import traceback
from dataclasses import dataclass
from typing import Protocol

from src.mybootstrap_core_itskovichanton.validation import ValidationException
from src.mybootstrap_ioc_itskovichanton.ioc import bean

from src.mybootstrap_mvc_itskovichanton.exceptions import CoreException, ERR_REASON_INTERNAL

ERR_MSG_INTERNAL = "Произошла внутренняя ошибка. Мы уже занимаемся решением этой проблемы."


@dataclass
class Err:
    message: str = None
    details: str = None
    reason: str = None


# @dataclass
# class ErrWithInfo(Err):
#     info: str = None
#

class ErrorProvider(Protocol):
    def provide_error(self, e: BaseException) -> Err:
        """Get error presentation. Также можно возвращать потомки Err"""


@bean
class ErrorProviderImpl(ErrorProvider):

    def provide_error(self, e: BaseException) -> Err:
        r = Err(message=self.calc_msg(e), details=self.calc_details(e), reason=self.calc_reason(e))
        if isinstance(e, ValidationException):
            r.param = e.param
            r.invalid_value = e.invalid_value
            r.validation_reason = e.validation_reason
        return r

    def calc_msg(self, e: BaseException):
        return ERR_MSG_INTERNAL if self._context.profile == "prod" else str(e)

    def calc_details(self, e: BaseException):
        return None if self._context.profile == "prod" else traceback.format_exc()

    def calc_reason(self, e: BaseException):
        return e.reason if isinstance(e, CoreException) else ERR_REASON_INTERNAL

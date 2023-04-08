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
    context: str = None


class ErrorProvider(Protocol):
    def provide_error(self, e: BaseException) -> Err:
        """Get error presentation. Также можно возвращать потомки Err"""


@bean(details_enabled=("mvc.response.details", bool, True),
      original_msg=("mvc.response.original_error_msg", bool, True))
class ErrorProviderImpl(ErrorProvider):

    def provide_error(self, e: BaseException) -> Err:
        r = Err(message=self.calc_msg(e), details=self.calc_details(e), reason=self.calc_reason(e))
        if isinstance(e, ValidationException):
            r.param = e.param
            if hasattr(e, "invalid_value"):
                r.invalid_value = e.invalid_value
            r.validation_reason = e.validation_reason
        e_dict = e.__dict__
        if e_dict:
            try:
                r.context = {k: str(v) for k, v in e_dict.items() if k not in r.__dict__}
            except:
                ...
        return r

    def calc_msg(self, e: BaseException):
        return str(e) if self.original_msg else ERR_MSG_INTERNAL

    def calc_details(self, e: BaseException):
        return "\n.".join(traceback.format_exception(e)) if self.details_enabled else None

    def calc_reason(self, e: BaseException):
        return e.reason if isinstance(e, CoreException) else ERR_REASON_INTERNAL

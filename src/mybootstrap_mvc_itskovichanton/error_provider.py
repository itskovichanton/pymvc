import traceback
from typing import Protocol

from pydantic import BaseModel, ValidationError, Extra
from src.mybootstrap_core_itskovichanton.validation import ValidationException
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.exceptions import CoreException, ERR_REASON_INTERNAL, ERR_REASON_VALIDATION

ERR_MSG_INTERNAL = "Произошла внутренняя ошибка. Мы уже занимаемся решением этой проблемы."


class Err(BaseModel):
    message: str = None
    details: str = None
    reason: str = None
    cause: str = None

    class Config:
        extra = Extra.allow


class ErrorProvider(Protocol):
    def provide_error(self, e: BaseException) -> Err:
        """Get error presentation. Также можно возвращать потомки Err"""


@bean(details_enabled=("mvc.response.details", bool, True),
      original_msg=("mvc.response.original-error-msg", bool, True))
class ErrorProviderImpl(ErrorProvider):

    def provide_error(self, e: BaseException) -> Err:
        r = Err(message=self.calc_msg(e), details=self.calc_details(e), reason=self.calc_reason(e),
                cause=self.calc_cause(e))
        if isinstance(e, ValidationException):
            r.param = e.param
            if hasattr(e, "invalid_value"):
                r.invalid_value = e.invalid_value
            r.validation_reason = e.validation_reason
        try:
            r.__dict__.update(e.__dict__)
        except:
            ...
        return r

    def calc_msg(self, e: BaseException):
        return str(e) if self.original_msg else ERR_MSG_INTERNAL

    def calc_details(self, e: BaseException):
        return "\n.".join(traceback.format_exception(e)) if self.details_enabled else None

    def calc_reason(self, e: BaseException):
        if isinstance(e, ValidationError):
            return ERR_REASON_VALIDATION
        if isinstance(e, CoreException):
            return e.reason
        return ERR_REASON_INTERNAL

    def calc_cause(self, e: BaseException):
        return e.cause if isinstance(e, CoreException) else None

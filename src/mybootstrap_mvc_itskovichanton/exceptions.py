import functools

ERR_REASON_SERVER_RESPONDED_WITH_ERROR = "ERRCODE_SERVER_RESPONDED_WITH_ERROR"
ERR_REASON_VALIDATION = "VALIDATION"
ERR_REASON_AUTH_REQUIRED = "AUTHORIZATION_REQUIRED"
ERR_REASON_TECHNICAL = "ERRCODE_TECHNICAL"
ERR_REASON_INTERNAL = "INTERNAL"
ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND = "ERRCODE_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND"
ERR_REASON_SERVER_UNAVAILABLE = "ERRCODE_SERVER_UNAVAILABLE"
ERR_REASON_CALLER_UPDATE_REQUIRED = "CALLER_UPDATE_REQUIRED"
ERR_REASON_ACCESS_DENIED = "ERRCODE_ACCESS_DENIED"
ERR_REASON_TOO_MANY_REQUESTS = "TO_MANY_REQUESTS"


class CoreException(BaseException):
    """Base exception, that has message and reason properties"""

    def __init__(self, message=None, reason=ERR_REASON_SERVER_RESPONDED_WITH_ERROR, cause: BaseException = None):
        if not message and cause:
            message = str(cause)
        self.reason = reason
        self.message = message
        self.cause = cause
        super().__init__(self.message)


def wrap_with_core_exception(_reason=ERR_REASON_SERVER_RESPONDED_WITH_ERROR, _message=None):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                message = _message
                if callable(message):
                    message = message(e)
                reason = _reason
                if callable(reason):
                    reason = reason(e)
                raise CoreException(reason=reason, cause=e, message=message)

        return wrapper

    return decorator_repeat

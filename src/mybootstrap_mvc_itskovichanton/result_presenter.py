from typing import Protocol, Any

import src.mybootstrap_mvc_itskovichanton.exceptions as exceptions
from src.mybootstrap_mvc_itskovichanton.pipeline import Result


class ResultPresenter(Protocol):

    def preprocess_result(self, r: Result) -> Any:
        return r

    def present(self, r: Result) -> Any:
        """Get http response"""

    def http_code(self, r: Result) -> int:
        if r.error is None:
            return 200

        match r.error.reason:
            case exceptions.ERR_REASON_NOT_IMPLEMENTED:
                return 501
            case exceptions.ERR_REASON_SERVER_RESPONDED_WITH_ERROR:
                return 200
            case exceptions.ERR_REASON_SERVER_RESPONDED_WITH_FATAL_ERROR:
                return 200
            case exceptions.ERR_REASON_TOO_MANY_REQUESTS:
                return 429
            case exceptions.ERR_REASON_ACCESS_DENIED:
                return 403
            case exceptions.ERR_REASON_VALIDATION:
                return 400
            case exceptions.ERR_REASON_SERVER_UNAVAILABLE:
                return 503
            case exceptions.ERR_REASON_AUTH_REQUIRED:
                return 401
            case exceptions.ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND:
                return 404

        return 500

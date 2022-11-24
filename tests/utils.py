from fastapi import Request

from src.mybootstrap_mvc_itskovichanton.pipeline import Call


def get_call_from_request(request: Request) -> Call:
    return Call(request=request,
                ip=request.headers.get('X-Real-Ip', ''),
                user_agent=request.headers.get('User-Agent', ''))

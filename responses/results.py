from dataclasses import dataclass
from typing import Any

from responses.exceptions import BizException


@dataclass
class R:
    success: bool
    code: int
    message: str
    data: Any

    @staticmethod
    def ok(data: any = None):
        return R(success=True, code=0, message='', data=data)

    @staticmethod
    def error(e: BizException):
        return R(success=False, code=e.code, message=e.message, data=None)

from dataclasses import dataclass
from enum import Enum


class Codes(Enum):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    # Client Error: 1000 - 1999
    ARGS_ERROR = (1000, 'Args Error.')
    UNAUTHORIZED = (1001, 'Unauthorized.')

    # Server Error: 9000 - 9999
    SERVER_ERROR = (9999, 'Server Error.')


@dataclass
class BizException(Exception):
    code: int
    message: str

    @staticmethod
    def from_codes(codes: Codes, message: str = None):
        msg = codes.message
        if message is not None:
            msg = message
        return BizException(codes.code, msg)

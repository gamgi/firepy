from io import StringIO
import re
from typing import Union
from sh import ErrorReturnCode

REGEX_STDERR_MESSAGE = re.compile('.*? \\[[\\w -:]+\\] (.*)', re.MULTILINE)


class FirecrackerError(RuntimeError):
    pass


def _error_str(error: Union[str, StringIO]) -> str:
    if isinstance(error, str):
        error_str = error
    else:
        error_str = error.getvalue()
        error.truncate(0)
    return error_str


def err_from_stderr(error: Union[str, StringIO],
                    exit_code: int = None) -> RuntimeError:
    error_str = _error_str(error)
    errors = list(REGEX_STDERR_MESSAGE.findall(error_str))

    if not errors:
        raise RuntimeError(f'Unknown error: {error_str}')

    if exit_code == 153:
        raise FirecrackerError(errors[0])
    else:
        raise RuntimeError(errors[0])


def err_from_returncode(err: ErrorReturnCode) -> RuntimeError:
    return err_from_stderr(err.stderr.decode(), err.exit_code or None)

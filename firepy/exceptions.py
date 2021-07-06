import re
from sh import ErrorReturnCode

REGEX_STDERR_MESSAGE = re.compile('.*? \\[[\\w -:]+\\] (.*)', re.MULTILINE)


class FirecrackerError(RuntimeError):
    pass


def err_from_stderr(err: ErrorReturnCode) -> RuntimeError:
    error_str = err.stderr.decode()
    error_code = err.exit_code or 1

    errors = list(REGEX_STDERR_MESSAGE.findall(error_str))
    if not errors:
        raise RuntimeError(f'Unknown error: {str(err)}')

    if error_code == 153:
        raise FirecrackerError(errors[0])
    else:
        raise RuntimeError(errors[0])

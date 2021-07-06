import pytest
from firepy.exceptions import err_from_stderr, FirecrackerError
from sh import ErrorReturnCode

EXAMPLE_STDERR = '''
2021-07-05T22:52:12.904223200 [anonymous-instance:main:ERROR:src/firecracker/src/main.rs:87] Firecracker panicked at 'Error creating the Kvm object: Error(13)', src/vmm/src/vstate/system.rs:53:30
2021-07-06T16:08:16.354918093 [anonymous-instance:main:ERROR:src/firecracker/src/main.rs:183] Arguments parsing error: Found argument 'foo' which wasn't expected, or isn't valid in this context.
'''  # noqa: E501


class TestExceptions:
    def test_err_from_stderr_parses_stderr(self, requests_mock):
        error = ErrorReturnCode('firecracker --foo',
                                'some stdout'.encode(),
                                EXAMPLE_STDERR.encode())
        error.exit_code = 153

        with pytest.raises(FirecrackerError, match="Firecracker panicked"):
            raise err_from_stderr(error)

    def test_err_from_stderr_returns_unknown_error(self, requests_mock):
        error = ErrorReturnCode('firecracker --foo',
                                'some stdout'.encode(),
                                'some stderr'.encode())
        error.exit_code = 1

        with pytest.raises(RuntimeError, match="Unknown error"):
            raise err_from_stderr(error)

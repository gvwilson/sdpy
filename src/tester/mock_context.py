from util import run_tests
from mock_object import Fake

# [contextfake]
class ContextFake(Fake):
    """Now make it work as a context manager."""

    def __init__(self, name, func=None, value=None):
        """Construct."""
        super().__init__(func, value)
        self.name = name
        self.original = None

    def __enter__(self):
        """Replace the original function."""
        assert self.name in globals()
        self.original = globals()[self.name]
        globals()[self.name] = self
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Put everything back."""
        globals()[self.name] = self.original
# [/contextfake]


# [test]
def subber(a, b):
    """Another function to test."""
    return a - b


def check_no_lasting_effects():
    """Make sure the function goes back to working."""
    assert subber(2, 3) == -1
    with ContextFake("subber", value=1234) as fake:
        assert subber(2, 3) == 1234
        assert len(fake.calls) == 1
    assert subber(2, 3) == -1
# [/test]


if __name__ == "__main__":
    run_tests(globals(), "check_")

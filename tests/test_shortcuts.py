# FIXME: Merge with failure reasons test module.

import pytest

import examples
from stories.exceptions import FailureError


def test_failures_in_class_with_list():
    """
    We can define error protocol for all stories in the class using
    `failures_in` shortcut.  It should support simple list of strings.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.shortcuts.SimpleWithList().x()
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.shortcuts.SimpleWithList().x.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failed_because("foo")


def test_failures_in_class_with_enum():
    """
    We can define error protocol for all stories in the class using
    `failures_in` shortcut.  It should support enumerators.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.shortcuts.SimpleWithEnum().x()
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.shortcuts.SimpleWithEnum().x.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failed_because(examples.shortcuts.SimpleWithEnum().x.failures.foo)

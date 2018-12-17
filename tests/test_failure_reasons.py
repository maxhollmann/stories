import enum

import pytest

import examples
from stories.exceptions import FailureError, FailureProtocolError


# Arguments of the Failure class.


def test_reasons_defined_with_list():
    """We can use list of strings to define story failure protocol."""

    # Simple.

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleWithList().x()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.failure_reasons.SimpleWithList().x.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")

    # Substory inheritance.

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().a()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.failure_reasons.SimpleSubstoryWithList().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")

    # Substory DI.

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().a()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.failure_reasons.SubstoryDIWithList().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")


def test_reasons_defined_with_enum():
    """We can use enum class to define story failure protocol."""

    # Simple.

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().x()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SimpleWithEnum().x.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SimpleWithEnum().x.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SimpleWithEnum().x.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SimpleWithEnum().x.failures.foo
    )

    # Substory inheritance.

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SimpleSubstoryWithEnum().a.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SimpleSubstoryWithEnum().a.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SimpleSubstoryWithEnum().a.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SimpleSubstoryWithEnum().a.failures.foo
    )

    # Substory DI.

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SubstoryDIWithEnum().a.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SubstoryDIWithEnum().a.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SubstoryDIWithEnum().a.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SubstoryDIWithEnum().a.failures.foo
    )


def test_wrong_reason_with_list():
    """
    We deny to use wrong reason in stories defined with list of
    strings as its failure protocol.
    """

    # Simple.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().y.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleSubstoryWithList.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().b.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().b.run()
    assert str(exc_info.value) == expected


def test_wrong_reason_with_enum():
    """
    We deny to use wrong reason in stories defined with enum class as
    its failure protocol.
    """

    # Simple.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().y.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleSubstoryWithEnum.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().b.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().b.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_list():
    """
    We deny to use Failure() in stories defined with list of strings
    as its failure protocol.
    """

    # Simple.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().z()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().z.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleSubstoryWithList.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().c.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().c.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_enum():
    """
    We deny to use Failure() in stories defined with enum class as its
    failure protocol.
    """

    # Simple.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().z()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().z.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleSubstoryWithEnum.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().c.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().c.run()
    assert str(exc_info.value) == expected


def test_reason_without_protocol():
    """
    We deny to use Failure('reason') in stories defined without
    failure protocol.
    """

    # Simple.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: ReasonWithSimple.two

Use 'failures' story method to define failure protocol.
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimple().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimple().y.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: ReasonWithSimpleSubstory.two

Use 'failures' story method to define failure protocol.
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimpleSubstory().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimpleSubstory().b.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: ReasonWithSimple.two

Use 'failures' story method to define failure protocol.
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSubstoryDI().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSubstoryDI().b.run()
    assert str(exc_info.value) == expected


# Arguments of the result class methods.


def test_summary_wrong_reason_with_list():
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    # TODO: Check success summary the same way.

    # Simple.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: SimpleWithList.x
""".strip()

    result = examples.failure_reasons.SimpleWithList().x.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: SimpleSubstoryWithList.a
""".strip()

    result = examples.failure_reasons.SimpleSubstoryWithList().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: SubstoryDIWithList.a
""".strip()

    result = examples.failure_reasons.SubstoryDIWithList().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_summary_wrong_reason_with_enum():
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    # TODO: Check success summary the same way.

    # Simple.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: SimpleWithEnum.x
""".strip()

    result = examples.failure_reasons.SimpleWithEnum().x.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: SimpleSubstoryWithEnum.a
""".strip()

    result = examples.failure_reasons.SimpleSubstoryWithEnum().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: SubstoryDIWithEnum.a
""".strip()

    result = examples.failure_reasons.SubstoryDIWithEnum().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_summary_reason_without_protocol():
    """
    Summary classes should deny to use `failed_because` method on
    stories defined without failure protocol.
    """

    # TODO: Check success summary the same way.

    # Simple.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: SummaryWithSimple.z

Use 'failures' story method to define failure protocol.
""".strip()

    result = examples.failure_reasons.SummaryWithSimple().z.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: SummaryWithSimpleSubstory.c

Use 'failures' story method to define failure protocol.
""".strip()

    result = examples.failure_reasons.SummaryWithSimpleSubstory().c.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: SummaryWithSubstoryDI.c

Use 'failures' story method to define failure protocol.
""".strip()

    result = examples.failure_reasons.SummaryWithSubstoryDI().c.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


# Composition of the stories.


def test_substory_protocol_match_with_empty():
    """
    We should allow to use stories composition, if parent story and
    substory does not define failure protocols.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.EmptySubstoryMatch().a()
    assert exc_info.value.reason is None

    result = examples.failure_reasons.EmptySubstoryMatch().a.run()
    assert result.failure_reason is None

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.EmptyDIMatch().a()
    assert exc_info.value.reason is None

    result = examples.failure_reasons.EmptyDIMatch().a.run()
    assert result.failure_reason is None


def test_substory_protocol_match_with_list():
    """
    We should allow to use stories composition, if parent story
    protocol is a superset of the substory protocol.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryMatchWithList().a()
    assert exc_info.value.reason == "foo"

    result = examples.failure_reasons.SimpleSubstoryMatchWithList().a.run()
    assert result.failed_because("foo")

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIMatchWithList().a()
    assert exc_info.value.reason == "foo"

    result = examples.failure_reasons.SubstoryDIMatchWithList().a.run()
    assert result.failed_because("foo")


def test_substory_protocol_match_with_enum():
    """
    We should allow to use stories composition, if parent story
    protocol is a superset of the substory protocol.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryMatchWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SimpleSubstoryMatchWithEnum().a.failures.foo
    )

    result = examples.failure_reasons.SimpleSubstoryMatchWithEnum().a.run()
    assert result.failed_because(
        examples.failure_reasons.SimpleSubstoryMatchWithEnum().a.failures.foo
    )

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIMatchWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SubstoryDIMatchWithEnum().a.failures.foo
    )

    result = examples.failure_reasons.SubstoryDIMatchWithEnum().a.run()
    assert result.failed_because(
        examples.failure_reasons.SubstoryDIMatchWithEnum().a.failures.foo
    )


def test_expand_substory_protocol_empty():
    """
    We expand protocol of composed story if substory does not define
    any protocol.
    """


def test_expand_substory_protocol_list():
    """
    We expand protocol of composed story if substory define protocol
    with list of strings.
    """

    # Substory inheritance.

    examples.failure_reasons.ExpandSimpleSubstoryWithList().a.failures == [
        "foo",
        "bar",
        "baz",
    ]

    result = examples.failure_reasons.ExpandSimpleSubstoryWithList().a()
    assert result is None

    result = examples.failure_reasons.ExpandSimpleSubstoryWithList().a.run()
    assert result.is_success
    assert result.value is None

    # Substory DI.

    examples.failure_reasons.ExpandSubstoryDIWithList().a.failures == [
        "foo",
        "bar",
        "baz",
    ]

    result = examples.failure_reasons.ExpandSubstoryDIWithList().a()
    assert result is None

    result = examples.failure_reasons.ExpandSubstoryDIWithList().a.run()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_enum():
    """
    We expand protocol of composed story if substory define protocol
    with enum class.
    """

    # Substory inheritance.

    assert isinstance(
        examples.failure_reasons.ExpandSimpleSubstoryWithEnum().a.failures,
        enum.EnumMeta,
    )
    assert set(
        examples.failure_reasons.ExpandSimpleSubstoryWithEnum().a.failures.__members__.keys()
    ) == {"foo", "bar", "baz"}

    result = examples.failure_reasons.ExpandSimpleSubstoryWithEnum().a()
    assert result is None

    result = examples.failure_reasons.ExpandSimpleSubstoryWithEnum().a.run()
    assert result.is_success
    assert result.value is None

    # Substory DI.

    assert isinstance(
        examples.failure_reasons.ExpandSubstoryDIWithEnum().a.failures, enum.EnumMeta
    )
    assert set(
        examples.failure_reasons.ExpandSubstoryDIWithEnum().a.failures.__members__.keys()
    ) == {"foo", "bar", "baz"}

    result = examples.failure_reasons.ExpandSubstoryDIWithEnum().a()
    assert result is None

    result = examples.failure_reasons.ExpandSubstoryDIWithEnum().a.run()
    assert result.is_success
    assert result.value is None

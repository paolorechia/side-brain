import pytest

import src.domain as domain


def test_item_classification():
    c = domain.ItemClassification()

    assert c.type_ == domain.ItemClassificationType.E

    c.advance()

    assert c.type_ == domain.ItemClassificationType.D

    c.advance()

    assert c.type_ == domain.ItemClassificationType.C

    c.advance()

    assert c.type_ == domain.ItemClassificationType.B

    c.advance()

    assert c.type_ == domain.ItemClassificationType.A

    c.advance()

    assert c.type_ == domain.ItemClassificationType.APLUS

    c.advance()

    assert c.type_ == domain.ItemClassificationType.APLUS


def test_item_classification_rewind():
    c = domain.ItemClassification()

    types = [
        domain.ItemClassificationType.APLUS,
        domain.ItemClassificationType.A,
        domain.ItemClassificationType.B,
    ]

    for t in types:
        c.type_ = t
        c.rewind()
        assert c.type_ == domain.ItemClassificationType.D

    types = [
        domain.ItemClassificationType.C,
        domain.ItemClassificationType.D,
        domain.ItemClassificationType.E,
    ]

    for t in types:
        c.type_ = t
        c.rewind()
        assert c.type_ == domain.ItemClassificationType.E

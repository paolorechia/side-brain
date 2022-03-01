import pytest

import src as sidebrain


def test_item_classification():
    c = sidebrain.ItemClassification()

    assert c.type_ == sidebrain.ItemClassificationType.E

    c.advance()

    assert c.type_ == sidebrain.ItemClassificationType.D

    c.advance()

    assert c.type_ == sidebrain.ItemClassificationType.C

    c.advance()

    assert c.type_ == sidebrain.ItemClassificationType.B

    c.advance()

    assert c.type_ == sidebrain.ItemClassificationType.A

    c.advance()

    assert c.type_ == sidebrain.ItemClassificationType.APLUS

    c.advance()

    assert c.type_ == sidebrain.ItemClassificationType.APLUS


def test_item_classification_rewind():
    c = sidebrain.ItemClassification()

    types = [
        sidebrain.ItemClassificationType.APLUS,
        sidebrain.ItemClassificationType.A,
        sidebrain.ItemClassificationType.B,
    ]

    for t in types:
        c.type_ = t
        c.rewind()
        assert c.type_ == sidebrain.ItemClassificationType.D

    types = [
        sidebrain.ItemClassificationType.C,
        sidebrain.ItemClassificationType.D,
        sidebrain.ItemClassificationType.E,
    ]

    for t in types:
        c.type_ = t
        c.rewind()
        assert c.type_ == sidebrain.ItemClassificationType.E

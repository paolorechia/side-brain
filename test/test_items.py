import pytest
import src as sidebrain


def test_item_is_instantiable():
    i = sidebrain.Item()
    assert i


def test_item_has_two_sides():
    i = sidebrain.Item()
    assert isinstance(i.visible_side, sidebrain.VisibleSide)
    assert isinstance(i.hidden_side, sidebrain.HiddenSide)

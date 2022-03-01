import pytest
import src as sidebrain


def test_item_history():
    h = sidebrain.ItemHistory()
    h.append(sidebrain.ItemFeedback("EASY"))
    assert h
    assert h[0] == sidebrain.ItemFeedback.EASY
    assert len(h) == 1


def test_item_history_invalid_type():
    h = sidebrain.ItemHistory()
    with pytest.raises(sidebrain.errors.InvalidItemFeedback):
        h.append("EASY")


def test_item_feedback():
    f = sidebrain.ItemFeedback("EASY")
    assert f

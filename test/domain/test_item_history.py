import pytest
import src.domain as domain


def test_item_history():
    h = domain.ItemHistory()
    h.append(domain.ItemFeedback("EASY"))
    assert h
    assert h[0] == domain.ItemFeedback.EASY
    assert len(h) == 1


def test_item_history_invalid_type():
    h = domain.ItemHistory()
    with pytest.raises(domain.errors.InvalidItemFeedback):
        h.append("EASY")


def test_item_feedback():
    f = domain.ItemFeedback("EASY")
    assert f

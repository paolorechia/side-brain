import pytest
import src as sidebrain


def test_item_get_statistics():
    i = sidebrain.Item()

    s = i.get_statistics()
    assert s.total_attempts == 0
    assert s.easy_answers == 0
    assert s.medium_answers == 0
    assert s.hard_answers == 0
    assert s.failed_answers == 0

    i.push_feedback(sidebrain.ItemFeedback.EASY)
    s = i.get_statistics()
    assert s.total_attempts == 1
    assert s.easy_answers == 1
    assert s.medium_answers == 0
    assert s.hard_answers == 0
    assert s.failed_answers == 0

    i.push_feedback(sidebrain.ItemFeedback.MEDIUM)
    i.push_feedback(sidebrain.ItemFeedback.MEDIUM)
    s = i.get_statistics()
    assert s.total_attempts == 3
    assert s.easy_answers == 1
    assert s.medium_answers == 2
    assert s.hard_answers == 0
    assert s.failed_answers == 0

    i.push_feedback(sidebrain.ItemFeedback.HARD)
    i.push_feedback(sidebrain.ItemFeedback.HARD)
    i.push_feedback(sidebrain.ItemFeedback.HARD)
    s = i.get_statistics()
    assert s.total_attempts == 6
    assert s.easy_answers == 1
    assert s.medium_answers == 2
    assert s.hard_answers == 3
    assert s.failed_answers == 0

    i.push_feedback(sidebrain.ItemFeedback.FAILED)
    s = i.get_statistics()
    assert s.total_attempts == 7
    assert s.easy_answers == 1
    assert s.medium_answers == 2
    assert s.hard_answers == 3
    assert s.failed_answers == 1

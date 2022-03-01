import pytest
import src as sidebrain


def test_answer_diff():
    diff = sidebrain.AnswerDiff("abc", "abc")
    assert diff.matches == True
    assert diff.first_different_index == -1

    diff = sidebrain.AnswerDiff("abcde", "abc")
    assert diff.matches == False
    assert diff.first_different_index == 3

    diff = sidebrain.AnswerDiff("abc", "abcde")
    assert diff.matches == False
    assert diff.first_different_index == 3

    diff = sidebrain.AnswerDiff("abc", "acd")
    assert diff.matches == False
    assert diff.first_different_index == 1


def test_answer_diff_empty_answer():
    with pytest.raises(sidebrain.EmptyAnswerException):
        sidebrain.AnswerDiff(None, "abc")

import pytest
import src.domain as domain


def test_answer_diff():
    diff = domain.AnswerDiff("abc", "abc")
    assert diff.matches == True
    assert diff.first_different_index == -1

    diff = domain.AnswerDiff("abcde", "abc")
    assert diff.matches == False
    assert diff.first_different_index == 3

    diff = domain.AnswerDiff("abc", "abcde")
    assert diff.matches == False
    assert diff.first_different_index == 3

    diff = domain.AnswerDiff("abc", "acd")
    assert diff.matches == False
    assert diff.first_different_index == 1


def test_answer_diff_empty_answer():
    with pytest.raises(domain.errors.EmptyAnswerException):
        domain.AnswerDiff(None, "abc")

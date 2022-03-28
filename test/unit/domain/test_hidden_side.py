import pytest

import src.domain as domain


def test_hidden_side_check_answer():
    hidden = domain.HiddenSide()

    hidden.set_answer("my answer")

    check1 = hidden.check_answer("my answer")
    assert isinstance(check1, domain.AnswerDiff)
    assert check1.matches == True

    check2 = hidden.check_answer("my stub")
    assert isinstance(check1, domain.AnswerDiff)
    assert check2.matches == False
    assert check2.first_different_index == 3


def test_hidden_side_check_answer_raises_exception():
    with pytest.raises(domain.errors.AnswerNotSetException) as excp:
        check1 = domain.HiddenSide().check_answer("my answer")

import pytest
import src as sidebrain


def test_hidden_side_is_correct_answer():
    hidden = sidebrain.HiddenSide()

    hidden.set_answer("my answer")

    assert hidden.is_correct_answer("duh") == False
    assert hidden.is_correct_answer("my answer") == True


def test_hidden_side_check_answer():
    hidden = sidebrain.HiddenSide()

    hidden.set_answer("my answer")

    check1 = hidden.check_answer("my answer")
    assert isinstance(check1, sidebrain.AnswerDiff)
    assert check1.matches == True

    check2 = hidden.check_answer("my stub")
    assert isinstance(check1, sidebrain.AnswerDiff)
    assert check2.matches == False
    assert check2.first_different_index == 3


def test_hidden_side_check_answer_raises_exception():
    with pytest.raises(sidebrain.AnswerNotSetException) as excp:
        check1 = sidebrain.HiddenSide().check_answer("my answer")

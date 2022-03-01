import pytest
import src as sidebrain


def test_item_is_instantiable():
    i = sidebrain.Item()
    assert i


def test_item_has_two_sides():
    i = sidebrain.Item()
    assert isinstance(i.visible_side, sidebrain.VisibleSide)
    assert isinstance(i.hidden_side, sidebrain.HiddenSide)


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


def test_hidden_side_check_answer_raises_exception():
    with pytest.raises(sidebrain.AnswerNotSetException) as excp:
        check1 = sidebrain.HiddenSide().check_answer("my answer")


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

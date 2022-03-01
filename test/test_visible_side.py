import pytest
import src as sidebrain


def test_visible_side_is_initializable():
    assert sidebrain.VisibleSide()


def test_visible_side_does_not_implement_get():
    with pytest.raises(sidebrain.errors.VisibleSideNotShowableException):
        sidebrain.VisibleSide().get()


def test_text_side():
    text_side = sidebrain.TextSide("question")
    assert text_side.get() == "question"


def test_image_side():
    image_side = sidebrain.ImageSide("https://link.com")
    assert image_side.get() == "https://link.com"


def test_multiplechoice_side():
    multiple_choice = sidebrain.MultipleChoiceSide(["a", "b"])
    assert multiple_choice.get() == ["a", "b"]


def test_fillin_side():
    fillin_side = sidebrain.FillInSide("question ___ wow")
    assert fillin_side.get() == "question ___ wow"

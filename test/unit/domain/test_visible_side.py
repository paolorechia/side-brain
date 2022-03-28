import pytest

import src.domain as domain


def test_visible_side_is_initializable():
    assert domain.VisibleSide()


def test_visible_side_does_not_implement_get():
    with pytest.raises(domain.errors.VisibleSideNotShowableException):
        domain.VisibleSide().get()


def test_text_side():
    text_side = domain.TextSide("question")
    assert text_side.get() == "question"


def test_text_side_errors():
    with pytest.raises(domain.errors.EmptyQuestionException):
        text_side = domain.TextSide("")

    with pytest.raises(domain.errors.EmptyQuestionException):
        text_side = domain.TextSide(None)

    with pytest.raises(domain.errors.InvalidQuestionType):
        text_side = domain.TextSide(2)


def test_image_side():
    image_side = domain.ImageSide("https://link.com")
    assert image_side.get() == "https://link.com"

    image_side = domain.ImageSide("https://link.com/wow/cat.png")

    assert image_side.get() == "https://link.com/wow/cat.png"


def test_image_side_errors():
    with pytest.raises(domain.errors.EmptyQuestionException):
        image_side = domain.ImageSide("")

    with pytest.raises(domain.errors.EmptyQuestionException):
        image_side = domain.ImageSide(None)

    with pytest.raises(domain.errors.InvalidQuestionType):
        image_side = domain.ImageSide(2)

    with pytest.raises(domain.errors.InvalidQuestionType):
        image_side = domain.ImageSide("Aaaa")


def test_multiplechoice_side():
    multiple_choice = domain.MultipleChoiceSide(["a", "b"])
    assert multiple_choice.get() == ["a", "b"]


def test_multiplechoice_side_errors():
    with pytest.raises(domain.errors.EmptyQuestionException):
        text_side = domain.MultipleChoiceSide([])

    with pytest.raises(domain.errors.InvalidQuestionType):
        text_side = domain.MultipleChoiceSide(["a"])

    with pytest.raises(domain.errors.InvalidQuestionType):
        text_side = domain.MultipleChoiceSide(["a", 2])

    with pytest.raises(domain.errors.InvalidQuestionType):
        text_side = domain.MultipleChoiceSide("bla")


def test_fillin_side():
    fillin_side = domain.FillInSide("question ___ wow")
    assert fillin_side.get() == "question ___ wow"


def test_fill_in_errors():
    with pytest.raises(domain.errors.EmptyQuestionException):
        text_side = domain.FillInSide("")

    with pytest.raises(domain.errors.EmptyQuestionException):
        text_side = domain.FillInSide(None)

    with pytest.raises(domain.errors.InvalidQuestionType):
        text_side = domain.FillInSide(2)

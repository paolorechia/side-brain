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


def test_text_side_errors():
    with pytest.raises(sidebrain.errors.EmptyQuestionException):
        text_side = sidebrain.TextSide("")

    with pytest.raises(sidebrain.errors.EmptyQuestionException):
        text_side = sidebrain.TextSide(None)

    with pytest.raises(sidebrain.errors.InvalidQuestionType):
        text_side = sidebrain.TextSide(2)


def test_image_side():
    image_side = sidebrain.ImageSide("https://link.com")
    assert image_side.get() == "https://link.com"

    image_side = sidebrain.ImageSide("https://link.com/wow/cat.png")

    assert image_side.get() == "https://link.com/wow/cat.png"


def test_image_side_errors():
    with pytest.raises(sidebrain.errors.EmptyQuestionException):
        image_side = sidebrain.ImageSide("")

    with pytest.raises(sidebrain.errors.EmptyQuestionException):
        image_side = sidebrain.ImageSide(None)

    with pytest.raises(sidebrain.errors.InvalidQuestionType):
        image_side = sidebrain.ImageSide(2)

    with pytest.raises(sidebrain.errors.InvalidQuestionType):
        image_side = sidebrain.ImageSide("Aaaa")


def test_multiplechoice_side():
    multiple_choice = sidebrain.MultipleChoiceSide(["a", "b"])
    assert multiple_choice.get() == ["a", "b"]


def test_multiplechoice_side_errors():
    with pytest.raises(sidebrain.errors.EmptyQuestionException):
        text_side = sidebrain.MultipleChoiceSide([])

    with pytest.raises(sidebrain.errors.InvalidQuestionType):
        text_side = sidebrain.MultipleChoiceSide(["a"])

    with pytest.raises(sidebrain.errors.InvalidQuestionType):
        text_side = sidebrain.MultipleChoiceSide(["a", 2])

    with pytest.raises(sidebrain.errors.InvalidQuestionType):
        text_side = sidebrain.MultipleChoiceSide("bla")


def test_fillin_side():
    fillin_side = sidebrain.FillInSide("question ___ wow")
    assert fillin_side.get() == "question ___ wow"


def test_fill_in_errors():
    with pytest.raises(sidebrain.errors.EmptyQuestionException):
        text_side = sidebrain.FillInSide("")

    with pytest.raises(sidebrain.errors.EmptyQuestionException):
        text_side = sidebrain.FillInSide(None)

    with pytest.raises(sidebrain.errors.InvalidQuestionType):
        text_side = sidebrain.FillInSide(2)

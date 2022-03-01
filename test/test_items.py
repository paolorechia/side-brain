import pytest
import src as sidebrain


def test_item_is_instantiable():
    i = sidebrain.Item()
    assert i
    assert isinstance(i.history, sidebrain.ItemHistory)


def test_item_has_two_sides():
    i = sidebrain.Item()
    assert isinstance(i.visible_side, sidebrain.VisibleSide)
    assert isinstance(i.hidden_side, sidebrain.HiddenSide)


def test_item_starts_empty():
    i = sidebrain.Item()
    with pytest.raises(sidebrain.errors.VisibleSideNotShowableException):
        i.visible_side.get()


def test_item_classification_behavior():
    i = sidebrain.Item()
    assert len(i.history) == 0
    i.push_feedback(sidebrain.ItemFeedback.EASY)
    assert len(i.history) == 1


@pytest.mark.parametrize(
    "feedbacks, expected_classification",
    [
        ([], sidebrain.ItemClassificationType.E),
        ([sidebrain.ItemFeedback.EASY], sidebrain.ItemClassificationType.D),
        (
            [sidebrain.ItemFeedback.EASY, sidebrain.ItemFeedback.EASY],
            sidebrain.ItemClassificationType.C,
        ),
        (
            [sidebrain.ItemFeedback.EASY, sidebrain.ItemFeedback.EASY],
            sidebrain.ItemClassificationType.C,
        ),
        ([sidebrain.ItemFeedback.MEDIUM], sidebrain.ItemClassificationType.E),
        (
            [sidebrain.ItemFeedback.MEDIUM, sidebrain.ItemFeedback.MEDIUM],
            sidebrain.ItemClassificationType.D,
        ),
        ([sidebrain.ItemFeedback.HARD], sidebrain.ItemClassificationType.E),
        (
            [sidebrain.ItemFeedback.HARD, sidebrain.ItemFeedback.HARD],
            sidebrain.ItemClassificationType.E,
        ),
        (
            [
                sidebrain.ItemFeedback.HARD,
                sidebrain.ItemFeedback.HARD,
                sidebrain.ItemFeedback.HARD,
            ],
            sidebrain.ItemClassificationType.D,
        ),
        ([sidebrain.ItemFeedback.FAILED], sidebrain.ItemClassificationType.E),
        (
            [
                sidebrain.ItemFeedback.EASY,
                sidebrain.ItemFeedback.FAILED,
            ],
            sidebrain.ItemClassificationType.E,
        ),
        (
            [
                sidebrain.ItemFeedback.EASY,
                sidebrain.ItemFeedback.FAILED,
                sidebrain.ItemFeedback.EASY,
            ],
            sidebrain.ItemClassificationType.D,
        ),
        (
            [
                sidebrain.ItemFeedback.EASY,
                sidebrain.ItemFeedback.FAILED,
                sidebrain.ItemFeedback.MEDIUM,
                sidebrain.ItemFeedback.MEDIUM,
            ],
            sidebrain.ItemClassificationType.D,
        ),
    ],
)
def test_item_classification_behavior(feedbacks, expected_classification):
    i = sidebrain.Item()
    for f in feedbacks:
        i.push_feedback(f)

    assert i.classification.type_ == expected_classification


def test_item_empty_history():
    i = sidebrain.Item()
    i._compute_classification()
    assert i.classification.type_ == sidebrain.ItemClassificationType.E

    assert i.history.__repr__()


def test_item_text_type():
    i = sidebrain.Item()

    i.set_text_type("side a")
    i.set_answer("side b")

    assert i.visible_side.name == "Text"

    assert i.visible_side.get() == "side a"
    assert isinstance(i.visible_side, sidebrain.TextSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches


def test_item_image_type():
    i = sidebrain.Item()

    i.set_image_type("https://link.com")
    i.set_answer("side b")

    assert i.visible_side.name == "Image"

    assert i.visible_side.get() == "https://link.com"
    assert isinstance(i.visible_side, sidebrain.ImageSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches


def test_item_multiple_choices_type():
    i = sidebrain.Item()

    i.set_multiple_choice_type(["a", "b"])
    i.set_answer("side b")

    assert i.visible_side.name == "MultipleChoice"

    assert i.visible_side.get() == ["a", "b"]
    assert isinstance(i.visible_side, sidebrain.MultipleChoiceSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches


def test_item_fill_in_type():
    i = sidebrain.Item()

    i.set_fill_in_type("side a")
    i.set_answer("side b")

    assert i.visible_side.name == "FillIn"

    assert i.visible_side.get() == "side a"
    assert isinstance(i.visible_side, sidebrain.FillInSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches

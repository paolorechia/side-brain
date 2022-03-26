import pytest
import src.domain as domain
from datetime import datetime


def test_item_is_instantiable():
    i = domain.Item()
    assert i
    assert isinstance(i.history, domain.ItemHistory)


def test_item_has_two_sides():
    i = domain.Item()
    assert isinstance(i.visible_side, domain.VisibleSide)
    assert isinstance(i.hidden_side, domain.HiddenSide)


def test_item_starts_empty():
    i = domain.Item()
    with pytest.raises(domain.errors.VisibleSideNotShowableException):
        i.visible_side.get()


def test_item_classification_behavior():
    i = domain.Item()
    assert len(i.history) == 0
    i.push_feedback(domain.ItemFeedback.EASY)
    assert len(i.history) == 1


@pytest.mark.parametrize(
    "feedbacks, expected_classification",
    [
        ([], domain.ItemClassificationType.E),
        ([domain.ItemFeedback.EASY], domain.ItemClassificationType.D),
        (
            [domain.ItemFeedback.EASY, domain.ItemFeedback.EASY],
            domain.ItemClassificationType.C,
        ),
        (
            [domain.ItemFeedback.EASY, domain.ItemFeedback.EASY],
            domain.ItemClassificationType.C,
        ),
        ([domain.ItemFeedback.MEDIUM], domain.ItemClassificationType.E),
        (
            [domain.ItemFeedback.MEDIUM, domain.ItemFeedback.MEDIUM],
            domain.ItemClassificationType.D,
        ),
        ([domain.ItemFeedback.HARD], domain.ItemClassificationType.E),
        (
            [domain.ItemFeedback.HARD, domain.ItemFeedback.HARD],
            domain.ItemClassificationType.E,
        ),
        (
            [
                domain.ItemFeedback.HARD,
                domain.ItemFeedback.HARD,
                domain.ItemFeedback.HARD,
            ],
            domain.ItemClassificationType.D,
        ),
        ([domain.ItemFeedback.FAILED], domain.ItemClassificationType.E),
        (
            [
                domain.ItemFeedback.EASY,
                domain.ItemFeedback.FAILED,
            ],
            domain.ItemClassificationType.E,
        ),
        (
            [
                domain.ItemFeedback.EASY,
                domain.ItemFeedback.FAILED,
                domain.ItemFeedback.EASY,
            ],
            domain.ItemClassificationType.D,
        ),
        (
            [
                domain.ItemFeedback.EASY,
                domain.ItemFeedback.FAILED,
                domain.ItemFeedback.MEDIUM,
                domain.ItemFeedback.MEDIUM,
            ],
            domain.ItemClassificationType.D,
        ),
    ],
)
def test_item_classification_behavior(feedbacks, expected_classification):
    i = domain.Item()
    for f in feedbacks:
        i.push_feedback(f)

    assert i.classification.type_ == expected_classification


@pytest.mark.parametrize(
    "classification_type, expected_time_delta_in_days",
    [
        (domain.ItemClassificationType.E, 0),
        (domain.ItemClassificationType.D, 1),
        (domain.ItemClassificationType.C, 7),
        (domain.ItemClassificationType.B, 14),
        (domain.ItemClassificationType.A, 28),
        (domain.ItemClassificationType.APLUS, 90),
    ],
)
def test_item_wait_until(classification_type, expected_time_delta_in_days):
    i = domain.Item()
    i.classification.type_ = classification_type
    i.update_wait_time()
    now = datetime.now()
    day_diff = (i.wait_until - now).days
    assert day_diff == expected_time_delta_in_days - 1
    if expected_time_delta_in_days == 0:
        assert now > i.wait_until
    else:
        assert i.wait_until.hour == 0
        assert i.wait_until.minute == 0
        assert i.wait_until.second == 0


def test_item_empty_history():
    i = domain.Item()
    i._compute_classification()
    assert i.classification.type_ == domain.ItemClassificationType.E

    assert i.history.__repr__()


def test_item_text_type():
    i = domain.Item()

    i.set_text_type("side a")
    i.set_answer("side b")

    assert i.visible_side.name == "Text"

    assert i.visible_side.get() == "side a"
    assert isinstance(i.visible_side, domain.TextSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches


def test_item_image_type():
    i = domain.Item()

    i.set_image_type("https://link.com")
    i.set_answer("side b")

    assert i.visible_side.name == "Image"

    assert i.visible_side.get() == "https://link.com"
    assert isinstance(i.visible_side, domain.ImageSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches


def test_item_multiple_choices_type():
    i = domain.Item()

    i.set_multiple_choice_type(["a", "b"])
    i.set_answer("side b")

    assert i.visible_side.name == "MultipleChoice"

    assert i.visible_side.get() == ["a", "b"]
    assert isinstance(i.visible_side, domain.MultipleChoiceSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches


def test_item_fill_in_type():
    i = domain.Item()

    i.set_fill_in_type("side a")
    i.set_answer("side b")

    assert i.visible_side.name == "FillIn"

    assert i.visible_side.get() == "side a"
    assert isinstance(i.visible_side, domain.FillInSide)

    assert i.check_answer("side b").matches
    assert not i.check_answer("abc").matches

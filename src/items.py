from typing import List, Optional
from src.answer_diff import AnswerDiff
import src.errors as errors


class Item:
    def __init__(self):
        self.visible_side = VisibleSide()
        self.hidden_side = HiddenSide()

    def set_text_type(self, textual_hint: str):
        self.visible_side = TextSide(textual_hint)

    def set_image_type(self, image_link: str):
        self.visible_side = ImageSide(image_link)

    def set_multiple_choice_type(self, options: List[str]):
        self.visible_side = MultipleChoiceSide(options)

    def set_fill_in_type(self, textual_hint: str):
        self.visible_side = FillInSide(textual_hint)

    def set_answer(self, expected_answer: str):
        self.hidden_side.set_answer(expected_answer)

    def check_answer(self, given_answer: str) -> AnswerDiff:
        return self.hidden_side.check_answer(given_answer)


class VisibleSide:
    def __init__(self):
        self.type_ = VisibleSide

    def get(self):
        raise errors.VisibleSideNotShowableException(
            "Please use a specific Visible Side"
        )


class TextSide(VisibleSide):
    def __init__(self, text):
        self.text = text

    @property
    def name(self):
        return "Text"

    def get(self):
        return self.text


class ImageSide(VisibleSide):
    def __init__(self, text):
        self.text = text

    @property
    def name(self):
        return "Image"

    def get(self):
        return self.text


class MultipleChoiceSide(VisibleSide):
    def __init__(self, options: List[str]):
        self.options = options

    @property
    def name(self):
        return "MultipleChoice"

    def get(self):
        return self.options


class FillInSide(VisibleSide):
    def __init__(self, text):
        self.text = text

    @property
    def name(self):
        return "FillIn"

    def get(self):
        return self.text


class HiddenSide:
    def __init__(self):
        self.answer: Optional[str] = None

    def set_answer(self, answer: str):
        self.answer = answer

    def check_answer(self, answer: str):
        if not self.answer:
            raise errors.AnswerNotSetException("Answer is not set")
        return AnswerDiff(answer, self.answer)


class ItemType:
    EMPTY = VisibleSide
    TEXT = TextSide
    IMAGE = ImageSide
    MULTIPLE_CHOICES = MultipleChoiceSide
    FILL_IN = FillInSide

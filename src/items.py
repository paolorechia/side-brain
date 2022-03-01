from typing import List, Optional
from src.answer_diff import AnswerDiff
import src.errors as errors

import enum
import re

_LINK_REGEX = re.compile("https://.+")


class ItemFeedback(enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    FAILED = "FAILED"


class ItemClassificationType(enum.Enum):
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    APLUS = "APLUS"


class ItemClassification:

    ADVANCE_RULES = {
        "E": "D",
        "D": "C",
        "C": "B",
        "B": "A",
        "A": "APLUS",
        "APLUS": "APLUS",
    }
    REWIND_RULES = {"APLUS": "D", "A": "D", "B": "D", "C": "E", "D": "E", "E": "E"}

    def __init__(self):
        self.type_ = ItemClassificationType.E

    def advance(self):
        self.type_ = ItemClassificationType(
            ItemClassification.ADVANCE_RULES[self.type_.value]
        )

    def rewind(self):
        self.type_ = ItemClassificationType(
            ItemClassification.REWIND_RULES[self.type_.value]
        )


class ItemHistory:
    def __init__(self):
        self._: List[ItemFeedback] = []

    def __len__(self):
        return len(self._)

    def __getitem__(self, index):
        return self._[index]

    def append(self, item: ItemFeedback):
        if not isinstance(item, ItemFeedback):
            raise errors.InvalidItemFeedback()

        self._.append(item)


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
    def __init__(self, text: str):
        if not text:
            raise errors.EmptyQuestionException()
        if not isinstance(text, str):
            raise errors.InvalidQuestionType()
        self.text = text

    @property
    def name(self):
        return "Text"

    def get(self):
        return self.text


class ImageSide(VisibleSide):
    def __init__(self, link: str):
        if not link:
            raise errors.EmptyQuestionException()
        if not isinstance(link, str):
            raise errors.InvalidQuestionType()
        if not re.match(_LINK_REGEX, link):
            raise errors.InvalidQuestionType()
        self.link = link

    @property
    def name(self):
        return "Image"

    def get(self):
        return self.link


class MultipleChoiceSide(VisibleSide):
    def __init__(self, options: List[str]):
        if not options:
            raise errors.EmptyQuestionException()
        if not isinstance(options, list):
            raise errors.InvalidQuestionType()
        if len(options) < 2:
            raise errors.InvalidQuestionType()
        types_ = set([type(o) for o in options])
        if len(types_) > 1:
            raise errors.InvalidQuestionType()

        self.options = options

    @property
    def name(self):
        return "MultipleChoice"

    def get(self):
        return self.options


class FillInSide(TextSide):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def name(self):
        return "FillIn"


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

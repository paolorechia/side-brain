from typing import Optional


class AnswerNotSetException(Exception):
    pass


class EmptyAnswerException(Exception):
    pass


class Item:
    def __init__(self):
        self.visible_side = VisibleSide()
        self.hidden_side = HiddenSide()


class VisibleSide:
    def __init__(self):
        pass


class HiddenSide:
    def __init__(self):
        self.answer: Optional[str] = None

    def set_answer(self, answer: str):
        self.answer = answer

    def is_correct_answer(self, answer: str):
        return self.answer == answer

    def check_answer(self, answer: str):
        if not self.answer:
            raise AnswerNotSetException("Answer is not set")
        return AnswerDiff(answer, self.answer)


class AnswerDiff:
    def __init__(self, given_answer: Optional[str], expected_answer: str):
        if not given_answer:
            raise EmptyAnswerException("No answer was provided")

        self.matches = len(given_answer) == len(expected_answer)
        self.first_different_index = -1

        if len(expected_answer) >= len(given_answer):
            right_side = expected_answer
            left_side = given_answer
        else:
            right_side = given_answer
            left_side = expected_answer

        for i, char_ in enumerate(right_side):
            try:
                if left_side[i] != char_:
                    self.matches = False
                    self.first_different_index = i
                    break
            except IndexError:
                self.matches = False
                self.first_different_index = i
                break

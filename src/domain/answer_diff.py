from typing import Optional
import src.domain.errors as errors


class AnswerDiff:
    def __init__(self, given_answer: Optional[str], expected_answer: str):
        if not given_answer:
            raise errors.EmptyAnswerException("No answer was provided")

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

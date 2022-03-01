class AnswerNotSetException(Exception):
    pass


class EmptyAnswerException(Exception):
    pass


class EmptyQuestionException(Exception):
    pass


class InvalidQuestionType(Exception):
    pass


class InvalidItemType(Exception):
    pass


class VisibleSideNotShowableException(NotImplementedError):
    pass

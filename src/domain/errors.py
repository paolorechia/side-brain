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


class InvalidItemFeedback(Exception):
    pass


class VisibleSideNotShowableException(NotImplementedError):
    pass


class NoItemToAnswerException(Exception):
    pass


class InvalidCollectionName(Exception):
    pass


class InvalidCollectionObject(Exception):
    pass


class NoCollectionToInspect(Exception):
    pass

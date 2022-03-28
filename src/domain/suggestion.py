from collections import Counter
from datetime import datetime

import src.domain.errors as errors

from .collections import Collection
from .items import ItemClassificationType


class Suggestions:
    def __init__(self):
        self.collections = []

    def __len__(self):
        return len(self.collections)

    def suggest(self) -> Collection:
        if not self.collections:
            raise errors.NoCollectionToInspect()
        now = datetime.now()

        may_be_used = []
        for col in self.collections:
            for i in col.items:
                if i.wait_until < now:
                    may_be_used.append(col)
                    break

        counters = []
        for col in may_be_used:
            types_ = [i.classification.type_.value for i in col.items]
            counters.append(Counter(types_))

        suggestion_score = []
        for c in counters:
            score = 0
            score += (
                c[ItemClassificationType.APLUS.value] * 1000000000000000000000000000000
            )
            score += c[ItemClassificationType.A.value] * 1000000000000000000
            score += c[ItemClassificationType.B.value] * 1000000000
            score += c[ItemClassificationType.C.value] * 100000
            score += c[ItemClassificationType.D.value] * 100
            score += c[ItemClassificationType.E.value] * 1

            suggestion_score.append(score)

        suggestions = list(zip(may_be_used, suggestion_score))
        suggestions.sort(key=lambda x: x[1])
        return suggestions[-1][0]

    def add(self, collection: Collection):
        if not collection:
            raise errors.InvalidCollectionObject()
        if not isinstance(collection, Collection):
            raise errors.InvalidCollectionObject()
        self.collections.append(collection)

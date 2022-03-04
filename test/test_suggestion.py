import pytest

from datetime import datetime
import src as sidebrain


def test_suggestion():
    c = sidebrain.Collection()
    c.set_name("Helles")

    c2 = sidebrain.Collection()

    c2.set_name("Radler")

    for i in range(5):
        item = sidebrain.Item()
        item.set_answer(str(i))
        item.set_text_type(str(i))
        item.classification.type_ = sidebrain.ItemClassificationType.APLUS
        item.wait_until = datetime.now()
        c.add(item)

    for i in range(10):
        item = sidebrain.Item()
        item.set_answer(str(i))
        item.set_text_type(str(i))
        item.classification.type_ = sidebrain.ItemClassificationType.C
        item.wait_until = datetime.now()
        c2.add(item)

    s = Suggestions()
    suggested = s.suggest()
    assert suggested.name == "Helles"

import pytest

from datetime import datetime
import src as sidebrain


def test_suggestion_add():
    c = sidebrain.Collection()
    c.set_name("Helles")

    c.add(sidebrain.Item())
    c2 = sidebrain.Collection()

    c2.set_name("Radler")
    c2.add(sidebrain.Item())

    s = sidebrain.Suggestions()

    s.add(c)
    s.add(c2)

    assert len(s) == 2


def test_suggestion_add_raises_errors():

    s = sidebrain.Suggestions()

    with pytest.raises(sidebrain.errors.InvalidCollectionObject):
        s.add("")

    with pytest.raises(sidebrain.errors.InvalidCollectionObject):
        s.add(None)

    with pytest.raises(sidebrain.errors.InvalidCollectionObject):
        s.add(sidebrain.Item())

    with pytest.raises(sidebrain.errors.InvalidCollectionObject):
        s.add(sidebrain.Collection())

    with pytest.raises(sidebrain.errors.NoCollectionToInspect):
        s.suggest()


def test_suggestion_suggest():
    c = sidebrain.Collection()
    c.set_name("Helles")

    c2 = sidebrain.Collection()

    c2.set_name("Radler")

    for i in range(5):
        item = sidebrain.Item()
        item.set_answer(str(i))
        item.set_text_type(str(i))
        item.classification.type_ = sidebrain.ItemClassificationType.B
        item.wait_until = datetime.now()
        c.add(item)

    for i in range(10):
        item = sidebrain.Item()
        item.set_answer(str(i))
        item.set_text_type(str(i))
        item.classification.type_ = sidebrain.ItemClassificationType.C
        item.wait_until = datetime.now()
        c2.add(item)

    s = sidebrain.Suggestions()
    s.add(c)
    s.add(c2)

    suggested = s.suggest()
    assert suggested.name == "Helles"

from datetime import datetime

import pytest

import src.domain as domain


def test_suggestion_add():
    c = domain.Collection()
    c.set_name("Helles")

    c.add(domain.Item())
    c2 = domain.Collection()

    c2.set_name("Radler")
    c2.add(domain.Item())

    s = domain.Suggestions()

    s.add(c)
    s.add(c2)

    assert len(s) == 2


def test_suggestion_add_raises_errors():

    s = domain.Suggestions()

    with pytest.raises(domain.errors.InvalidCollectionObject):
        s.add("")

    with pytest.raises(domain.errors.InvalidCollectionObject):
        s.add(None)

    with pytest.raises(domain.errors.InvalidCollectionObject):
        s.add(domain.Item())

    with pytest.raises(domain.errors.InvalidCollectionObject):
        s.add(domain.Collection())

    with pytest.raises(domain.errors.NoCollectionToInspect):
        s.suggest()


def test_suggestion_suggest():
    c = domain.Collection()
    c.set_name("Helles")

    c2 = domain.Collection()

    c2.set_name("Radler")

    for i in range(5):
        item = domain.Item()
        item.set_answer(str(i))
        item.set_text_type(str(i))
        item.classification.type_ = domain.ItemClassificationType.B
        item.wait_until = datetime.now()
        c.add(item)

    for i in range(10):
        item = domain.Item()
        item.set_answer(str(i))
        item.set_text_type(str(i))
        item.classification.type_ = domain.ItemClassificationType.C
        item.wait_until = datetime.now()
        c2.add(item)

    s = domain.Suggestions()
    s.add(c)
    s.add(c2)

    suggested = s.suggest()
    assert suggested.name == "Helles"

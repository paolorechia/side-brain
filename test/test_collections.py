import src as sidebrain


def test_collection_starts_empty():
    c = sidebrain.Collection()
    assert len(c) == 0


def test_collection_add_item():
    c = sidebrain.Collection()

    item = sidebrain.Item()
    item.set_text_type("a")
    item.set_answer("b")

    c.add(item)
    assert len(c) == 1


def test_empty_collection_next_returns_none():
    c = sidebrain.Collection()
    item = c.next()
    assert not item

import pytest
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


def test_collection_answer_item_errors():
    c = sidebrain.Collection()
    _ = c.next()
    with pytest.raises(sidebrain.errors.InvalidItemFeedback):
        c.answer_item("a")

    with pytest.raises(sidebrain.errors.NoItemToAnswerException):
        c.answer_item(sidebrain.ItemFeedback.HARD)


def test_collection_next():
    c = sidebrain.Collection()

    def create_stub_item(i):
        item = sidebrain.Item()
        item.set_text_type(i)
        item.set_answer(i)
        return item

    for i in range(5):
        c.add(create_stub_item(str(i)))

    for i in range(5):
        item = c.next()
        assert item.check_answer(str(i))
        c.answer_item(sidebrain.ItemFeedback.EASY)

    # Finishes
    assert not c.next()


def test_collection_next_with_medium():
    c = sidebrain.Collection()

    item = sidebrain.Item()
    item.set_text_type("a")
    item.set_answer("a")

    c.add(item)
    for i in range(2):
        _ = c.next()
        print(i)
        c.answer_item(sidebrain.ItemFeedback.MEDIUM)
        c.answer_item(sidebrain.ItemFeedback.MEDIUM)

    # Finishes
    assert not c.next()


def test_collection_next_with_hard():
    c = sidebrain.Collection()

    item = sidebrain.Item()
    item.set_text_type("a")
    item.set_answer("a")

    c.add(item)
    for i in range(3):
        _ = c.next()
        print(i)
        c.answer_item(sidebrain.ItemFeedback.HARD)
        c.answer_item(sidebrain.ItemFeedback.HARD)
        c.answer_item(sidebrain.ItemFeedback.HARD)

    # Finishes
    assert not c.next()


def test_collection_next_with_failed():
    c = sidebrain.Collection()

    def create_stub_item(i):
        item = sidebrain.Item()
        item.set_text_type(i)
        item.set_answer(i)
        return item

    for i in range(5):
        c.add(create_stub_item(str(i)))

    for i in range(6):
        _ = c.next()
        if i == 0:
            c.answer_item(sidebrain.ItemFeedback.FAILED)
        else:
            c.answer_item(sidebrain.ItemFeedback.EASY)

    # Finishes
    assert not c.next()


def test_collection_ignores_items_with_wait_time():
    raise NotImplementedError()

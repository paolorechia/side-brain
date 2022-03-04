import pytest
import src as sidebrain


def test_collection_starts_empty():
    c = sidebrain.Collection()
    assert len(c) == 0


def test_collection_set_name():
    c = sidebrain.Collection()
    c.set_name("bah")
    assert c.name == "bah"


def test_collection_set_name_raises_errors():
    c = sidebrain.Collection()

    with pytest.raises(sidebrain.errors.InvalidCollectionName):
        c.set_name("")

    with pytest.raises(sidebrain.errors.InvalidCollectionName):
        c.set_name(None)

    with pytest.raises(sidebrain.errors.InvalidCollectionName):
        c.set_name(123)

    with pytest.raises(sidebrain.errors.InvalidCollectionName):
        c.set_name(["ahoy"])


def test_collection_add_item():
    c = sidebrain.Collection()

    item = sidebrain.Item()
    item.set_text_type("a")
    item.set_answer("b")

    c.add(item)
    assert len(c) == 1


def test_collection_add_item_raises_errors():
    c = sidebrain.Collection()

    with pytest.raises(sidebrain.errors.InvalidItemType):
        c.add("garbage")

    with pytest.raises(sidebrain.errors.InvalidItemType):
        c.add(None)

    with pytest.raises(sidebrain.errors.InvalidItemType):
        c.add(123)


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

    _ = c.next()
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

    _ = c.next()

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
    item = sidebrain.Item()
    item.set_text_type("a")
    item.set_answer("a")

    wait = sidebrain.Item()
    wait.set_text_type("wait")
    wait.set_answer("wait")
    wait.push_feedback(sidebrain.ItemFeedback.EASY)

    c = sidebrain.Collection()
    c.add(item)
    c.add(wait)

    item = c.next()
    assert item.check_answer("a")
    c.answer_item(sidebrain.ItemFeedback.EASY)

    empty = c.next()
    assert not empty


def test_collection_shuffles_change_orders():
    c = sidebrain.Collection()

    for i in range(100):
        item = sidebrain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        c.add(item)

    c.shuffle()
    changed = False
    for i in range(100):
        item = c.next()
        if item.visible_side.get() != str(i):
            changed = True
        c.answer_item(sidebrain.ItemFeedback.EASY)

    assert changed

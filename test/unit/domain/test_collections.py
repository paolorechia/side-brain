import pytest
import src.domain as domain


def test_collection_starts_empty():
    c = domain.Collection()
    assert len(c) == 0


def test_collection_set_name():
    c = domain.Collection()
    c.set_name("bah")
    assert c.name == "bah"


def test_collection_set_name_raises_errors():
    c = domain.Collection()

    with pytest.raises(domain.errors.InvalidCollectionName):
        c.set_name("")

    with pytest.raises(domain.errors.InvalidCollectionName):
        c.set_name(None)

    with pytest.raises(domain.errors.InvalidCollectionName):
        c.set_name(123)

    with pytest.raises(domain.errors.InvalidCollectionName):
        c.set_name(["ahoy"])


def test_collection_add_item():
    c = domain.Collection()

    item = domain.Item()
    item.set_text_type("a")
    item.set_answer("b")

    c.add(item)
    assert len(c) == 1


def test_collection_add_item_raises_errors():
    c = domain.Collection()

    with pytest.raises(domain.errors.InvalidItemType):
        c.add("garbage")

    with pytest.raises(domain.errors.InvalidItemType):
        c.add(None)

    with pytest.raises(domain.errors.InvalidItemType):
        c.add(123)


def test_empty_collection_next_returns_none():
    c = domain.Collection()
    item = c.next()
    assert not item


def test_collection_answer_item_errors():
    c = domain.Collection()
    _ = c.next()
    with pytest.raises(domain.errors.InvalidItemFeedback):
        c.answer_item("a")

    with pytest.raises(domain.errors.NoItemToAnswerException):
        c.answer_item(domain.ItemFeedback.HARD)


def test_collection_next():
    c = domain.Collection()

    def create_stub_item(i):
        item = domain.Item()
        item.set_text_type(i)
        item.set_answer(i)
        return item

    for i in range(5):
        c.add(create_stub_item(str(i)))

    for i in range(5):
        item = c.next()
        assert item.check_answer(str(i))
        c.answer_item(domain.ItemFeedback.EASY)

    # Finishes
    assert not c.next()


def test_collection_next_with_medium():
    c = domain.Collection()

    item = domain.Item()
    item.set_text_type("a")
    item.set_answer("a")

    c.add(item)

    _ = c.next()
    c.answer_item(domain.ItemFeedback.MEDIUM)
    c.answer_item(domain.ItemFeedback.MEDIUM)

    # Finishes
    assert not c.next()


def test_collection_next_with_hard():
    c = domain.Collection()

    item = domain.Item()
    item.set_text_type("a")
    item.set_answer("a")

    c.add(item)

    _ = c.next()

    c.answer_item(domain.ItemFeedback.HARD)
    c.answer_item(domain.ItemFeedback.HARD)
    c.answer_item(domain.ItemFeedback.HARD)

    # Finishes
    assert not c.next()


def test_collection_next_with_failed():
    c = domain.Collection()

    def create_stub_item(i):
        item = domain.Item()
        item.set_text_type(i)
        item.set_answer(i)
        return item

    for i in range(5):
        c.add(create_stub_item(str(i)))

    for i in range(6):
        _ = c.next()
        if i == 0:
            c.answer_item(domain.ItemFeedback.FAILED)
        else:
            c.answer_item(domain.ItemFeedback.EASY)

    # Finishes
    assert not c.next()


def test_collection_ignores_items_with_wait_time():
    item = domain.Item()
    item.set_text_type("a")
    item.set_answer("a")

    wait = domain.Item()
    wait.set_text_type("wait")
    wait.set_answer("wait")
    wait.push_feedback(domain.ItemFeedback.EASY)

    c = domain.Collection()
    c.add(item)
    c.add(wait)

    item = c.next()
    assert item.check_answer("a")
    c.answer_item(domain.ItemFeedback.EASY)

    empty = c.next()
    assert not empty


def test_collection_shuffles_change_orders():
    c = domain.Collection()

    for i in range(100):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        c.add(item)

    c.shuffle()
    changed = False
    for i in range(100):
        item = c.next()
        if item.visible_side.get() != str(i):
            changed = True
        c.answer_item(domain.ItemFeedback.EASY)

    assert changed

import src.domain as domain


def test_collection_starts_with_empty_stats():
    c = domain.Collection()

    assert c.get_statistics() == domain.CollectionStatistics(
        total_attempts=0,
        easy_answers=0,
        medium_answers=0,
        hard_answers=0,
        failed_answers=0,
        a_plus_items=0,
        a_items=0,
        b_items=0,
        c_items=0,
        d_items=0,
        e_items=0,
    )


def test_collection_statistics():
    c = domain.Collection()
    expected_collection = domain.CollectionStatistics(
        total_attempts=0,
        easy_answers=0,
        medium_answers=0,
        hard_answers=0,
        failed_answers=0,
        a_plus_items=1,
        a_items=2,
        b_items=3,
        c_items=4,
        d_items=5,
        e_items=5,
    )
    for i in range(expected_collection.a_plus_items):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        item.classification.type_ = domain.ItemClassificationType.APLUS
        c.add(item)
    for i in range(expected_collection.a_items):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        item.classification.type_ = domain.ItemClassificationType.A
        c.add(item)
    for i in range(expected_collection.b_items):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        item.classification.type_ = domain.ItemClassificationType.B
        c.add(item)
    for i in range(expected_collection.c_items):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        item.classification.type_ = domain.ItemClassificationType.C
        c.add(item)
    for i in range(expected_collection.d_items):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        item.classification.type_ = domain.ItemClassificationType.D
        c.add(item)
    for i in range(expected_collection.e_items):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        item.classification.type_ = domain.ItemClassificationType.E
        c.add(item)

    assert c.get_statistics() == expected_collection


def test_collection_statistics_2():
    c = domain.Collection()
    expected_collection = domain.CollectionStatistics(
        total_attempts=7,
        easy_answers=1,
        medium_answers=2,
        hard_answers=3,
        failed_answers=1,
        a_plus_items=0,
        a_items=0,
        b_items=0,
        c_items=0,
        d_items=2,
        e_items=3,
    )

    for i in range(expected_collection.d_items + expected_collection.e_items):
        item = domain.Item()
        item.set_text_type(str(i))
        item.set_answer(str(i))
        c.add(item)

    for i in range(expected_collection.easy_answers):
        c.next()
        c.answer_item(domain.ItemFeedback.EASY)

    for i in range(expected_collection.medium_answers):
        c.next()
        c.answer_item(domain.ItemFeedback.MEDIUM)

    for i in range(expected_collection.hard_answers):
        c.next()
        c.answer_item(domain.ItemFeedback.HARD)

    for i in range(expected_collection.failed_answers):
        c.next()
        c.answer_item(domain.ItemFeedback.FAILED)

    print(c.items)
    assert c.get_statistics() == expected_collection

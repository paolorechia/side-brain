from src.dynaborn import Table, Column, Integer, String, UUID


def test_dynaborn_column():
    pass


def test_dynaborn_table():
    table = Table(
        "test",
        Column("pk", UUID, auto_generate=True),
        Column("abc", String),
        Column("number", Integer),
    )
    assert table

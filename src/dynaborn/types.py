class ColumnType:
    pass


class Integer(ColumnType):
    pass


class String(ColumnType):
    pass


class UUID(ColumnType):
    pass


class Column:
    def __init__(self, property_name: str, column_type: ColumnType, **options):
        self.property_name = property_name
        self.column_type = column_type
        self.options = options

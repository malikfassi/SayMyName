import datetime as dt
from peewee import DataError
from playhouse.postgres_ext import DateTimeTZField


class DateTimeTzField(DateTimeTZField):
    def db_value(self, value):
        if value is not None:
            if value.tzinfo is None:
                raise DataError(f'Cannot use naive datetime "{value}" in DateTimeTzField')
            value = value.astimezone(dt.timezone.utc).replace(tzinfo=None)
        return super(DateTimeTzField, self).db_value(value)

    def python_value(self, value):
        value = super(DateTimeTzField, self).python_value(value)
        if value is not None:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value
import json

import dateutil


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        for k, v in obj.items():
            obj[k] = self._date_value(v) or v
            # We could also automatically transform number strings into Decimal,
            # but this could yield false positive (user name being numbers for example)
        return obj

    def _date_value(self, v):
        if isinstance(v, str):
            try:
                return dateutil.parser.isoparse(v)
            except:
                pass
from typing import Dict

from peewee import Model, Proxy, DoesNotExist

from api.common.Utility import Utility
from api.common.models.DateTimeTZField import DateTimeTzField

database_proxy = Proxy()


class BaseModel(Model):
    created_on = DateTimeTzField(default=Utility.utc_now)
    updated_on = DateTimeTzField(default=Utility.utc_now)

    class Meta:
        database = database_proxy

    DoesNotExistException = None  # will be overidden by subClasses

    def serialize(self, *args, **kwargs) -> Dict:
        return self._serialize(*args, **kwargs)

    def _serialize(self, *args, **kwargs) -> Dict:
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        self.updated_on = Utility.utc_now()
        return super().save(*args, **kwargs)

    @classmethod
    def update(cls, __data=None, **update):
        update['updated_on'] = Utility.utc_now()
        return super().update(**update)

    def update_model(self, **update):
        self.update(**update).where(self._pk_expr()).execute()
        return self.get(self._pk_expr())

    @classmethod
    def get_type_name(cls):
        return Utility.get_type_name(cls.__name__)

    @staticmethod
    def get_models():
        sub_models = {}
        # Traverse the sub classes hierarchy and create a map from class name to model.
        # This could be done with metaclasses as well, but peewee.Model already has a metaclass
        # which makes adding a new one a bit trickier.
        class_list = [BaseModel]
        while class_list:
            sub_class = class_list.pop()
            sub_models[sub_class.__name__] = sub_class
            class_list.extend(sub_class.__subclasses__())
        return sub_models

    @classmethod
    def get(cls, *query, **filters):
        try:
            return super().get(*query, **filters)
        except DoesNotExist as e:
            if cls.DoesNotExistException:
                raise cls.DoesNotExistException(*query, **filters) from e
            else:
                raise

    def refresh(self):
        """
        Get the model object reflecting the most recently updated state.

        For example, instead of doing this:
          group = Group.get_by_id(group.id)

        we could just do:
          group = group.refresh()

        Note: this method is pure, so the original model instance
              remains unchanged.
        """
        return type(self).get(self._pk_expr())

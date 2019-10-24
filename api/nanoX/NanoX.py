from peewee import CharField, ForeignKeyField

from api.common.models.BaseModel import BaseModel
from api.materials.Materials import Material
from api.nanoX.NanoXExceptions import NanoXDoesNotExistException


class NanoX(BaseModel):
    identity = CharField(unique=True, null=True)
    pcb = CharField(unique=True)  # same as identity
    battery = ForeignKeyField(Material, null=True)
    display = ForeignKeyField(Material, null=True)
    back_cover = ForeignKeyField(Material, null=True)
    top_cover = ForeignKeyField(Material, null=True)
    button_metal = ForeignKeyField(Material, null=True)
    swivel = ForeignKeyField(Material, null=True)

    DoesNotExistException = NanoXDoesNotExistException

    def get_materials(self):
        return [self.battery, self.display, self.back_cover, self.top_cover, self.button_metal]

    def serialize(self):
        return {
            'id': self.id,
            'identity': self.identity,
            'battery': self.battery.get_batch_ref(),
            'display': self.display.get_batch_ref(),
            'back_cover': self.back_cover.get_batch_ref(),
            'top_cover': self.top_cover.get_batch_ref(),
            'PCB': self.pcb,
            'button_metal': self.button_metal.get_batch_ref(),
            'swivel': self.swivel,
            'created_on': self.created_on,
            'updated_on': self.updated_on
        }

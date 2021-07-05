import enum

from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class StatusTypes(str, enum.Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    DONE = "done"


class Products(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    status = fields.CharEnumField(enum_type=StatusTypes, default=StatusTypes.DRAFT)
    categories = fields.ManyToManyField(model_name="app.models.categories.Categories", related_name="products")

    def __str__(self):
        return f"Product:{self.id} [{self.title}]"


Product_Pydantic = pydantic_model_creator(Products, name="Product")
ProductIn_Pydantic = pydantic_model_creator(Products, name="ProductIn", exclude_readonly=True)


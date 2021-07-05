from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Categories(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

    def __str__(self):
        return self.name


Category_Pydantic = pydantic_model_creator(Categories, name="Category")
CategoryIn_Pydantic = pydantic_model_creator(Categories, name="CategoryIn", exclude_readonly=True)

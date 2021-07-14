import enum

from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Categories(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

    def __str__(self):
        return self.name


CategoryOutGet = pydantic_model_creator(Categories, name="CategoryOutGet")
CategoryOutPost = pydantic_model_creator(Categories, name="CategoryOutPost", include=("id",))
CategoryIn = pydantic_model_creator(Categories, name="CategoryIn", exclude_readonly=True)


class StatusTypes(str, enum.Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    DONE = "done"


class Products(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    status = fields.CharEnumField(enum_type=StatusTypes, default=StatusTypes.DRAFT)
    categories = fields.ManyToManyField(model_name="models.Categories", related_name="products")

    def __str__(self):
        return f"Product:{self.id} [{self.title}]"


ProductOutGet = pydantic_model_creator(Products, name="ProductOutGet")
ProductOutPost = pydantic_model_creator(Products, name="ProductOutPost", include=("id",))
ProductIn = pydantic_model_creator(Products, name="ProductIn", exclude_readonly=True)


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128)

    class PydanticMeta:
        exclude = ["password_hash"]

    def __str__(self):
        return self.username


UserOutGet = pydantic_model_creator(Users, name="UserOutGet")
UserOutPost = pydantic_model_creator(Users, name="UserOutPost", include=("id",))
UserIn = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

# TODO Figure out how to distribute models to files

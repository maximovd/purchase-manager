from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128)

    class PydanticMeta:
        exclude = ["password_hash"]

    def __str__(self):
        return self.username


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

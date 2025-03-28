from tortoise import fields, models, Tortoise


class MsUser(models.Model):
    microservice = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)
    date_join = fields.DatetimeField(auto_now_add=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    class PydanticMeta:
        exclude = ('comments', 'password')
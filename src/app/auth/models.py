from tortoise import models, fields


class Verification(models.Model):
    link = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.MsUser', related_name='verification')
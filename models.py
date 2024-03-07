from tortoise import fields
from tortoise.models import Model

class ProcessedImage(Model):
    id = fields.IntField(pk=True)
    source_image = fields.TextField()
    target_image = fields.TextField()
    processed_image = fields.TextField()

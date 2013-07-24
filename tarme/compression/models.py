from django.db import models

# Create your models here.
class Document(models.Model):
    doc = models.FileField(upload_to='documents/%Y/%m/%d')
    #compressed_doc = models.FileField(upload_to='documents/%Y/%m/%d')

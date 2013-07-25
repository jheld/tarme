from django.db import models

# Create your models here.
class Document(models.Model):
    doc = models.FileField(upload_to='documents/%Y/%m/%d')
    compressed_doc = models.FileField(upload_to='documents/%Y/%m/%d',null=True,blank=True)
    def get_absolute_url(self):
        return ('document_list',(),{'pk':self.pk})
    def __unicode__(self):
        return self.doc.name

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete,sender=Document)
def document_delete(sender, instance, **kwargs):
    if instance.doc:
        instance.doc.delete(False)
    if instance.compressed_doc:
        instance.compressed_doc.delete(False)

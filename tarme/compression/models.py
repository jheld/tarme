from django.db import models

# Create your models here.

class CompressedDocument(models.Model):
    compressed_doc = models.FileField(upload_to='documents/%Y/%m/%d')
    COMPRESSION_TYPES = (
        ('tar.gz','tar.gz'),
        ('tar.bz2','tar.bz2'),
        ('zip','zip'),
        ('gzip','gzip'),
        )
    compression_type = models.CharField(max_length=10,choices=COMPRESSION_TYPES)
    def __unicode__(self):
        return self.compressed_doc.name

class Document(models.Model):
    doc = models.FileField(upload_to='documents/%Y/%m/%d')

    compressed_docs = models.ManyToManyField(CompressedDocument, verbose_name='list of compressed docs based on upload document.',null=True,blank=True)
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
        
    if instance.compressed_docs:
        for cDoc in CompressedDocument.objects.all():
            if cDoc in instance.compressed_docs.all():
                instance.compressed_docs.remove(cDoc)
                cDoc.delete()


@receiver(pre_delete,sender=CompressedDocument)
def compresseddocument_delete(sender, instance, **kwargs):
    if instance.compressed_doc:
        instance.compressed_doc.delete(False)

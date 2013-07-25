# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    document = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
        )
class CompressForm(forms.Form):
    compression_type = forms.ChoiceField(choices=(('tar.gz','tar.gz'),('tar.bz','tar.bz')),label='compression type',help_text='will create a compressed file')

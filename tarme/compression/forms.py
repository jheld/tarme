# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    document = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
        )

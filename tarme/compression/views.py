# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic.edit import FormView
from django.views.generic import ListView

from compression.models import Document
from compression.forms import DocumentForm

class CompressView(ListView):
    #template_name = 'compress.html'
    model = Document
    '''
    form_class = DocumentForm
    success_url = '/compressed/'
    '''

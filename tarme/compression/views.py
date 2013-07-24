# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from compression.models import Document
from compression.forms import DocumentForm

class SuccessView(TemplateView):
    template_name = 'success.html'
    

class CompressView(FormView):
    template_name = 'compress.html'
    success_url = '/document_list/'
    form_class = DocumentForm
    model = Document
    def form_valid(self, form):
        return super(CompressView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CompressView, self).form_invalid(form)


    def post(self, request, *args, **kwargs):        
        form = DocumentForm(request.POST,request.FILES)
        if self.form_valid(form):
            newDocument = Document(doc = request.FILES['document'])
            newDocument.save()
            return super(CompressView, self).post(request,*args,**kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(CompressView, self).get_context_data(**kwargs)
        return context


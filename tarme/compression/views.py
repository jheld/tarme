# -*- coding: utf-8 -*-
import tarfile
from os import chdir, remove
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File

from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse, lazy

from compression.models import Document
from compression.forms import DocumentForm, CompressForm

from tarme.settings import ROOT_DIR,MEDIA_ROOT

class SuccessView(TemplateView):
    template_name = 'success.html'
    
class CompressView(FormView):
    template_name = 'compress.html'
    model = Document
    form_class = CompressForm
    def get_success_url(self, **kwargs):
        print(self.kwargs['pk'])
        return '/document_list/{pk}'.format(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):        

        form = CompressForm(request.POST)
        if self.form_valid(form):
            document = Document.objects.get(pk=kwargs['pk'])
            print(MEDIA_ROOT+'/'+document.doc.name[0:document.doc.name.rfind('/')+1])
            fullpath = MEDIA_ROOT+'/'+document.doc.name
            tarfilepath = fullpath+'1'+'.tar.gz';
            chdir(MEDIA_ROOT+'/'+document.doc.name[0:document.doc.name.rfind('/')+1])
            tar = tarfile.open(tarfilepath,'w:gz')
            tar.add(fullpath)
            tar.close()
            chdir(ROOT_DIR)
            with open(tarfilepath,'r') as f:
                myfile = File(f)
                
                document.compressed_doc.save(document.doc.name+'.tar.gz',myfile)
                document.save()
                remove(tarfilepath)

            return super(CompressView, self).post(request,*args,**kwargs)

    
    '''
    def get_context_data(self, **kwargs):
        print('context')
        context = super(CompressView, self).get_context_data(**kwargs)
        return context
    '''



class UploadView(FormView):
    template_name = 'upload.html'
    form_class = DocumentForm
    model = Document
    success_url = '/document_list/'
    def form_valid(self, form):
        return super(UploadView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UploadView, self).form_invalid(form)


    def post(self, request, *args, **kwargs):        
        form = DocumentForm(request.POST,request.FILES)
        if self.form_valid(form):
            newDocument = Document(doc = request.FILES['document'])
            newDocument.save()
            return super(UploadView, self).post(request,*args,**kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        return context


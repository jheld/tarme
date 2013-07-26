# -*- coding: utf-8 -*-
import tarfile, zipfile
from os import chdir, remove
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File

from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import ListView
from django.views.generic.base import TemplateView#, BaseDetailView

from django.http import HttpResponse


from compression.models import Document, CompressedDocument
from compression.forms import DocumentForm, CompressForm

from tarme.settings import ROOT_DIR,MEDIA_ROOT

class SuccessView(TemplateView):
    template_name = 'success.html'

'''
class FileResponseMixin(object):
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content-type'] = 'application/'

class DownloadView()
   
'''
 
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
            compression_type = request.POST['compression_type']
            document = Document.objects.get(pk=kwargs['pk'])
            #print(MEDIA_ROOT+'/'+document.doc.name[0:document.doc.name.rfind('/')+1])
            fullpath = MEDIA_ROOT+'/'+document.doc.name
            tarfilepath = fullpath+'1'+'.'+compression_type;
            chdir(MEDIA_ROOT+'/'+document.doc.name[0:document.doc.name.rfind('/')+1])
        
            tarType = 'gz'
            if compression_type == 'tar.gz':
                tarType = 'gz'
            elif compression_type == 'tar.bz2':
                tarType = 'bz2'
            elif compression_type == 'gzip':
                tarType = 'gz'
            elif compression_type == 'zip':
                tarType = ''
                doZip = True
            if tarType:
                tar = tarfile.open(tarfilepath,'w:{tType}'.format(tType=tarType))
                tar.add(fullpath)
                tar.close()

            elif doZip:
                zFile = zipfile.ZipFile(tarfilepath,'w')
                zFile.write(fullpath)
                zFile.close()
                with open(tarfilepath,'r') as f:
                    myfile = File(f)
                    cDoc = CompressedDocument()
                    cDoc.compression_type = compression_type
                    cDoc.compressed_doc.save(document.doc.name+'.'+compression_type,myfile)
                    cDoc.save()
                    document.compressed_docs.add(cDoc)
                    document.save()
                    remove(tarfilepath)

            chdir(ROOT_DIR)

            with open(tarfilepath,'r') as f:
                myfile = File(f)
                cDoc = CompressedDocument()
                cDoc.compression_type = compression_type
                cDoc.compressed_doc.save(document.doc.name+'.'+compression_type,myfile)
                cDoc.save()
                document.compressed_docs.add(cDoc)
                document.save()
                remove(tarfilepath)
            return super(CompressView, self).post(request,*args,**kwargs)

    
    
    def get_context_data(self, **kwargs):
        context = super(CompressView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    



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


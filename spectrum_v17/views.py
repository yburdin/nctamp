import glob
import os

from django.shortcuts import render
from django import forms
from django.db import models
from datetime import datetime
from sendfile import sendfile
import spectrum_v17.prepare_spectrum_new


class SpectrumForm(forms.Form):
    docfile = forms.FileField()


class Document(models.Model):
    docfile = models.FileField(upload_to='./spectrum_v17/')


def index(request):
    r = glob.glob('./tmp/spectrum_v17/*')
    for file in r:
        os.remove(file)

    if request.method == 'POST':
        form = SpectrumForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = Document(docfile=request.FILES['docfile'])
            new_doc.save()

            input_file = glob.glob('./tmp/spectrum_v17/*')[0]

            date_str = str(datetime.now())[:-7].replace(':', '-').replace(' ', '-')
            output_file = './tmp/spectrum_v17/' + date_str + '.zip'

            spectrum_v17.prepare_spectrum_new.prepare(input_file, output_file)

            return sendfile(request, output_file, attachment=True)

    else:
        form = SpectrumForm()

    return render(request, 'spectrum_v17/spectrum_index.html', {'form': form})

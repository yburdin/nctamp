import glob, os

from django.shortcuts import render
from django import forms
from sendfile import sendfile

from datetime import datetime

import spectrum.prepare_spectrum

from spectrum.models import Document

class SpectrumForm(forms.Form):
    docfile = forms.FileField()
    
def index(request):
    
    r = glob.glob('./tmp/spectrum/*')
    for file in r:
        os.remove(file)
                
    if request.method == 'POST':
        form = SpectrumForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            
            input_file = glob.glob('./tmp/spectrum/*')[0]
            
            date_str = str(datetime.now())[:-7].replace(':', '-').replace(' ','-')
            output_file = './tmp/spectrum/' + date_str + '.zip' 
            
            spectrum.prepare_spectrum.prepare_spekters(input_file, output_file)            
                        
            return sendfile(request, output_file, attachment=True)
        
    else:
        form = SpectrumForm()
            
    return render(request, 'spectrum/spectrum_index.html', {'form': form})
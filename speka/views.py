import glob, os

from django.shortcuts import render
from django import forms
from sendfile import sendfile

from datetime import datetime

import speka.calculation_speka


from speka.models import Document

class SpekaForm(forms.Form):
    docfile = forms.FileField()
    
def index(request):
    
    r = glob.glob('./tmp/*')
    for file in r:
        os.remove(file)
                
    if request.method == 'POST':
        form = SpekaForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            
            input_file = glob.glob('./tmp/*')[0]
            
            date_str = str(datetime.now())[:-7].replace(':', '-').replace(' ','-')
            output_file = './tmp/' + date_str + '.xlsx' 
            
            speka.calculation_speka.calculate_spec(input_file, output_file)
                        
            return sendfile(request, output_file, attachment=True)
        
    else:
        form = SpekaForm()
            
    return render(request, 'speka/speka_index.html', {'form': form})

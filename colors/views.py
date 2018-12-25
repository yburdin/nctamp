from django.shortcuts import render
from django import forms

import numpy as np
import colorsys

class MyForm(forms.Form):
    InputNumber = forms.CharField(max_length=50)
	
def count_distance(u, v):
    d = np.array(u) - np.array(v)
    d = sum(d**2)
    
    return np.sqrt(d)	
	
def random_colors(number):
    pixels = []
    n = 0
    step = ((6e4 / number) ** (1/2.1))*0.9
    
    while len(pixels) < number:
        hsvColor = [np.random.randint(10, 90)/100, np.random.randint(30, 50)/100, np.random.randint(70, 90)/100]        
        rgbColor = [int(x*255) for x in colorsys.hsv_to_rgb(hsvColor[0], hsvColor[1], hsvColor[2])]
        
        try:
            dist = [count_distance(rgbColor, x) for x in pixels]
            if min(dist) > step:
                pixels.append(rgbColor)
        except ValueError:
            pixels.append(rgbColor)
            
        n += 1
        if n > 1000: break
 
    return pixels

def prepare_results(pixels):
	result_string = ''
	for color in pixels:
		result_string += '<tr>'
		result_string += '<td bgcolor="#{:02x}{:02x}{:02x}"> {} </td> <td align="center"> {} </td>'.format(color[0],color[1],color[2],' ', color)
		result_string += '</tr>'
		
	return result_string

def index(request):
    if request.method == 'POST': 
        form = MyForm(request.POST)
        
        if form.is_valid():             
            colorsAmount = int(form.cleaned_data['InputNumber'])            
            result = prepare_results(random_colors(colorsAmount))            
            return render(request, 'colors/colors_form.html', {'result':result})
        
    else:
        form = MyForm()
        
    return render(request, 'colors/colors_form.html', {'form': form})
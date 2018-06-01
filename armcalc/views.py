from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import math

# Create your views here.

class H1Form(forms.Form):
    h1_a = forms.CharField(max_length=10)
    h1_b = forms.CharField(max_length=10)
    h1_c = forms.CharField(max_length=10)
    h1_d = forms.CharField(max_length=10)

class D1Form(forms.Form):
    d1_a = forms.CharField(max_length=10)
    d1_b = forms.CharField(max_length=10)
    d1_c = forms.CharField(max_length=10)
    d1_d = forms.CharField(max_length=10)

class P1Form(forms.Form):
    p1_a = forms.CharField(max_length=10)
    p1_b = forms.CharField(max_length=10)
    p1_d = forms.CharField(max_length=10)

class L1Form(forms.Form):
    l1_a = forms.CharField(max_length=10)
    l1_b = forms.CharField(max_length=10)
    l1_c = forms.CharField(max_length=10)
    l1_d = forms.CharField(max_length=10)

class H2Form(forms.Form):
    h2_a = forms.CharField(max_length=10)
    h2_b = forms.CharField(max_length=10)
    h2_d = forms.CharField(max_length=10)

class H3Form(forms.Form):
    h3_a = forms.CharField(max_length=10)
    h3_b = forms.CharField(max_length=10)
    h3_d = forms.CharField(max_length=10)

def index(request):
    return render(request, 'armcalc/index.html')

def get_mass(diameter, length):
    mass = math.pi/4 * diameter**2 * length * 7850 * 1e-9
    return format(mass, '.3g')

def prepare_result(diameter, length, mass):
    result_string = ('<tr>' +
                     '<td>'+str(diameter)+'</td>' +
                     '<td>'+str(length)+'</td>' +
                     '<td>'+str(mass)+'</td>' +
                     '</tr>')
    return result_string

def calculator(request, calc_type):    
    if calc_type == 'h1':
        if request.method == 'POST':
            form = H1Form(request.POST)

            if form.is_valid():
                h1_a = int(form.cleaned_data['h1_a'])
                h1_b = int(form.cleaned_data['h1_b'])
                h1_c = int(form.cleaned_data['h1_c'])
                diameter = int(form.cleaned_data['h1_d'])
                
                length = (h1_a + h1_b + h1_c)*2
                mass = get_mass(diameter,length)
                
                result = prepare_result(diameter, length, mass)                       

                return render(request, 'armcalc/h1.html', {'h1_res':result})
        else:
            return render(request, 'armcalc/h1.html')

    elif calc_type == 'd1':
        if request.method == 'POST':
            form = D1Form(request.POST)

            if form.is_valid():
                d1_a = int(form.cleaned_data['d1_a'])
                d1_b = int(form.cleaned_data['d1_b'])
                d1_c = int(form.cleaned_data['d1_c'])
                diameter = int(form.cleaned_data['d1_d'])
                
                length = d1_a + d1_b + d1_c
                mass = get_mass(diameter,length)
                
                result = prepare_result(diameter, length, mass)                       

                return render(request, 'armcalc/d1.html', {'d1_res':result})
        else:
            return render(request, 'armcalc/d1.html')

    elif calc_type == 'p1':
        if request.method == 'POST':
            form = P1Form(request.POST)

            if form.is_valid():
                p1_a = int(form.cleaned_data['p1_a'])
                p1_b = int(form.cleaned_data['p1_b'])
                diameter = int(form.cleaned_data['p1_d'])
                
                length = p1_a + p1_b + p1_a
                mass = get_mass(diameter,length)
                
                result = prepare_result(diameter, length, mass)                       

                return render(request, 'armcalc/p1.html', {'p1_res':result})
        else:
            return render(request, 'armcalc/p1.html')

    elif calc_type == 'l1':
        if request.method == 'POST':
            form = L1Form(request.POST)

            if form.is_valid():
                l1_a = int(form.cleaned_data['l1_a'])
                l1_b = int(form.cleaned_data['l1_b'])
                l1_c = int(form.cleaned_data['l1_c'])
                diameter = int(form.cleaned_data['l1_d'])
                
                length = l1_b + (l1_a + l1_c)*2
                mass = get_mass(diameter,length)
                
                result = prepare_result(diameter, length, mass)                       

                return render(request, 'armcalc/l1.html', {'l1_res':result})
        else:
            return render(request, 'armcalc/l1.html')

    elif calc_type == 'h2':
        if request.method == 'POST':
            form = H2Form(request.POST)

            if form.is_valid():
                h2_a = int(form.cleaned_data['h2_a'])
                h2_b = int(form.cleaned_data['h2_b'])
                diameter = int(form.cleaned_data['h2_d'])

                len_h2 = math.sqrt(h2_a**2 + (2.5*diameter)**2)
                
                length = int(len_h2) + (h2_b + 2.5*diameter)*2
                mass = get_mass(diameter,length)
                
                result = prepare_result(diameter, length, mass)                       

                return render(request, 'armcalc/h2.html', {'h2_res':result})
        else:
            return render(request, 'armcalc/h2.html')
        
    elif calc_type == 'h3':
        if request.method == 'POST':
            form = H3Form(request.POST)

            if form.is_valid():
                h3_a = int(form.cleaned_data['h3_a'])
                h3_b = int(form.cleaned_data['h3_b'])
                diameter = int(form.cleaned_data['h3_d'])
                
                length = h3_a + (h3_b + 2.5*diameter)*2
                mass = get_mass(diameter,length)
                
                result = prepare_result(diameter, length, mass)                       

                return render(request, 'armcalc/h3.html', {'h3_res':result})
        else:
            return render(request, 'armcalc/h3.html')

        
    else:
        return HttpResponse(calc_type)

    

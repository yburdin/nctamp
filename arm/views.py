from django.shortcuts import render
from django import forms

import math
import pandas as pd


class MyForm(forms.Form):
    InputArea = forms.CharField(max_length=50)
    InputFonDiameter = forms.CharField(max_length=50)
    InputFonSpacing = forms.CharField(max_length=50)

arm_list = [3,4,5,6,7,8,9,10,12,14,16,18,20,22,25,28,32,36,40,45,50,55,60,70,80]

def calc_area (diameter, spacing):
    """
    Расчитывает интенсивность (площадь) армирования.
    Исходные данные в мм, ответ в см.
    """
    area = (math.pi * diameter ** 2 / 4 * 1000 / spacing) / 100
    return area

def get_selection (fon, area):
    """
    Выдает выборку доп.армирования по заданному фону и расчитанной интенсивности
    """
    (diameter, spacing) = fon
    fon_area = calc_area(diameter, spacing)
    
    selection = []
    for arm in range(arm_list.index(diameter),len(arm_list)):
        if ((calc_area(arm_list[arm], spacing) + fon_area) / area > 0.9 and
            (calc_area(arm_list[arm], spacing) + fon_area) / area < 1.2):
            selection.append( (arm_list[arm], spacing) )
            
    for n in range(4):
        calced_area_for_2 = calc_area(arm_list[arm_list.index(diameter) + n] ,
                                              spacing)
        for arm in range(arm_list.index(diameter),len(arm_list)):
            if ((calc_area(arm_list[arm], spacing) +
                 calced_area_for_2 + fon_area) / area > 0.9 and
                (calc_area(arm_list[arm], spacing) + 
                 calced_area_for_2 + fon_area)  / area < 1.2):
                selection.append( ([arm_list[arm_list.index(diameter) + n], arm_list[arm]], spacing) )    
    return selection

def get_arm (fon,area):
    """Выдает отсортированную pandas таблицу с отформатированными данными"""
    arm_pd = pd.DataFrame(columns = ("Diameter", "Spacing", "Area", "Reinforce"))
    
    row = 1
    for item in get_selection(fon,area):
        (diam_fon, spacing_fon) = fon
        (diameter, spacing) = item
        
        if type(diameter) == int:
            calced_area = calc_area(diam_fon,spacing_fon) + calc_area(diameter,spacing)
            reinforce = calced_area / area
            arm_pd.loc[row] = (diameter, spacing, format(calced_area,'.2f'), format(reinforce, '.2f'))
        else:
            r = 0
            diam_str = ""
            for diam in diameter:
                r += calc_area(diam,spacing)
                diam_str += str(diam) + " + "
            calced_area = calc_area(diam_fon,spacing_fon) + r
            reinforce = calced_area / area        
            arm_pd.loc[row] = (diam_str[0:-3], format(spacing,'.0f'), format(calced_area,'.2f'), format(reinforce, '.2f'))
        
        row +=1     
    return arm_pd.sort_values("Reinforce")

def prepare_results(result_table):
    result_string = ""
    results_array = result_table.values
    for item in results_array:
        result_string += '<tr>'
        for cell in item:
            result_string += '<td>'+str(cell)+'</td>'
        result_string += '</tr>'
    return result_string

def index(request):
    if request.method == 'POST': 
        form = MyForm(request.POST)
        
        if form.is_valid():             
            area = float(form.cleaned_data['InputArea'].replace(',','.'))
            fon_diam = int(form.cleaned_data['InputFonDiameter'])
            fon_spacing = int(form.cleaned_data['InputFonSpacing'])
            
            result = prepare_results(get_arm( (fon_diam,fon_spacing), area))
            
            return render(request, 'arm/arm_form.html', {'result':result})
        
    else:
        form = MyForm()
        
    return render(request, 'arm/arm_form.html', {'form': form})
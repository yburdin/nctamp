import pandas as pd
import numpy as np
import math

def item_mass (diameter, length):
    mass = math.pi/4 * diameter ** 2 * length * 7850 * 1e-9
    return mass

def process_file(file):
    xls = pd.ExcelFile(file)
    table = xls.parse().values
    
    #Разделение стрингов в столбце с диаметрами
    for item in table:
        if type(item[4]) == str:
            item[4] = item[4].split('+')
    
    #Замена стрингов в столюце с диаметрами на числа     
    for item in table:
        if type(item[4]) == list:
            for n in range(len(item[4])):
                item[4][n] = int(item[4][n])
    
    #Доавбление столбца с количеством арматуры
    temp = []        
    for n in range(len(table)):
        if math.isnan(table[n][3]):
            temp.append(0)
        else:
            temp.append(math.ceil(table[n][3]/200)+1)
    table = np.append(table, np.array(temp).reshape(len(temp),1), axis=1)                     
    
    #Выбор уникальных длин для стержней и деталей, и диаметров
    bars = []; details = []; diametrs = []
    for item in table:
        if item[2] == 'с':
            if item[1] not in bars: bars.append(item[1]) 
        elif item[2] == 'д' or item[2] == 'дд':
            if item[1] not in details: details.append(item[1]) 
        else: pass
    
    for item in table:
        if type(item[4]) == list:
            for diam in item[4]:
                if diam not in diametrs: diametrs.append(diam)
        elif type(item[4]) == int:
            if item[4] not in diametrs: diametrs.append(item[4])
        else: pass
    
    bars.sort(); details.sort(); diametrs.sort(reverse=True)
    
    return (table, bars, details, diametrs)
    

def get_spec (table,bars,details,diametrs):
    spec = pd.DataFrame(columns = ("Поз","Обозначение","Наименование", "Количество", "Тип", "Масса ед.", "Масса общ."))
    spec_mapping = []
    mark = "ГОСТ Р 52544-2006"
    row = 1
    for diam in diametrs:
        for leng in bars:
            count = 0
            for item in table:
                if type(item[4]) == int and item[1] == leng and item[2] == 'с' and item[4] == diam:
                    count += item[5]
                elif type(item[4]) == list and item[1] == leng and item[2] == 'с' and diam in item[4]:
                    count += item[5]
            if count > 0 :
                mass_item = item_mass(diam,leng)
                name = u'\ue712' + str(diam) + ' A500C l=' + str(int(leng)) 
                spec.loc[row] = (row,mark, name, count, 'с', 
                        str(format(mass_item,'.2f')).replace('.',','), 
                        str(format(mass_item*count,'.2f')).replace('.',','))
                spec_mapping.append([row,diam,leng,'с'])
                row += 1
    
    for diam in diametrs:
        for leng in details:
            count = 0
            for item in table:
                if type(item[4]) == int and item[1] == leng and item[2] == 'д' and item[4] == diam:
                    count += item[5]
                elif type(item[4]) == list and item[1] == leng and item[2] == 'д' and diam in item[4]:
                    count += item[5]
            if count > 0 :
                mass_item = item_mass(diam,leng)
                name = u'\ue712' + str(diam) + ' A500C l=' + str(int(leng)) 
                spec.loc[row] = (row,mark, name, count, 'д', 
                        str(format(mass_item,'.2f')).replace('.',','), 
                        str(format(mass_item*count,'.2f')).replace('.',','))
                spec_mapping.append([row,diam,leng,'д'])
                row += 1  
                
    for diam in diametrs:
        for leng in details:
            count = 0
            for item in table:
                if type(item[4]) == int and item[1] == leng and item[2] == 'дд' and item[4] == diam:
                    count += item[5]
                elif type(item[4]) == list and item[1] == leng and item[2] == 'дд' and diam in item[4]:
                    count += item[5]
            if count > 0 :
                mass_item = item_mass(diam,leng)
                name = u'\ue712' + str(diam) + ' A500C l=' + str(int(leng)) 
                spec.loc[row] = (row,mark, name, count, 'дд', 
                        str(format(mass_item,'.2f')).replace('.',','), 
                        str(format(mass_item*count,'.2f')).replace('.',','))
                spec_mapping.append([row,diam,leng,'дд'])
                row += 1   
                
    return (spec, spec_mapping)

def get_vedomost(table,diametrs):
    cols = []
    mass_ved = []
    for diam in sorted(diametrs):
        cols.append(u'\ue712' + str(diam))
        leng = 0
        for item in table:
            if type(item[4]) == int and item[4] == diam:
                leng += item[1]*item[5]
            elif type(item[4]) == list and diam in item[4]:
                leng += item[1]*item[5]
            else: pass
        mass_ved.append(math.ceil(item_mass(diam,leng)))     
        
    vedomost = pd.DataFrame(columns = cols)
    vedomost.loc[0] = mass_ved
    
    return vedomost

def get_mapping(table,spec_mapping):
    mapping = pd.DataFrame(columns = ("Участок", "Позиция"))
    for item in table:
        if type(item[4]) == int:
            for pos in spec_mapping:
                if item[4] == pos[1] and item[1] == pos[2] and item[2] == pos[3]:
                    mapping.loc[int(item[0])] = (int(item[0]), pos[0])
        if type(item[4]) == list:
            pos_list = ""
            for diam in item[4]:
                for pos in spec_mapping:
                    if diam == pos[1] and item[1] == pos[2] and item[2] == pos[3]:
                        pos_list += str(pos[0]) + " + "               
            
            mapping.loc[int(item[0])] = (int(item[0]), pos_list[:-3])
    return mapping

def calculate_spec (input_file, output_file):           
    (table, bars, details, diametrs) = process_file(input_file)
    (spec, spec_mapping) = get_spec(table,bars,details,diametrs)
    vedomost = get_vedomost(table,diametrs)
    mapping = get_mapping(table,spec_mapping)    
            
    writer = pd.ExcelWriter(output_file)
    spec.to_excel(writer,"Спецификация",index=False)
    vedomost.to_excel(writer, 'Ведомость расхода',index=False)
    mapping.to_excel(writer,'Таблица соответствий',index=False)
    writer.save()

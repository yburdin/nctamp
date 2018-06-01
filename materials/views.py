from django.shortcuts import render
from django import forms

# Create your views here.

OPTIONS = '<option>03Х16Н9М2</option><option>03Х21Н32М3Б</option><option>05Х12Н2М</option><option>06Х12Н3Д</option><option>06Х12Н3ДЛ</option><option>06Х13Н7Д2</option><option>07Х16Н4Б</option><option>08Х13</option><option>08Х14МФ</option><option>08Х16Н11М3</option><option>08Х18Н10Т</option><option>08Х18Н12Т</option><option>09Г2С</option><option>09Х16Н15М3Б</option><option>09Х17Н</option><option>09Х18Н9</option><option>0Х20Н46Б</option><option>10</option><option>10ГН2МФА</option><option>10ГН2МФАЛ</option><option>10Х11Н20Т3Р</option><option>10Х17Н13М2Т</option><option>10Х18Н12М3Л</option><option>10Х18Н9</option><option>10Х2М</option><option>10Х2М1ФБ</option><option>10ХН1М</option><option>10ХСНД</option><option>12Х18Н10Т</option><option>12Х18Н12М3ТЛ</option><option>12Х18Н12Т</option><option>12Х18Н9</option><option>12Х18Н9Т</option><option>12Х18Н9ТЛ</option><option>12Х1МФ</option><option>12Х2М</option><option>12Х2МФА</option><option>12ХМ</option><option>12МХ</option><option>14Х17Н2</option><option>15</option><option>15ГС</option><option>15Х1М1Ф</option><option>15Х1М1ФЛ</option><option>15Х2МФА</option><option>15Х2НМФА</option><option>15Х3НМФА</option><option>15ХМ</option><option>15Л</option><option>16ГНМА</option><option>16ГС</option><option>18Х12ВМБФР</option><option>18Х2МФА</option><option>1Х12В2МФ</option><option>1Х16Н36МБТЮР</option><option>20</option><option>20ГСЛ</option><option>20Х</option><option>20Х12ВНМФ</option><option>20Х13</option><option>20Х1М1Ф1БР</option><option>20ХМ</option><option>20ХМА</option><option>20ХМФЛ</option><option>20ХМЛ</option><option>20К</option><option>20Л</option><option>22К</option><option>25</option><option>25Х1МФ</option><option>25Х2М1Ф</option><option>25Х2МФА</option><option>25Х3МФА</option><option>25Л</option><option>30</option><option>30Х</option><option>30Х13</option><option>30ХГСА</option><option>30ХМА</option><option>31Х19Н9МВБТ</option><option>35</option><option>35Х</option><option>35ХМ</option><option>35ХМА</option><option>36Х2Н2МФА</option><option>38ХН3МФА</option><option>40</option><option>40Х</option><option>45</option><option>45Х</option><option>45Х14Н14В2М</option><option>Х18Н22В2Т2</option><option>ХН35ВТ</option><option>ХН35ВТЮ</option><option>Ст3сп5</option>'

ALPHA_GROUPS = {1: ['Ст3сп5', '10', '15', '15Л', '20', '20Л', '20К', '22К',
                    '25', '25Л', '30', '35', '40', '45', '20Х', '30Х', '35Х',
                    '40Х', '45Х', '12ХМ', '15ХМ', '20ХМ', '20ХМА', '20ХМЛ',
                    '20ХМФЛ', '30ХМ', '30ХМА', '35ХМ', '35ХМА', '10Х2М',
                    '12Х2М', '12МХ', '30ХГСА', '12Х1МФ', '25Х1МФ', '15Х1М1Ф',
                    '15Х1М1ФЛ', '12Х2МФА', '12Х2МФА-А', '15Х2МФА', '15Х2МФА-А',
                    '18Х2МФА', '25Х2МФА', '25Х2М1Ф', '25Х3МФА', '10Х2М1ФБ',
                    '20Х1М1Ф1БР', '38ХН3МФА', '15Х2НМФА', '15Х2НМФА-А',
                    '36Х2Н2МФА', '15Х3НМФА', '15Х3НМФА-А', '10ХСНД',
                    '10ХН1М', '15ГС', '16ГС', '20ГСЛ', '09Г2С', '16ГНМА',
                    '10ГН2МФА', '10ГН2МФАЛ'],
                2: ['08Х13', '20Х13', '30Х13', '09Х17Н', '1Х12В2МФ', '14Х17Н2',
                    '20Х12ВНМФ', '18Х12ВМБФР', '05Х12Н2М-ВИ', '05Х12Н2М',
                    '05Х12Н2М-ВД', '06Х12Н3Д', '06Х12Н3ДЛ', '08Х14МФ',
                    '06Х13Н7Д2', '07Х16Н4Б'],
                3: ['09Х18Н9', '10Х18Н9', '12Х18Н9', '08Х18Н10Т', '12Х18Н9Т',
                    '12Х18Н10Т', '08Х18Н12Т', '12Х18Н12Т', '12Х18Н9ТЛ',
                    '03Х16Н9М2', '08Х16Н11М3', '10Х17Н13М2Т', '10Х18Н12М3Л',
                    '12Х18Н12М3ТЛ', '09Х16Н15М3Б', '45Х14Н14В2М', 'Х18Н22В2Т2',
                    '31Х19Н9МВБТ', '10Х11Н20Т3Р', '1Х16Н36МБТЮР', 'ХН35ВТЮ',
                    'ХН35ВТ-ВД', 'ХН35ВТ', '03Х21Н32М3Б', '0Х20Н46Б']}

YOUNG_GROUPS = {1: ['Ст3сп5', '10', '15', '15Л', '20', '20Л', '20К', '22К',
                    '25', '25Л'],
                2: ['30', '35', '40', '45'],
                3: ['20Х', '12ХМ', '15ХМ', '20ХМ', '20ХМА', '20ХМЛ', '20ХМФЛ',
                    '10Х2М', '12Х2М', '12МХ', '12Х1МФ', '10Х2М1ФБ', '15Х1М1Ф',
                    '15Х1М1ФЛ', '12Х2МФА', '12Х2МФА-А', '15Х2МФА', '15Х2МФА-А',
                    '18Х2МФА', '15Х2НМФА', '15Х2НМФА-А', '15Х3НМФА', '15Х3НМФА-А',
                    '10ХСНД', '10ХН1М', '15ГС', '16ГС', '20ГСЛ', '09Г2С', '16ГНМА',
                    '10ГН2МФА', '10ГН2МФАЛ', '06Х12Н3Д', '06Х12Н3ДЛ', '20Х1М1Ф1БР'],
                4: ['30Х', '35Х', '40Х', '45Х', '30ХМ', '30ХМА', '35ХМ', '35ХМА',
                    '30ХГСА', '25Х1МФ', '25Х2МФА', '25Х2М1Ф', '25Х3МФА', '36Х2Н2МФА',
                    '38ХН3МФА', '07Х16Н4Б'],
                5: ['08Х13', '20Х13', '30Х13', '14Х17Н2', '18Х12ВМБФР',
                    '08Х14МФ', '20Х12ВНМФ','09Х17Н', '1Х12В2МФ', '05Х12Н2М-ВИ',
                    '05Х12Н2М', '05Х12Н2М-ВД'],
                6: ['09Х18Н9', '10Х18Н9', '12Х18Н9', '08Х18Н10Т', '08Х18Н12Т',
                    '12Х18Н9Т', '12Х18Н10Т', '12Х18Н12Т', '12Х18Н9ТЛ',
                    '03Х16Н9М2', '08Х16Н11М3', '09Х16Н15М3Б', '06Х13Н7Д2',
                    '10Х18Н12М3Л', '12Х18Н12М3ТЛ', '10Х17Н13М2Т', '31Х19Н9МВБТ',
                    '45Х14Н14В2М', '0Х20Н46Б', 'Х18Н22В2Т2', '1Х16Н36МБТЮР',
                    'ХН35ВТ', 'ХН35ВТ-ВД', 'ХН35ВТЮ', '03Х21Н32М3Б'],
                7: ['10Х11Н20Т3Р']}

class MatForm(forms.Form):
    marka = forms.CharField(max_length=50)    
    
def westernize_mark(text):
    rus = 'абвгдежзиклмнопрстуфхцчшэюя'
    eng = 'abvgdejziklmnoprstyfhcqw_ux'
    result = ''
    
    for symb in text:
        if symb in rus:
            result += eng[rus.index(symb)]
        else:
            result += symb
            
    return result

def rusify_mark(text):
    rus = 'абвгдежзиклмнопрстуфхцчшэюя'
    eng = 'abvgdejziklmnoprstyfhcqw_ux'
    result = ''
    
    for symb in text:
        if symb in eng:
            result += rus[eng.index(symb)].capitalize()

        else:
            result += symb
            
    return result

def get_group(target_mark, groups):
    for group in groups.keys():
        if target_mark in groups[group]:
            result = group
    
    return result

def index(request):
    if request.method == 'POST':
        form = MatForm(request.POST)
        
        if form.is_valid():
            marka = form.cleaned_data['marka']
            
            img_src = '/static/materials/mats_pictures_png/' + westernize_mark(str(marka).lower()) + '.png'
            img_out = '<img src="' + img_src + '">'
            
            alpha_img_src = '/static/materials/mats_alf_pics/Alf_{0}.png'.format(get_group(marka, ALPHA_GROUPS))
            alpha_img_out = '<img src="' + alpha_img_src + '">'
            
            young_img_src = '/static/materials/young_pictures_png/E_{0}.png'.format(get_group(marka, YOUNG_GROUPS))
            young_img_out = '<img src="' + young_img_src + '">'
            
            return render(request, 'materials/index.html',
                          {'options':OPTIONS,
                           'steel_img':img_out,
                           'alph_img':alpha_img_out,
                           'young_img':young_img_out})
        
    
    return render(request, 'materials/index.html', {'options':OPTIONS})
    

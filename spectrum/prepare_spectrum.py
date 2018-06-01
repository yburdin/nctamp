import pandas as pd
import zipfile
import os

def prepare_spekters(file, output_file):
    spektr = []
    spektr_list = []
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names

    n = 0
    while True:
        try:
            spektr.append(xls.parse(n))
            n += 1
        except IndexError:
            break

    for spkt in spektr:
        if len(spkt.columns.values) == 2:
            spkt.iloc[:,0] = 1/spkt.iloc[:,0]
            answ = spkt.sort_values(spkt.dtypes.index[0], ascending=True)
            spektr_list.append(answ.values.tolist())
        else:
            raise Exception

    file_num = 0
    z = zipfile.ZipFile(output_file, 'w')    
    for item in spektr_list:
        n = 0
        file_name = sheet_names[file_num] + ".prn"
        spectr_file = open(file_name, "w")
        for n in range(len(item)-1):
            string = str(item[n][0]).replace(",",".") + "  " + str(item[n][1]).replace(",",".") + '\r\n'
            spectr_file.write(string)
        n = len(item) - 1
        last_string = str(item[n][0]).replace(",",".") + "  " + str(item[n][1]).replace(",",".") + '\r\n'
        spectr_file.write(last_string)
        spectr_file.close()
        z.write(file_name)
        os.remove(file_name)
        file_num += 1
    z.close()


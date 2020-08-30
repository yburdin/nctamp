import pandas as pd
import numpy as np
import zipfile
import os
import matplotlib.pyplot as plt
from time import sleep
import matplotlib
matplotlib.use('Agg')


def prepare(file, output_file):
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names

    z = zipfile.ZipFile(output_file, 'w')

    error_file = 'errors.txt'

    for sheet in sheet_names:
        sheet_data = xls.parse(sheet_name=sheet, header=None)

        if sheet_data.shape != (0, 0):
            while len(sheet_data.iloc[:, 0].dropna()) == 0:
                sheet_data = sheet_data.drop(axis='columns', labels=sheet_data.iloc[:, 0].name)

            while len(sheet_data.iloc[0, :].dropna()) == 0:
                sheet_data = sheet_data.drop(axis='index', labels=sheet_data.iloc[0, :].name)

            result_spectrum = []
            for i in range(len(sheet_data)):
                spectrum_line = []
                if str(sheet_data.iloc[i, 0]).replace('.', '').replace(',', '').isdigit():
                    spectrum_line.append(float(str(sheet_data.iloc[i, 0]).replace(',', '.')))
                if str(sheet_data.iloc[i, 1]).replace('.', '').replace(',', '').isdigit():
                    spectrum_line.append(float(str(sheet_data.iloc[i, 1]).replace(',', '.')))

                if len(spectrum_line) == 2:
                    result_spectrum.append(spectrum_line)

            if len(result_spectrum) > 1:
                result_spectrum = np.array(result_spectrum)

                file_name = '{}.prn'.format(sheet)
                with open(file_name, 'w') as spectrum_file:
                    for i in range(len(result_spectrum)):
                        string = '{}  {}\r\n'.format(result_spectrum[i][0], result_spectrum[i][1])
                        spectrum_file.write(string)

                z.write(file_name)

                fig_name = '{}.png'.format(sheet)
                fig = plt.figure(figsize=[12, 4], dpi=150)
                plt.plot(result_spectrum[:, 0], result_spectrum[:, 1])
                plt.grid(True)
                plt.xlabel('Частота, Гц')
                plt.ylabel('Амплитуда')

                if result_spectrum[-1, 1] == result_spectrum[-2, 1]:
                    plt.xlim(0, int(result_spectrum[-2, 0] * 1.15))

                plt.savefig(fig_name)
                plt.close(fig)
                z.write(fig_name)

                sleep(1)
                os.remove(file_name)
                os.remove(fig_name)

            else:
                with open(error_file, 'a') as errors:
                    errors.write('{} - лист без спектра\r\n'.format(sheet))

        else:
            with open(error_file, 'a') as errors:
                errors.write('{} - пустой лист\r\n'.format(sheet))

    z.write(error_file)
    os.remove(error_file)

    z.close()


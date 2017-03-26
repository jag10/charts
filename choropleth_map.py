# -*- coding: utf-8 -*-
# python 2.7, python3.5. libraries: sudo pip(3) install geopandas, pysal
import csv
import numpy as np

import geopandas as gpd
import matplotlib.pyplot as plt

def preproc (nameCSV):
    with open(nameCSV, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 0
        provincias = {}
        data = {}
        # collect all data for every city
        for row in reader:
            if i != 0:
                try:
                    provincias[int(row[0])] = provincias[int(row[0])] + get_filtered_row(row)
                except KeyError:
                    provincias[int(row[0])] = get_filtered_row(row)
            i = i + 1
    # build a dict with equiv codes for shapefile and INE data
    with open('data/shapes/adm_spain/ESP_adm2.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        equiv = {}
        j = 0
        for row in reader:
            if j != 0:
                equiv[prepoc_number(row[0]) - 1] = prepoc_number(row[10])
            j = j + 1
    # build a dict with mean data collected for every city
    for i in range(0,56):
        try:
            data[i] = np.mean(provincias[equiv[i]])
        except KeyError:
            data[i] = 0
    return data

def prepoc_number(number):
    if number == '':
        return 0
    else:
        return float(number)

# gets data from d01 to d31 for the specified row
def get_filtered_row(row):
    filtered_row= []
    for i in range(7, 38):
        filtered_row.append(prepoc_number(row[i]))
    return filtered_row


# MAIN
# PREPROCESS DATA

As_file = 'data/diarios_tcm7-432622/As_DD_2015.csv'
BaP_file = 'data/diarios_tcm7-432622/BaP_DD_2015.csv'
Cd_file = 'data/diarios_tcm7-432622/Cd_DD_2015.csv'
Ni_file = 'data/diarios_tcm7-432622/Ni_DD_2015.csv'
Pb_file = 'data/diarios_tcm7-432622/Pb_DD_2015.csv'
pm10_file = 'data/diarios_tcm7-432622/PM10_DD_2015.csv'
pm25_file = 'data/diarios_tcm7-432622/PM25_DD_2015.csv'

#choose map and data
spain = gpd.read_file('data/shapes/adm_spain/ESP_adm2.shp')
spain['Ni'] = preproc(Ni_file).values()

# draw subplots
f, ax = plt.subplots(1, figsize=(9, 9))
ax.set_axis_off()

# draw maps
spain.plot(column='Ni', scheme='Quantiles', ax=ax, legend=True)
ax.set_title(u'Concentración de óxidos de nitrógeno en España en 2015')

plt.show()

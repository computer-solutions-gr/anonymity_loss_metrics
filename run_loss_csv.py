
import pymongo 
import copy
import os
from pathlib import Path
import json

from analyze_data import analyze_table

import settings.csvdata_settings as SETTINGS

#########################################################
# GET/SET PARAMETERS

QI = getattr(SETTINGS, "QI")
QI_SET = [key for key,val in QI.items() if val>0] 

if len(QI_SET) == 0:
    raise Exception  

CATEGORICAL = getattr(SETTINGS, "CATEGORICAL")
K = getattr(SETTINGS, "K")

########################################################
# SET FILENAMES

in_dir = "/home/arianna/CSL/ml_anon/data/Results_QI=AGE,SEX,CURADM_DAYS/"
in_file = f"{in_dir}data_k={K}.csv"

result_dir = f"{in_dir}metrics/"
Path(result_dir).mkdir(parents=True, exist_ok=True)

result_file = f"{result_dir}metrics_k={K}.txt"

#########################################################
# GET INPUT DATA from csv

f = open( in_file, "r")      
# lines = [ line.strip("\n").split(",")[1:] for line in f ]
lines = [ line.strip("\n").split(",") for line in f ]

fields_indexes = { c: i for i,c in enumerate(lines[0]) }
indexes_fields = { val:key for key,val in fields_indexes.items() }

columns = sorted( fields_indexes.items(), key=lambda x: x[1])
columns = list(map( lambda a:a[0], columns ))

data_in = lines[1:]
    

#########################################################
# CONVERT INPUT DATA to list of dicts

data = []
for line in data_in:
    d = {indexes_fields[i]:l for (i,l) in enumerate(line) }
    data.append(d)

#########################################################

(EQ_classes, total_stats, EQ_stats, metrics) = analyze_table(data, QI_SET, CATEGORICAL, K)

#########################################################
# SAVE RESULTS TO CSV

with open(result_file, 'w') as outfile:
    json.dump(metrics, outfile)

print(f"Finished!")

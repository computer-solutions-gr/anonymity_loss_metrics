
import pymongo 
import copy
import os
from pathlib import Path
import json
from db import MongoRepository

from analyze_data import analyze_table

import settings.etl_settings as SETTINGS

########################################################
# MongoDB parameters

host = "localhost"
port = 27017
db_name = "etl_test"
# db_name = "ETL_CS_CARE3_K5"
mongo_repo = MongoRepository( host, port, db_name )   

########################################################
# SET FILENAMES

result_dir = f"{ os.path.realpath(os.getcwd()) }/Results/ETL/"
Path(result_dir).mkdir(parents=True, exist_ok=True)
result_file = f"{result_dir}{db_name}_metrics.csv"

########################################################

data_all = {}
total_stats_all = {}
EQ_classes_all = {}
EQ_stats_all = {}
metrics_all = {}

ontologies = [ "Patient" ]

########################################################

for ontology in ontologies:

    ########################################################
    # GET/SET PARAMETERS

    ONTOLOGY_SETTINGS = getattr(SETTINGS, ontology) 
    QI_SET = [key for key,val in ONTOLOGY_SETTINGS["QI"].items() if val>0] 

    if len(QI_SET) == 0:
        continue   

    CATEGORICAL = ONTOLOGY_SETTINGS["CATEGORICAL"]  
    K = ONTOLOGY_SETTINGS["k"]  

    #########################################################
    # GET INPUT DATA from repository

    data_in = mongo_repo.get( ontology ) # keyword args
    data_in = [d for d in data_in]
    data = copy.deepcopy(data_in)
    
    #########################################################
    (EQ_classes, total_stats, EQ_stats, metrics) = analyze_table(data, QI_SET, CATEGORICAL, K)

    #########################################################
    data_all[ontology] = data
    EQ_classes_all[ontology] = EQ_classes
    metrics_all[ontology] = metrics
    total_stats_all[ontology] = total_stats
    EQ_stats_all[ontology] = EQ_stats

#########################################################
# SAVE RESULTS TO CSV

with open(result_file, 'w') as outfile:
    json.dump(metrics_all, outfile)

print(f"Finished!")

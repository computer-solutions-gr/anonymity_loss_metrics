#1 DIMENSION: ONTOLOGY

import pymongo 
import copy
import os
from pathlib import Path
import json
from db import MongoRepository

from analyze_data import analyze_table

import settings.etl_settings as ETL_SETTINGS
import settings.db_settings as DB_SETTINGS

########################################################
# DB Parameters
db_conn = DB_SETTINGS.db_conn_1
# host = "localhost"
# port = 27017
# schema = "ETL_FHIR_CS_CARE3_K20" 
# mongo_repo = MongoRepository( host, port, schema )   

########################################################
# SET FILENAMES

result_dir = f"{ os.path.realpath(os.getcwd()) }/Results/ETL/"
Path(result_dir).mkdir(parents=True, exist_ok=True)

result_file = f"{result_dir}{db_conn['SCHEMA']}_metrics.txt"

########################################################
# INITIALIZATION

data_all = {}
total_stats_all = {}
EQ_classes_all = {}
EQ_stats_all = {}
metrics_all = {}

ontologies = [ "Patient" ]

################################################################
# GET DATA FOR EVERY ONTOLOGY FROM REPOSITORY
# DATA_ALL[ONTOLOGY]

mongo_repo = MongoRepository( db_conn["HOST"], db_conn["PORT"], db_conn["SCHEMA"] )
 
for ontology in ontologies:        
    data_in = mongo_repo.get( ontology ) # keyword args
    data_in = [d for d in data_in] 
    data_all[ontology] = copy.deepcopy(data_in)
    print(f"len(data_all[{ontology}])={len(data_all[ontology])}")

############################################################

for ontology in ontologies:

    ########################################################
    # GET ONTOLOGY PARAMETERS

    ONTOLOGY_SETTINGS = getattr(ETL_SETTINGS, ontology) 
    QI_SET = [key for key,val in ONTOLOGY_SETTINGS["QI"].items() if val>0] 

    if len(QI_SET) == 0:
        continue   

    CATEGORICAL = ONTOLOGY_SETTINGS["CATEGORICAL"]  
    K = ONTOLOGY_SETTINGS["k"]  

    # #########################################################
    # # GET INPUT DATA from repository
    # data_in = mongo_repo.get( ontology ) # keyword args
    # data_in = [d for d in data_in]
    # data = copy.deepcopy(data_in)

     #########################################################
    # GET ONTOLOGY DATA 
    data = data_all[ontology]
    
    #########################################################
    (EQ_classes, total_stats, EQ_stats, metrics) = analyze_table(data, QI_SET, CATEGORICAL, K)

    #########################################################
   
    EQ_classes_all[ontology] = EQ_classes
    metrics_all[ontology] = metrics
    total_stats_all[ontology] = total_stats
    EQ_stats_all[ontology] = EQ_stats

#########################################################
# SAVE RESULTS TO CSV

with open(result_file, 'w') as outfile:
    json.dump(metrics_all, outfile)

print(f"Finished!")

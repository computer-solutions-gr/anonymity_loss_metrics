#2 DIMENSIONS: ONTOLOGY, SCHEMA

import pymongo 
import copy
import os
from pathlib import Path
import json
from db import MongoRepository

# from analyze_data import analyze_table
from dataset import Dataset

import settings.etl_settings as ETL_SETTINGS
import settings.db_settings as DB_SETTINGS

########################################################
# DB Parameters
db_conns = DB_SETTINGS.DB_CONNECTIONS

########################################################
# SET FILENAMES

result_dir = f"{ os.path.realpath(os.getcwd()) }/Results/ETL_2020_5/"
Path(result_dir).mkdir(parents=True, exist_ok=True)

schemata = [ db_conn["SCHEMA"] for db_conn in db_conns]
schemata = "_".join(schemata)
result_file = f"{result_dir}{schemata}_metrics_2020_5.txt"

########################################################
# INITIALIZATION

data_all = {}
metrics_all = {}
# total_stats_all = {}
# EQ_classes_all = {}
# EQ_stats_all = {}

ONTOLOGIES = [ "Patient" ]

for ontology in ONTOLOGIES:
    data_all[ontology]={}
    for db_conn_i, db_conn in enumerate(db_conns):    
        data_all[ontology][db_conn_i] = []

################################################################
# GET DATA FOR EVERY ONTOLOGY & CONNECTION FROM REPOSITORY
# DATA_ALL[ONTOLOGY][DB SCHEMA]

for (db_conn_i,db_conn) in enumerate(db_conns):
    mongo_repo = MongoRepository( db_conn["HOST"], db_conn["PORT"], db_conn["SCHEMA"] )   

    for ontology in ONTOLOGIES:        
        data_in = mongo_repo.get( ontology ) # keyword args
        data_in = [d for d in data_in] 
        data_all[ontology][db_conn_i] = copy.deepcopy(data_in)
        print(f"len(data_all[{ontology}][{db_conn_i}])={len(data_all[ontology][db_conn_i])}")

################################################################
for ontology in ONTOLOGIES:

    ########################################################
    # GET ONTOLOGY PARAMETERS

    ONTOLOGY_SETTINGS = getattr(ETL_SETTINGS, ontology) 
    QI_SET = [key for key,val in ONTOLOGY_SETTINGS["QI"].items() if val>0] 

    if len(QI_SET) == 0:
        continue   

    CATEGORICAL = ONTOLOGY_SETTINGS["CATEGORICAL"]  
    K = ONTOLOGY_SETTINGS["k"]  ####

    #########################################################
    # GET ONTOLOGY DATA FOR ALL CONNECTIONS
    data = []
    for db_conn_i in data_all[ontology]:
        data.extend( data_all[ontology][db_conn_i] )
    print(f"len(data)={len(data)}")
    
    #########################################################
    # (EQ_classes, total_stats, EQ_stats, metrics) = analyze_table(data, QI_SET, CATEGORICAL, K)

    dataset = Dataset(data, QI_SET, CATEGORICAL, K)
    metrics = {
        "GIL": dataset.calculate_GIL(),
        "DM": dataset.calculate_DM(),
        "CAVG": dataset.calculate_CAVG(),
        "Number of EQs": len(dataset.EQs)
    }

    #########################################################
    metrics_all[ontology] = metrics
    # EQ_classes_all[ontology] = EQ_classes    
    # total_stats_all[ontology] = total_stats
    # EQ_stats_all[ontology] = EQ_stats

#########################################################
# SAVE RESULTS TO CSV

with open(result_file, 'w') as outfile:
    json.dump(metrics_all, outfile)

print(f"Finished!")

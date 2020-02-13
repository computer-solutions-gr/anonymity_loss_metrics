
import pymongo 
import copy
from db import MongoRepository
import settings.etl_mondrian_settings as PARAMETERS
from settings.ontology_settings import ONTOLOGIES

from analyze_data import get_EQ_classes, get_EQs_stats, get_Partition_stats, calculate_GIL

########################################################
# MongoDB parameters
host = "localhost"
port = 27017
db_name = "etl_test"
mongo_repo = MongoRepository( host, port, db_name )   

########################################################

data = {}
EQ_classes = {}
EQ_stats = {}
total_stats = {}
GIL = {}
ontologies = ONTOLOGIES

for ontology_name in ontologies:   

    ONTOLOGY_PARAMETERS = getattr(PARAMETERS, ontology_name) 
    QI_SET = [key for key,val in ONTOLOGY_PARAMETERS["QI"].items() if val>0] 
    CATEGORICAL = ONTOLOGY_PARAMETERS["CATEGORICAL"]

    if len(QI_SET) == 0:
        continue   

    #########################################################
    # Get data from repository
    data_o = mongo_repo.get( ontology_name ) # keyword args
    data_o = [d for d in data_o]
    data[ontology_name] = copy.deepcopy(data_o)
    
    #########################################################
    # Get total data statistics
    # total_stats[ontology_name] = get_Partition_stats( data[ontology_name], ontology_name)
    total_stats[ontology_name] = get_Partition_stats( data[ontology_name], QI_SET, CATEGORICAL)

    #########################################################
    # Get EQuivalence classes & their stats for GILs      
    EQ_classes[ontology_name] = get_EQ_classes( data[ontology_name], QI_SET )
    
    EQ_stats[ontology_name] = get_EQs_stats( EQ_classes[ontology_name], QI_SET, CATEGORICAL)

    #########################################################
    # Calculate metrics
    GIL[ontology_name] = calculate_GIL( EQ_classes[ontology_name], EQ_stats[ontology_name], 
                                        total_stats[ontology_name], QI_SET )

    print(f"GIL for {ontology_name} = { GIL[ontology_name] }")

    #########################################################


print(f"Finished!")
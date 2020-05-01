
import pymongo 
import copy
import etl_mondrian_settings as PARAMETERS
from ontology_settings import ONTOLOGIES

# MongoDB parameters
host = "localhost"
port = 27017
db_name = "etl_test"

client = pymongo.MongoClient(host, port)
db = client[db_name]
# db = client.etl_test

#####################################################################

for ontology_name in ONTOLOGIES:   

    ontology_parameters = getattr(PARAMETERS, ontology_name) 
    # get QI set
    mondrian_allow = ontology_parameters["MONDRIAN_ALLOW"]
    qi_set = [key for key,val in mondrian_allow.items() if val>0]    
    
    if len(qi_set) == 0:
        continue

    k = ontology_parameters["k"]
    
    ##################################################################
    # Build dictionary for group query  
    group_fields_1 = {str(qi): "$" + str(qi) for qi in qi_set}
    group_fields_1["version"] = "$version"    

    mod_fields = ["ord_latitude", "ord_logitude"]
    group_fields_2 = copy.deepcopy(group_fields_1)
    for mf in mod_fields:
        group_fields_2[mf] = "$" + str(mf)
    
    ##################################################################
    no_ords_1 = db[ontology_name].find(
    {
        "ord_latitude": { "$exists": False },
        "ord_logitude": { "$exists": False }
    })
    no_ords_1 = list( no_ords_1 )

    ##################################################################
    no_ords_2 = db[ontology_name].aggregate([
    {
        "$match": {
            "ord_latitude": {"$exists": False},
            "ord_logitude": {"$exists": False} 
        }
    }
    ])
    no_ords_2 = list( no_ords_2 )

    ##################################################################
    
    group_result_1 = db[ontology_name].aggregate([
    {
        "$match": {
            "ord_latitude": {"$exists": False },
            "ord_logitude": {"$exists": False }
        }
    },
    {
        "$group": {
            "_id" : group_fields_1 ,
            "count" : { "$sum": 1 }
        }
    }
    ])
    
    group_result_1 = list(group_result_1)
    compromised_docs_1 = list( filter( lambda doc: doc["count"]<k, group_result_1 ) )    
    print(f"compromised_docs_1 = {compromised_docs_1}")

    ##################################################################

    group_result_2 = db[ontology_name].aggregate([
    {
        "$match": {
            "ord_latitude": {"$exists": True },
            "ord_logitude": {"$exists": True } 
        }
    },
    { 
        "$group": {
            "_id" : group_fields_2,
            "count" : { "$sum": 1 }
        }
    }
    ])

    group_result_2 = list(group_result_2)
    compromised_docs_2 = list( filter( lambda doc: doc["count"]<k, group_result_2 ) )    
    print(f"compromised_docs_2 = {compromised_docs_2}")


    ##################################################################



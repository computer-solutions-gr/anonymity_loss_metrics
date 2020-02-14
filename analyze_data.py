import itertools
import settings.etl_mondrian_settings as PARAMETERS
from settings.ontology_settings import ONTOLOGIES
from utils_parameters import set_key_order, set_categories
from utils_numbers import get_number

##############################################################################

def get_Partition_stats(Partition, QI_SET, CATEGORICAL):
    # Returns:
    # Partition_stats : {
    #   "address" : Number of distinct values in Partition (categorical attrs)
    #   "birthDate" : max(number)-min(number) in Partition (arithmetic attrs)
    # }

    Partition_data_distinct = get_distinct_data(Partition, QI_SET)
    Partition_stats = {}

    for qi in QI_SET:  
        if CATEGORICAL[qi]==1:
            try:      
                Partition_stats[qi] = len(Partition_data_distinct[qi])
            except:
                Partition_stats[qi] = 0
        else:
            nums = list(map(get_number, Partition_data_distinct[qi]))
            Partition_stats[qi]= max(nums)-min(nums)
            
    return Partition_stats

##############################################################################

def get_EQs_stats(EQ_classes, QI_SET, CATEGORICAL):
    # Returns:
    # EQ_stats = [
        # {
        #   "address" : Number of distinct values in EQ_class 1 (categorical attr)
        #   "birthDate" : max(number)-min(number) in EQ_class 1 (arithmetic attr)
        # },
        # {
        #   "address" : Number of distinct values in EQ_class 2 (categorical attrs)
        #   "birthDate" : max(number)-min(number) in EQ_class 2 (arithmetic attrs)
        # } 
    # ]
    EQ_stats = []
    for EQ_class in EQ_classes:
        EQ_stats_one = get_Partition_stats(EQ_class, QI_SET, CATEGORICAL)
        # EQ_stats_one = get_Partition_stats(EQ_class, ontology_name)
        EQ_stats.append(EQ_stats_one)
    return EQ_stats

##############################################################################

def get_EQ_classes(data, QI_SET):
    # Get all EQuivalence classes from data based on QI_SET

    EQ_classes = []    
    for key, group in itertools.groupby(data, lambda x: [x[qi] for qi in QI_SET] ):
        EQ_classes.append( list(group) )

    return EQ_classes

##############################################################################

def calculate_GIL( EQ_classes, EQ_stats, total_stats, QI_SET ):
    # Calculate Generalized Information Loss
    summ = 0
    total_records = 0

    for (EQ_index, EQ_class) in enumerate(EQ_classes):
        total_records = total_records + len(EQ_class)
        for qi in QI_SET:
            # for doc in EQ_class:
            for doc_index in range(len(EQ_class)):          
                part = EQ_stats[EQ_index][qi] /total_stats[qi] 
                summ = summ + part
    
    GIL = summ / (total_records * len(QI_SET))

    return GIL

##############################################################################

def calculate_DM( EQ_classes ):
    # Calculate Discernibility Metric
    DM = 0
    for EQ in EQ_classes:
        DM = DM + (len(EQ) ** 2)
    return DM

##############################################################################

def calculate_CAVG( EQ_classes, k ):
    # Calculate Average EQ class size metric
    total_EQs = len(EQ_classes)
    total_records = sum( [len(EQ) for EQ in EQ_classes] )
    C_avg = total_records / (total_EQs * k)        
    return C_avg 

##############################################################################

def get_distinct_data(data, QI_SET):
    # Returns a dictionary with all unique values per QI in QI_SET
    # data_distinct = {
    #   "key1": ["val11", "val12"],
    #   "key2": ["val21", "val22"]
    # }

    data_distinct = {}
    for qi in QI_SET:
        data_distinct[qi] = set()
    # for key, val in QI.items(): 
    #     data_distinct[key] = set()

    for doc in data:
        for qi in QI_SET:
        # for key, val in QI.items():  
        #     if val==0:
        #         continue          
            doc_field_vals = doc[qi].split("~")
            data_distinct[qi].update(doc_field_vals)

    # Convert distinct data sets to lists
    for qi, val in data_distinct.items():
        data_distinct[qi] = list( data_distinct[qi] )

    return data_distinct

##############################################################################    

# def map_data_to_nums(data_distinct):
#     data_distinct_map = {}
#     for key, val_list in data_distinct.items():
#         # val is a list
#         # data_distinct_map[key] = {}
#         d = {}
#         for (index,datum) in enumerate(val_list):
#             d[datum] = index
#         data_distinct_map[key] = d    
#     return data_distinct_map

##############################################################################    


import itertools
from partition import Partition

class Dataset():   


    def __init__(self, data, QI_SET, CATEGORICAL, K):
        # data should be a list of dicts
        # data = [
        # {"field1": "val11", "field2": "val12", ...  }
        # {"field1": "val21", "field2": "val22", ...  }
        #]
        self.data = data
        self.QI_SET = QI_SET
        self.CATEGORICAL = CATEGORICAL
        self.K = K
        self.EQs = self.get_EQs()
        pass
        # self.GIL = None
        # self.DM = None
        # self.CAVG = None
        # self.EQs_stats = []
    
    #############################################################################

    def get_EQs(self):
        # Gets all EQuivalence classes from dataset based on QI_SET
        EQs = []    
        for key, group in itertools.groupby(self.data, lambda x: [x[QI] for QI in self.QI_SET] ):
            EQs.append( list(group) )

        return EQs

    #############################################################################
    # def analyze_dataset(self, data, QI_SET, CATEGORICAL, K):
    # def analyze_dataset(self):        

    #     # # Get stats for whole table
    #     # whole_dataset_stats = self.get_partition_stats(self.data)

    #     # # Get stats for each EQ
    #     # EQs_stats = []       
    #     # for EQ in self.EQs:
    #     #     EQ_stats = self.get_partition_stats( EQ )
    #     #     EQs_stats.append(EQ_stats)
    #     # pass

    #     # Calculate metrics
    #     metrics = {}
    #     # metrics["GIL"] = calculate_GIL( EQ_stats, total_stats )
    #     metrics["GIL"] = calculate_GIL()
    #     metrics["DM"] = calculate_DM()
    #     metrics["C_AVG"] = calculate_CAVG()
    #     metrics["Number of EQs"] = len( self.EQs )

    #     return EQ_classes, total_stats, EQ_stats, metrics

    
    #############################################################################
    def get_partition_stats(self, partition_data):
        partition = Partition( partition_data, self.QI_SET, self.CATEGORICAL)
        stats = partition.get_stats()
        return stats

    #############################################################################

    # def calculate_GIL( self, EQ_stats, total_stats):
    def calculate_GIL( self ):
        # Calculate Generalized Information Loss for dataset

        # Get stats for whole table
        total_stats = self.get_partition_stats(self.data)

        # Get stats for each EQ
        EQs_stats = []       
        for EQ_class in self.EQs:
            EQ_stats = self.get_partition_stats( EQ_class )
            EQs_stats.append(EQ_stats)
        pass

        #####################################
        summ = 0
        total_records = 0

        for (EQ_index, EQ_class) in enumerate( self.EQs ):
            total_records = total_records + len(EQ_class)
            for QI in self.QI_SET:
                # for doc in EQ_class:
                for doc_index in range(len(EQ_class)):          
                    part = EQs_stats[EQ_index][QI] /total_stats[QI] 
                    summ = summ + part
        
        GIL = summ / (total_records * len(self.QI_SET))

        return GIL

    ##############################################################################

    def calculate_DM( self ):
        # Calculate Discernibility Metric
        DM = 0
        for EQ in self.EQs:
            DM = DM + (len(EQ) ** 2)
        return DM
    
    ##############################################################################

    def calculate_CAVG( self ):
        # Calculate Average EQ class size metric
        total_EQs = len( self.EQs )
        total_records = len( self.data )
        # total_records = sum( [len(EQ) for EQ in self.EQs] )
        C_AVG = total_records / (total_EQs * self.K)        
        return C_AVG 

    #############################################################################

    # def get_EQs_stats(EQ_classes, QI_SET, CATEGORICAL):
    # def get_EQs_stats(self):
    #     # Returns:
    #     # EQ_stats = [
    #         # {
    #         #   "address" : Number of distinct values in EQ_class 1 (categorical attr)
    #         #   "birthDate" : max(number)-min(number) in EQ_class 1 (arithmetic attr)
    #         # },
    #         # {
    #         #   "address" : Number of distinct values in EQ_class 2 (categorical attrs)
    #         #   "birthDate" : max(number)-min(number) in EQ_class 2 (arithmetic attrs)
    #         # } 
    #     # ]
    #     EQ_stats = []
    #     # for EQ_class in EQ_classes:
    #     for EQ_class in self.EQs:
    #         partition = Partition(EQ_class, self.QI_SET, self.CATEGORICAL)
    #         EQ_stats_one = partition.get_stats()
    #         # EQ_stats_one = get_Partition_stats(EQ_class, ontology_name)
    #         EQ_stats.append(EQ_stats_one)
    #     self.EQs_stats = EQ_stats
        # return EQ_stats

    #############################################################################

  


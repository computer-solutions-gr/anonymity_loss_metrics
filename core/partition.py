from core.utils_numbers import get_number

class Partition():

    def __init__(self, data, QI_SET, CATEGORICAL):
        # self.data is a list of dicts! 
        self.data = data
        self.QI_SET = QI_SET
        self.CATEGORICAL = CATEGORICAL
        pass
        # self.stats = {}

    #########################################################

    def get_stats(self):
        # self.data is a list of dicts!
        # Returns:
        # Partition_stats : {
        #   "address" : Number of distinct values in Partition (categorical attrs)
        #   "birthDate" : max(number)-min(number) in Partition (arithmetic attrs)
        # }

        Partition_data_distinct = self.get_distinct_data()
        Partition_stats = {}

        for QI in self.QI_SET:
            if self.CATEGORICAL[QI]==1:
                try:
                    Partition_stats[QI] = len(Partition_data_distinct[QI])-1
                except:
                    Partition_stats[QI] = 0
            else:
                nums = list(map(get_number, Partition_data_distinct[QI]))
                Partition_stats[QI]= max(nums)-min(nums)

        # self.stats = Partition_stats
        # return Partition_stats
        return Partition_stats


    #########################################################

    def get_distinct_data(self):
        # self.data is a list of dicts! 

        # Returns a dictionary with all unique values per QI in QI_SET
        # data_distinct = {
        #   "key1": ["val11", "val12"],
        #   "key2": ["val21", "val22"]
        # }

        data_distinct = {}
        for QI in self.QI_SET:
            data_distinct[QI] = set()

        for doc in self.data:
            for QI in self.QI_SET:
                doc_field_vals = doc[QI].split("~")
                data_distinct[QI].update(doc_field_vals)

        # Convert distinct data sets to lists
        for qi, val in data_distinct.items():
            data_distinct[qi] = list( data_distinct[qi] )

        return data_distinct
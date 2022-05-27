

from typing import List
from core.utils_files import *
import csv
from core.dataset import Dataset

import settings.CSVdata_settings as SETTINGS


categorical_attributes = getattr(SETTINGS, "CATEGORICAL_ATTRIBUTES")
input_directory = getattr(SETTINGS, 'INPUT_DIRECTORY')
result_filepath = getattr(SETTINGS, 'RESULT_FILEPATH')


#########################################################
results = []

input_files = get_files_in_directory(input_directory)

for filepath in input_files:
    k, qi_set = get_parameters_from_filepath(filepath)
    if k is None or qi_set in [[], None]:
        print(f'No anonymization parameters detected in filepath {filepath}')
        continue

    data = get_data_from_file(filepath)

    dataset = Dataset(data, qi_set, categorical_attributes, k)
    metrics = {
        "GIL": dataset.calculate_GIL(),
        "DM": dataset.calculate_DM(),
        "CAVG": dataset.calculate_CAVG(),
        "Number of EQs": len(dataset.EQs)
    }
    result_dict = {'k': k, 'qi_set': ','.join(qi_set)}
    result_dict.update(metrics)
    results.append(result_dict)


#########################################################
results.sort(key=lambda x: (len(x['qi_set']), x['k']))

headers = results[0].keys()

with open(result_filepath, 'w') as outfile:
    dict_writer = csv.DictWriter(outfile, headers)
    dict_writer.writeheader()
    dict_writer.writerows(results)


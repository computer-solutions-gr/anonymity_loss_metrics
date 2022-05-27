
# QI = {"AGE": 1, "SEX": 1, "CURADM_DAYS": 1, "OUTCOME": 0, "CURRICU_FLAG":0,
#        "PREVADM_NO":0, "PREVADM_DAYS":0, "PREVICU_DAYS":0, "READMISSION_30_DAYS":0}
# K = 20

CATEGORICAL_ATTRIBUTES = {"AGE": 0, "SEX": 1, "CURADM_DAYS": 0, "OUTCOME": 1, "CURRICU_FLAG":1,
                            "PREVADM_NO":0, "PREVADM_DAYS":0, "PREVICU_DAYS":0, "READMISSION_30_DAYS":1}



INPUT_DIRECTORY = "/home/arianna/CSL Docs/Papers/Paper_Anonymized_ML/dataset"
RESULT_DIRECTORY = f"/home/arianna/CSL Docs/Papers/Paper_Anonymized_ML/loss_metric_results"
RESULT_FILEPATH = f'{RESULT_DIRECTORY}/anonymity_results.csv'
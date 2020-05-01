"""
Parameters for etl & mondrian
"""


Patient = {
    "resourceType" : "Patient",    
    "QI": {"resourceType" : 0, "birthDate" : 1, "address" : 1, "gender" : 0,
            "ord_latitude" : 1, "ord_logitude" : 1, "version" : 0},
    "CATEGORICAL": { "resourceType" : 1, "birthDate" : 0, "address" : 1, "gender" : 1, 
                    "ord_latitude" : 0, "ord_logitude" : 0, "version" : 1},
    "k":10  
}

# Observation = {
#     "resourceType" : "Observation",
#     "QI": {"resourceType":0},
#     "CATEGORICAL": { "resourceType" : 1}
# }

# DiagnosticReport = {
#     "resourceType" : "DiagnosticReport",
#     "QI" : {"resourceType":0},
#     "CATEGORICAL": { "resourceType" : 1}
# }

# Location = {
#     "resourceType" : "Location",
#     "QI" : {"resourceType":0},
#     "CATEGORICAL": { "resourceType" : 1}
# }

# Encounter = {
#     "resourceType" : "Encounter",
#     "QI" : {"resourceType":0},
#     "CATEGORICAL": { "resourceType" : 1}
# }


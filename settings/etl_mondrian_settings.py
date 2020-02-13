"""
Parameters for etl & mondrian
"""

#PATIENT = {
Patient = {
    "resourceType" : "Patient",
    # "MONDRIAN_ALLOW": {"resourceType" : 0, "birthDate" : 1, "address" : 1, "gender" : 0, 
    #                     "ord_latitude" : 1, "ord_logitude" : 1, "version" : 0},
    "QI": {"resourceType" : 0, "birthDate" : 1, "address" : 1, "gender" : 0,
            "ord_latitude" : 1, "ord_logitude" : 1, "version" : 0},
    "CATEGORICAL": { "resourceType" : 1, "birthDate" : 0, "address" : 1, "gender" : 1, 
                    "ord_latitude" : 0, "ord_logitude" : 0, "version" : 1},
    "k":5
        
    #"KEY_ORDER":{"resourceType":0,"birthDate":1,"address":2,"gender":3},    
    
}

#OBSERVATION = {
Observation = {
    "resourceType" : "Observation",
    "QI": {"resourceType":0},
    "CATEGORICAL": { "resourceType" : 1},
    # "MONDRIAN_ALLOW": {"resourceType":0},
    #"KEY_ORDER":{"resourceType":1,"birthDate":1,"address":1,"gender":0},
    "k":5
  
}

DiagnosticReport = {
    "resourceType" : "DiagnosticReport",
    "QI" : {"resourceType":0},
    "CATEGORICAL": { "resourceType" : 1},
    # "MONDRIAN_ALLOW": {"resourceType":0},
    "k":5
}

Location = {
    "resourceType" : "Location",
    "QI" : {"resourceType":0},
    "CATEGORICAL": { "resourceType" : 1},
    # "MONDRIAN_ALLOW": {"resourceType":0},
    "k":5
}
Encounter = {
    "resourceType" : "Encounter",
    "QI" : {"resourceType":0},
    "CATEGORICAL": { "resourceType" : 1},
    # "MONDRIAN_ALLOW": {"resourceType":0},
    "k":5
}


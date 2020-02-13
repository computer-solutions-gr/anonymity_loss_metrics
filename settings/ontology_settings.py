"""
Ontologies to convert to Fhir and anonymize
"""

ONTOLOGIES = [ "Patient", "Encounter", "Observation", "DiagnosticReport", "Location" ]
# ONTOLOGIES = ["Encounter" ]

ONTOLOGY_KEYS = {"Patient":"pid", 
                "Observation":"listest_id", 
                "DiagnosticReport":"nr", 
                "Location": "nr",
                "Encounter": "encounter_nr"}
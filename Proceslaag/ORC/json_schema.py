#Leeg json schema voor de metadata van een ORC bestand
#meta_data = {
#    "name": "",
#    "namePlural": "",
#    "description": "",
#    "dataClassification": "", #Kies uit open, intern, confidential, strictly confidential
#    "maintainerOrganization": "",
#    "maintainerDepartment": "",
#    "contactPerson": "",
#    "contactEmail": "",
#    "source": "",
#    "updateFrequency": "", #Kies uit Realtime, Hourly, Daily, Weekly, Monthly, , Yearly of Unknown
#    "providerOrganization": "",
#    "documentationUrl": ""
#}

#json_schema= {
#    "$schema": "http://json-schema.org/draft-07/schema#",
#    "type": "object",
#    "properties": {
#    },
#    "required": []
#}

import json

def create_metadata_and_json_schema():
    data_classification_options = ["open", "intern", "confidential", "strictly confidential"]
    update_frequency_options = ["realtime", "hourly", "daily", "weekly", "monthly", "yearly", "unknown"]

    meta_data = {
        "name": input("Enter name: "),
        "namePlural": input("Enter namePlural: "),
        "description": input("Enter description: "),
        "dataClassification": "",
        "maintainerOrganization": input("Enter maintainerOrganization: "),
        "maintainerDepartment": input("Enter maintainerDepartment: "),
        "contactPerson": input("Enter contactPerson: "),
        "contactEmail": input("Enter contactEmail: "),
        "source": input("Enter source: "),
        "updateFrequency": "",
        "providerOrganization": input("Enter providerOrganization: "),
        "documentationUrl": input("Enter documentationUrl: ")
    }
    
    # Valideer dataClassification input
    while meta_data["dataClassification"] not in data_classification_options:
        print(f"Valid options: {', '.join(data_classification_options)}")
        meta_data["dataClassification"] = input("Enter dataClassification: ")
        
    # Valideer updateFrequency input
    while meta_data["updateFrequency"] not in update_frequency_options:
        print(f"Valid options: {', '.join(update_frequency_options)}")
        meta_data["updateFrequency"] = input("Enter updateFrequency: ")

    # Voorbereiden van json_schema
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "required": []
    }
    
    # Verzamel eigenschappen voor json_schema van de gebruiker
    while True:
        property_name = input("Enter property name (or press enter to finish): ")
        if not property_name:
            break
        
        property_type = input(f"Enter type for '{property_name}' (e.g., string, integer): ")
        property_description = input(f"Enter description for '{property_name}': ")
        is_required = input(f"Is '{property_name}' required? (yes/no): ").lower() == 'yes'
        
        json_schema['properties'][property_name] = {
            "type": property_type,
            "description": property_description
        }
        
        if is_required:
            json_schema['required'].append(property_name)
    
    # Verzamel de gewenste bestandsnaam van de gebruiker
    filename = input("Enter the desired filename (without extension): ") + '.py'
    
    # Sla de meta_data en json_schema op in een Python-bestand
    with open(filename, 'w') as file:
        file.write(f"meta_data = {json.dumps(meta_data, indent=4)}\n\n")
        file.write(f"json_schema = {json.dumps(json_schema, indent=4)}\n")
    
    print(f"File '{filename}' successfully created.")

create_metadata_and_json_schema()

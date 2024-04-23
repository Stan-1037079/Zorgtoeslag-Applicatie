meta_data_zorg = {
    "name": "Zorgtoeslag",
    "namePlural": "Zorgtoeslagen",
    "description": "Zorgtoeslag",
    "dataClassification": "open",
    "maintainerOrganization": "",
    "maintainerDepartment": "",
    "contactPerson": "Stan",
    "contactEmail": "Stanverdoorn@gmail.com",
    "source": "Belastingdienst",
    "updateFrequency": "yearly",
    "providerOrganization": "",
    "documentationUrl": "https://www.belastingdienst.nl/wps/wcm/connect/nl/zorgtoeslag/content/kan-ik-zorgtoeslag-krijgen"
}

json_schema_zorg = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "Inkomen": {
            "type": "integer",
            "description": "Het inkomen van de gebruiker"
        },
        "18 jaar of ouder?": {
            "type": "string",
            "description": "Is de gebruiker ouder dan 18 ja of nee?"
        },
        "Toeslagpartner?": {
            "type": "string",
            "description": "Heeft de gebruiker een toeslagpartner ja of nee?"
        },
        "Vermogen": {
            "type": "integer",
            "description": "Het vermogen van de gebruiker"
        },
        "Zorgtoeslag": {
            "type": "integer",
            "description": "Het bedrag aan zorgtoeslag dat de gebruiker ontvangt"
        }
    },
    "required": ["Vermogen","Inkomen","18 jaar of ouder?","Toeslagpartner?", "Zorgtoeslag"]
}

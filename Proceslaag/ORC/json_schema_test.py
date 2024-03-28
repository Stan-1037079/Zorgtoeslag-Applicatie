test_data = {
    "name": "Koek",
    "namePlural": "Koekjes",
    "description": "Lekkere koekjes.",
    "dataClassification": "open",
    "maintainerOrganization": "Koek organization",
    "maintainerDepartment": "Koek API department",
    "contactPerson": "Koekie Monster",
    "contactEmail": "monster@lovescookies.nl",
    "source": "Koekiemonster",
    "updateFrequency": "monthly",
    "providerOrganization": "Open data for koekjes",
    "documentationUrl": "https://nl.wikipedia.org/wiki/Koekiemonster"
}

json_schema_koek = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "smaak": {
            "type": "string",
            "description": "De smaak van het koekje."
        },
        "aantal": {
            "type": "integer",
            "description": "Hoeveel koekjes er in een pakje zitten."
        }
    },
    "required": ["smaak", "aantal"]
}
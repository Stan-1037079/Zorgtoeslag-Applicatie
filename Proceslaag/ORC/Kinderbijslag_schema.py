kinderbijslag_meta_data = {
    "name": "Kinderbijslag",
    "namePlural": "Kinderbijslagen",
    "description": "Kinderbijslag",
    "dataClassification": "open",
    "maintainerOrganization": "",
    "maintainerDepartment": "",
    "contactPerson": "Stan",
    "contactEmail": "Stanverdoorn@gmail.com",
    "source": "SVB",
    "updateFrequency": "yearly",
    "providerOrganization": "",
    "documentationUrl": "https://www.svb.nl/nl/kinderbijslag/bedragen-betaaldagen/bedragen-kinderbijslag"
}

Kinderbijslag_json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "Leeftijd kind": {
            "type": "string",
            "description": "Leeftijd kind"
        },
        "Bedrag": {
            "type": "integer",
            "description": "Bedrag kinderbijslag per kwartaal"
        }
    },
    "required": ["Leeftijd kind", "Bedrag"]
}

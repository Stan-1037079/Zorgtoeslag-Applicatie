import requests
from conf import urls_tokens
conf = urls_tokens()
from json_schema_test import test_data, json_schema_koek

def postObjecttype(objecttype_data, json_schema, headers ={"Authorization": "Token " + conf['token_object_types'], "Content-Type": "application/json"}):
    #base_url_object_types = "http://localhost:8001/api/v1"
    #conf["base_url_object_types"]
    # Objecttype aanmaken
    response = requests.post(f"{conf['base_url_object_types']}/objecttypes", headers=headers, json=objecttype_data)
    if response.status_code == 201:
        objecttype_url = response.json()["url"]
        print(f"Objecttype aangemaakt: {objecttype_url}")
    else:
        print("Fout bij het aanmaken van objecttype:", response.text)
        return None

    # JSON-schema toevoegen
    # Haalt het UUID van het objecttype op uit de URL en pakt de laatste element van de lijst (het UUID)
    objecttype_uuid = objecttype_url.split('/')[-1]
    response = requests.post(f"{conf['base_url_object_types']}/objecttypes/{objecttype_uuid}/versions", headers=headers, json={"status": "draft", "jsonSchema": json_schema})
    if response.status_code == 201:
        version_url = response.json()["url"]
        print(f"Versie aangemaakt voor objecttype: {version_url}")
        return objecttype_uuid
    else:
        print("Fout bij het toevoegen van JSON-schema aan objecttype:", response.text)
        return None
    
    #postObjecttype(test_data, json_schema_koek)
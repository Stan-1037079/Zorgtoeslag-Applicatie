import requests
from conf import urls_tokens
conf = urls_tokens()
from json_schema_test import test_data, json_schema_koek
# DRY: Don't Repeat Yourself

def getObject(requestUrl):
    
    data = requests.get(conf['base_url_objects'] + requestUrl, headers={'Authorization': 'Token ' + conf['token_objects']} )
    dataJson = data.json()
    if data.status_code == 200:
        print("Objecten opgehaald")

    for i in dataJson['results']:
        print(str(i["record"]["data"]))

def putObject(requestUrl, data):
    data = requests.get(requestUrl, headers={'Authorization': 'Token cd63e158f3aca276ef284e3033d020a22899c728'} )
    print("Hello World")

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

def Postobject(token_objects, objecttype_uuid, object_data,base_url_objects):
    base_url = "http://localhost:8000/api/v2"
    headers = {
        "Authorization": f"Token {token_objects}",
        "Content-Type": "application/json"
    }
    # Object aanmaken binnen het objecttype
    response = requests.post(f"{base_url}/objects", headers=headers, json=object_data)
    if response.status_code == 201:
        object_url = response.json()["url"]
        print(f"Object aangemaakt: {object_url}")
    else:
        print("Fout bij het aanmaken van object:", response.text)

#getObject('/objects?type=http://localhost:8001/api/v1/objecttypes/feeaa795-d212-4fa2-bb38-2c34996e5702')
#postObjecttype(test_data, json_schema_koek)
import requests
from conf import urls_tokens
conf = urls_tokens()
from json_schema_test import test_data, json_schema_koek
from objecttypes import getAllObjecttypes
import json
from object_metadata import object_metadata

# DRY: Don't Repeat Yourself

def getObject(requestUrl):
    
    data = requests.get(conf['base_url_objects'] + requestUrl, headers={'Authorization': 'Token ' + conf['token_objects']} )
    dataJson = data.json()
    if data.status_code == 200:
        print("Objecten opgehaald")

    for i in dataJson['results']:
        print(str(i["record"]["data"]))

def getAllObjects(headers = {"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json"}):
    
    response = requests.get(f"{conf['base_url_objects']}/objects", headers=headers)
    if response.status_code == 200:
        
        objects = response.json()
        print(json.dumps(objects, indent=2))

def putObject(requestUrl, data):
    data = requests.get(requestUrl, headers={'Authorization': 'Token cd63e158f3aca276ef284e3033d020a22899c728'} )
    print("Hello World")

def postObject(objecttype_uuid, object_data, headers={"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json", 'Content-Crs': 'EPSG:4326'}):

    # Voeg het UUID van het objecttype toe aan de data
    object_data = {
        "type": f"{conf['base_url_object_types']}/objecttypes/{objecttype_uuid}",
        "record": object_data
    }

    # Object aanmaken binnen het objecttype
    response = requests.post(f"{conf['base_url_objects']}/objects", headers=headers, json=object_data)

    if response.status_code == 201:
        object_url = response.json()["url"]
        print(f"Object aangemaakt: {object_url}")
    else:
        print("Fout bij het aanmaken van object:", response.text)

def postObjecty(objecttype_uuid, object_data2):
    # headers_for_get = {"Authorization": "Token " + conf['token_object_types'], "Content-Type": "application/json"}
    headers_for_post = {"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json", 'Content-Crs': 'EPSG:4326'}

    # responses = requests.get(f"{conf['base_url_object_types']}/objecttypes/{objecttype_uuid}", headers=headers_for_get)
    # if responses.status_code == 200:
    #     objecttype_url = responses.json()["url"]
    #     print(f"Objecttype opgehaald: {objecttype_url}")

    # Voeg het UUID van het objecttype toe aan de data
    object_data = {
        "type": conf["base_url_object_types"] + "/objecttypes/f0d053fb-e00d-40e5-a810-56a8ae89901d",
        "record": object_data2
    }
    print(f"{conf['base_url_objects']}/objects")
    print(object_data2)
    # Object aanmaken binnen het objecttype
    response = requests.post(f"{conf['base_url_objects']}/objects", headers=headers_for_post, json=object_data)
    print("-------")

    print(object_data)

    if response.status_code == 201:
        object_url = response.json()["url"]
        print(f"Object aangemaakt: {object_url}")
    else:
        print("Fout bij het aanmaken van object:", response.text)

def getObjectsZorgtoeslag(headers = {"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json"}):
    
    response = requests.get(f"{conf['base_url_objects_zorgtoeslag']}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def getObjectsZorgtoeslagen(headers = {"Authorization": "Token " + conf['token_objects'], "Content-Type": "application/json"}):
    
    response = requests.get(f"{conf['base_url_objects_zorgtoeslag']}", headers=headers)
    if response.status_code == 200:
        objects = response.json()
        print(json.dumps(objects, indent=2))
    return None

#getObjectsZorgtoeslagen()
#getObject('/objects?type=http://localhost:8001/api/v1/objecttypes/feeaa795-d212-4fa2-bb38-2c34996e5702')
#getAllObjecttypes()
#getAllObjects()
#postObjecty("f0d053fb-e00d-40e5-a810-56a8ae89901d", object_metadata)
import requests
from conf import urls_tokens
conf = urls_tokens()
from json_schema_test import test_data, json_schema_koek

def getAllObjecttypes(headers = {"Authorization": "Token " + conf['token_object_types'], "Content-Type": "application/json"}):
    # Stuur een GET-verzoek naar het endpoint voor alle objecttypes
    response = requests.get(f"{conf['base_url_object_types']}/objecttypes", headers=headers)
    
    # Controleer of de request succesvol was
    if response.status_code == 200:
        # De response.json() methode converteert de JSON response naar een Python dictionary of list
        objecttypes = response.json()
        
        for objecttype in objecttypes:
            print(objecttype)  
    else:
        print("Fout bij het ophalen van objecttypes:", response.text)

def getAllObjecttypesUID(headers = {"Authorization": "Token " + conf['token_object_types'], "Content-Type": "application/json"}):
    response = requests.get(f"{conf['base_url_object_types']}/objecttypes", headers=headers)
    
    if response.status_code == 200:
        objecttypes = response.json()
        
        for objecttype in objecttypes:
            if "uuid" in objecttype and "name" in objecttype and "versions" in objecttype:
                print(f"Name: {objecttype['name']}\n, UUID: {objecttype['uuid']}\n, Versions: {objecttype['versions']}")
            else:
                print("Een of meer vereiste velden ontbreken in objecttype")
    else:
        print("Fout bij het ophalen van objecttypes:", response.text)

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
    
def deleteObjecttype(objecttype_uuid, versions, headers={"Authorization": "Token " + conf['token_object_types']}):
    # Verwijder elke versie voor dit objecttype dit moet eerst gebeuren voordat het objecttype zelf verwijderd kan worden
    # for loop itereert door de lijst van versies
    for version_url in versions:
        version_response = requests.delete(version_url, headers=headers)
        if version_response.status_code != 204:
            print(f"Fout bij het verwijderen van versie {version_url}: {version_response.text}")
            return False
        print(f"Versie {version_url} succesvol verwijderd.")
    
    # Na het succesvol verwijderen van alle versies, het objecttype zelf verwijderen
    objecttype_url = f"{conf['base_url_object_types']}/objecttypes/{objecttype_uuid}"
    objecttype_response = requests.delete(objecttype_url, headers=headers)
    
    if objecttype_response.status_code == 204:
        print(f"Objecttype {objecttype_uuid} succesvol verwijderd.")
        return True
    else:
        print(f"Fout bij het verwijderen van objecttype {objecttype_uuid}: {objecttype_response.text}")
        return False

#postObjecttype(test_data, json_schema_koek)
#getAllObjecttypes()
#getAllObjecttypesUID()
    
#Geef UUID en versies van objecttypes mee aan de deleteObjecttype functie (gebruik de functie getAllObjecttypesUID() om deze informatie op te halen
#deleteObjecttype("33ecd272-61e9-4af8-9afc-16f660627a28", ["http://localhost:8001/api/v1/objecttypes/33ecd272-61e9-4af8-9afc-16f660627a28/versions/1"])

import http.client
import api_key
import json
import os 
from pathlib import Path

connection = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': api_key.api_key,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

def get_response(endpoint, file_name):
       
    connection.request("GET", endpoint, headers=headers)
    result = connection.getresponse()
    response_body = result.read()
    # # print('response_body',response_body) 
    decoded_data = response_body.decode(encoding="utf-8")
  
    # # deserialize the json data to a python dictionary 
    reponse_dict = json.loads(decoded_data)

    # # extract reponse part of the data
    response = reponse_dict['response']
    file_path = os.path.join(os.curdir, file_name)

    with open(file_path, 'w') as file:
        json.dump(response, file, indent=4)

    return response

def load_api_response(file_name='teams_info.json'):
    file_path = Path('.') / file_name
    null = None
    if file_path.exists():
        with open(file_path, 'r') as file:
            print('here',file)
            return json.load(file)
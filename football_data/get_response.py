import http.client
import api_key
import json

connection = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': api_key.api_key,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

def get_response(items_to_fetch):

    connection.request("GET", items_to_fetch, headers=headers)
    result = connection.getresponse()
    response_body = result.read()

    decoded_data = response_body.decode(encoding="utf-8")
  
    # deserialize the json data to a python dictionary 
    reponse_dict = json.loads(decoded_data)

    # extract reponse part of the data
    response = reponse_dict['response']

    return response
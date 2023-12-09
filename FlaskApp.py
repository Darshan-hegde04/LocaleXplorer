import awsgi
from flask import Flask, request, Response
import requests
import json

#Initiate a Flask App
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_results():
    #Store the required parameters in variables
    query_dict = request.args.to_dict(flat=False)
    latitude = f"{query_dict['latitude'][0]}"
    longitude = f"{query_dict['longitude'][0]}"
    query = f"{query_dict['query'][0]}"
    limit = f"{query_dict['limit'][0]}"

    #URL endpoint
    dis_url = f"https://discover.search.hereapi.com/v1/discover?at={latitude},{longitude}&limit={limit}&q={query}&apikey={api_key}"

    #Here API get request
    response_dis = requests.get(dis_url)
    data_disco = response_dis.json()

    # Check for successful Here API response
    if response_dis.status_code == 200:
        #Empty list for storing multiple responses
        response_list=[]

        for item in data_disco['items']:
            title = item['title']
            address = item['address']['label']
            latitude = item['position']['lat']
            longitude = item['position']['lng']

            opening_hours = item.get('openingHours', [])
            if opening_hours:
                opening_hours_text = opening_hours[0].get('text', [])
                if opening_hours_text:
                    opening_hours_text = ', '.join(opening_hours_text)
                else:
                    opening_hours_text = "Not available"
            else:
                opening_hours_text = "Not available"

            contacts = item.get('contacts', [])
            contact_numbers = []
            for contact in contacts:
                phones = contact.get('phone', [])
                for phone in phones:
                    contact_numbers.append(phone['value'])

            websites = []
            www_values = item.get('www', [])
            for www_value in www_values:
                websites.append(www_value['value'])

            #Formatting the required response
            response = {"Title": f"{title}", "Address": f"{address}", "Latitude": f"{latitude}", "Longitude": f"{longitude}", "Opening Hours": f"{opening_hours_text}", "Contact Numbers": f"{', '.join(contact_numbers)}", "Websites" : f"{', '.join(websites)}"}
            response_list.append(response)

        response = json.dumps(response_list, indent=4)
        data = json.loads(response)
        json_data = json.dumps(data)
        return Response(json_data, status=200, mimetype='application/json')

    #For unsuccessful Here API response
    else:
        response = {"Error": f"{response_dis.status_code}"}
        response = json.dumps(response, indent=4)
        data = json.loads(response)
        json_data = json.dumps(data)
        return Response(json_data, status=400, mimetype='application/json')

#Deploying the REST API using AWS Lambda and API Gateway integration
#Lambda function handler
def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})
    

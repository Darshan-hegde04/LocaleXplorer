import awsgi
from flask import Flask, request, Response
import requests
import json

# Initiate a Flask App
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_results():
    query_dict = request.args.to_dict(flat=False)
    req = f"{query_dict['requesting'][0]}"

    #If Details requested
    if req == "details":
        #Example request: https://170fr34z82.execute-api.us-east-1.amazonaws.com/Dev?requesting=details&latitude=13.100120&longitude=77.596350&query=electronic&limit=2
        # Store the required parameters in variables
        latitude = f"{query_dict['latitude'][0]}"
        longitude = f"{query_dict['longitude'][0]}"
        query = f"{query_dict['query'][0]}"
        limit = f"{query_dict['limit'][0]}"

        # URL endpoint
        dis_url = f"https://discover.search.hereapi.com/v1/discover?at={latitude},{longitude}&limit={limit}&q={query}&apikey={api_key}"

        # Here API get request
        response_dis = requests.get(dis_url)
        data_disco = response_dis.json()

        # Check for successful Here API response
        if response_dis.status_code == 200:
            # Empty list for storing multiple responses
            response_list = []

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
                    phones = contact.get('mobile', [])
                    for phone in phones:
                        contact_numbers.append(phone['value'])

                websites = []
                # www_values = item.get('www', [])
                try:
                    www_values = contacts[0]["www"][0]['value']
                except:
                    www_values = item.get('www', [])
                # www_values = item[0]['www'][0]['value']

                try:
                    websites.append(www_values)
                except:
                    for www_value in www_values:
                        websites.append(www_value)
                if len(websites[0]) == 0:
                    websites[0] = "Not available"

                # Formatting the required response
                response = {"Title": f"{title}", "Address": f"{address}", "Latitude": f"{latitude}",
                            "Longitude": f"{longitude}", "Opening Hours": f"{opening_hours_text}",
                            "Contact Numbers": f"{', '.join(contact_numbers)}", "Websites": f"{websites[0]}"}
                if (len(contact_numbers) == 0):
                    contact_numbers = "Not available"
                    response = {"Title": f"{title}", "Address": f"{address}", "Latitude": f"{latitude}",
                                "Longitude": f"{longitude}", "Opening Hours": f"{opening_hours_text}",
                                "Contact Numbers": f"{contact_numbers}", "Websites": f"{websites[0]}"}

                response_list.append(response)

            # Return json
            response = json.dumps(response_list, indent=4)
            data = json.loads(response)
            json_data = json.dumps(data)
            return Response(json_data, status=200, mimetype='application/json')

        # For unsuccessful Here API response
        else:
            response = {"Error": f"{response_dis.status_code}"}
            # Return json
            response = json.dumps(response, indent=4)
            data = json.loads(response)
            json_data = json.dumps(data)
            return Response(json_data, status=400, mimetype='application/json')

    #If user location requested
    elif req == "location":
        #Example request: https://170fr34z82.execute-api.us-east-1.amazonaws.com/Dev?requesting=location&latitude=13.100120&longitude=77.596350
        # Store the required parameters in variables
        query_dict = request.args.to_dict(flat=False)
        latitude = f"{query_dict['latitude'][0]}"
        longitude = f"{query_dict['longitude'][0]}"

        # # Get user's current location from Here API with lat and lon
        geo_url = f"https://revgeocode.search.hereapi.com/v1/revgeocode?at={latitude},{longitude}&types=street&apikey={api_key}"
        response_dis = requests.get(geo_url)
        if response_dis.status_code == 200:
            try:
                data_disco = response_dis.json()
                street = data_disco['items'][0]['address']['street']
                district = data_disco['items'][0]['address']['district']
                city = data_disco['items'][0]['address']['city']
                response = {"location": f"{street}, {district}, {city}"}
            except:
                response = {"Error": "Unable to get Location"}

            response = json.dumps(response, indent=4)
            data = json.loads(response)
            json_data = json.dumps(data)
            return Response(json_data, status=200, mimetype='application/json')

    else:
        #If the request format is invalid
        response = {"Error": "Invalid request. Check again."}

        response = json.dumps(response, indent=4)
        data = json.loads(response)
        json_data = json.dumps(data)
        return Response(json_data, status=200, mimetype='application/json')


# Deploying the REST API using AWS Lambda and API Gateway integration
# Lambda function handler
def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})


if __name__ == '__main__':
    app.run()


import requests


headers = {
    "X-RapidAPI-Key": "73a1dc7d81msh330b3a9c23cb99dp13f4a1jsnc0618f6e29aa",
    "X-RapidAPI-Host": "local-business-data.p.rapidapi.com"
}

search_url = "https://local-business-data.p.rapidapi.com/search"
reviews_url = "https://local-business-data.p.rapidapi.com/business-reviews"

querystring = {"query": #address of shop with name ,
               "limit": "1", "lat": latitude , "lng": longitude , "zoom": "13", "language": "en", "region": "ind"}

search_response = requests.get(search_url, headers=headers, params=querystring)

data = search_response.json()
business_id = data["data"][0]["business_id"]
data_response = data["data"]
rating = data["data"][0]["rating"]
photo = data["data"][0]["photos_sample"][0]["photo_url_large"]




review_string = {f"business_id": business_id, "limit": "10", "region": "ind", "language": "en"}
review_response = requests.get(reviews_url, headers=headers, params=review_string)

review_data = review_response.json()

if 'data' in review_data and review_data['data']:
    
    for review in review_data['data']:
        review_text = review.get('review_text', 'No review text available')
        print(f"Review Text: {review_text}")
else:
    print("No review data found in the response.")


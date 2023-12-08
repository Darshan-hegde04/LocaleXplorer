import requests

#  API key
api_key = "lgblBT4r0F8zXJn80OA7jV5uExXqfv2EySrCim1nViA"

# coordinates
latitude = 12.98995222860768
longitude = 75.34099184798936

# query_location
query = "Hotel Panchami"
limit = 1

# URL
dis_url = f"https://discover.search.hereapi.com/v1/discover?at={latitude},{longitude}&limit={limit}&q={query}&apikey={api_key}"


# request
response_dis = requests.get(dis_url)

data_disco = response_dis.json()




# Check for successful response
if response_dis.status_code == 200:
    # Query Api Result
    query = data_disco["items"][0]["position"]
    q_address = data_disco["items"][0]["address"]
    q_street = q_address["label"]
    q_city = q_address["city"]
    q_postalCode = q_address["postalCode"]
    q_lat = query["lat"]
    q_lng = query["lng"]

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

        print(f"Title: {title}")
        print(f"Address: {address}")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        print(f"Opening Hours: {opening_hours_text}")
        print(f"Contact Numbers: {', '.join(contact_numbers)}")
        print(f"Websites: {', '.join(websites)}")
        print("-" * 50)
else:
    print(f"Error: {response_dis.status_code}")


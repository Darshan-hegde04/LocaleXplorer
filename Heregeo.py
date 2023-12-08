import requests

class HereGeo:
    def __init__(self, api_key, latitude, longitude, query, limit):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.query = query
        self.limit = limit

    def get_reverse_geocode(self):
        url = f"https://revgeocode.search.hereapi.com/v1/revgeocode?at={self.latitude},{self.longitude}&apikey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            address = data["items"][0]["address"]
            street = address["label"]
            city = address["city"]
            postalCode = address["postalCode"]

            print("User location")
            print(city)
            print(postalCode)
            print(street)
            print("\n")
        else:
            print(f"Error: {response.status_code}")

    def get_discover(self):
        url = f"https://discover.search.hereapi.com/v1/discover?at={self.latitude},{self.longitude}&limit={self.limit}&q={self.query}&apikey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data_disco = response.json()

            print("Query result")
            for item in data_disco['items']:
                title = item['title']
                latitude = item['position']['lat']
                longitude = item['position']['lng']

                print(f"Title: {title}, Latitude: {latitude}, Longitude: {longitude}")
        else:
            print(f"Error: {response.status_code}")

# API key
api_key = "lgblBT4r0F8zXJn80OA7jV5uExXqfv2EySrCim1nViA"

# Coordinates
latitude = 12.98995222860768
longitude = 75.34099184798936

# Query location
query = "Restaurant"
limit = 10

# Create HereGeo instance
here_geo_instance = HereGeo(api_key, latitude, longitude, query,limit)

# Get reverse geocode
here_geo_instance.get_reverse_geocode()

# Get discover result
here_geo_instance.get_discover()
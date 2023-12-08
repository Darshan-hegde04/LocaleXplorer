import requests

user_query = "Cafe near bangalore"
nominatim_url = "https://nominatim.openstreetmap.org/search"
params = {
    "q":user_query,
    "format": "json",
    "limit": 10
}

response = requests.get(nominatim_url, params=params)
data = response.json()
print(data)

#For Displaying Latitude and Longatitude

for place in data:
    name = place.get("display_name", "N/A")
    lat = place.get("lat", "N/A")
    lon = place.get("lon", "N/A")

    print(f"Shop Name: {name}, Latitude: {lat}, Longitude: {lon}")
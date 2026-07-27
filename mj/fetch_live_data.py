import requests
import folium

def fetch_street_view_image(lat, lon, api_key, output_file="street_view.jpg"):
    url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "600x400",  # Image resolution
        "location": f"{lat},{lon}",
        "fov": 90,         # Field of view (default is 90)
        "heading": 0,      # Direction of the camera
        "pitch": 0,        # Tilt of the camera
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Street View image saved as {output_file}")
    else:
        print(f"Error: Unable to fetch Street View image. Status code: {response.status_code}")

# Example usage
api_key = "<YOUR_API_KEY>"  # Replace with your API key
lat, lon = 51.43136241297104, 5.483785233930436   # Replace with your coordinates
fetch_street_view_image(lat, lon, api_key)
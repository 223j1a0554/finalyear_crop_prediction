import requests
from math import radians,sin,cos,sqrt,atan2
def check_water_source(lat, lon):

    query = f"""
    [out:json][timeout:25];
    (
    way(around:6000,{lat},{lon})["natural"="water"];
    relation(around:6000,{lat},{lon})["natural"="water"];

    way(around:6000,{lat},{lon})["waterway"];
    relation(around:6000,{lat},{lon})["waterway"];

    way(around:6000,{lat},{lon})["landuse"="reservoir"];

    way(around:6000,{lat},{lon})["waterway"="river"];
    way(around:6000,{lat},{lon})["waterway"="stream"];
    way(around:6000,{lat},{lon})["waterway"="canal"];
    );
    out tags center;
    """

    url = "https://overpass-api.de/api/interpreter"

    try:
        response = requests.post(url, data=query, timeout=30)

        if response.status_code != 200:
            return "Moderate",None

        data = response.json()
        elements = data.get("elements", [])

        print("Water bodies detected:",len(elements))
        
        nearest_distance = None

        for el in elements:

            center = el.get("center")

            # If center exists
            if center:
                water_lat = center["lat"]
                water_lon = center["lon"]

            # If center not available, use geometry
            elif "geometry" in el and len(el["geometry"]) > 0:
                water_lat = el["geometry"][0]["lat"]
                water_lon = el["geometry"][0]["lon"]

            else:
                continue

            distance = calculate_distance(lat, lon, water_lat, water_lon)

            print("Distance to water:", distance)

            if nearest_distance is None or distance < nearest_distance:
                nearest_distance = distance
        if nearest_distance is not None:
            if nearest_distance < 2.0:
                return "Good", nearest_distance
            elif nearest_distance < 6.0:
                return "Moderate", nearest_distance
            else:
                return "Poor", nearest_distance
    except Exception as e:
        print("Water API error:", e)
        return "Moderate",None
    
def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2

    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = R * c

    return distance
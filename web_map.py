"""
https://www.pythonanywhere.com/user/anastasiiakernytska/web_map.py
"""

import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import twitter2
from random import randint
# import json


def get_json():
    return twitter2.get_json_friends()
    # with open('test.json', 'r') as file:
    #     return json.load(file)


def get_users_info_by(json_data):
    users_info = []
    try:
        for user in json_data['users']:
            users_info.append((
                user['screen_name'],
                user['location'],
            ))
    except KeyError:
        print('No user was found.')

    return users_info


def render_html():
    def get_cords(_place: str):
        """
        The function is named location and returns a tuple with location
        coordinates.
        If no coordinates are found for the full name of the location, then
        there is a narrower search for it
        Example: 'Melrose Lumber, Ossining, New York, USA' - not found, search
        for 'Ossining, New York, USA'
        """
        place_location = None
        geolocator = Nominatim(user_agent="user_agent")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)
        step_indexes = [0] + [i + 1 for i, ltr in enumerate(_place) if ltr == ',']

        for step in step_indexes:
            place_location = geolocator.geocode("{}".format(_place))
            if not place_location:
                _place = _place[step:]

        if place_location is None:
            return
        return place_location.latitude, place_location.longitude

    def randomize_color() -> str:
        colors = ['darkpurple', 'beige', 'purple', 'blue',
                  'lightgreen', 'lightred', 'white', 'red',
                  'lightgray', 'darkgreen', 'gray', 'darkred',
                  'orange', 'green', 'darkblue', 'pink', 'black',
                  'cadetblue', 'lightblue']
        return colors[randint(0, len(colors))]

    json_file = get_json()
    users = get_users_info_by(json_file)

    html_map = folium.Map()

    all_subs = folium.FeatureGroup(name="Friends' locations")

    for user in users:
        name = user[0]

        place = get_cords(user[1])

        all_subs.add_child(folium.Marker(
            location=place,
            popup=name,
            icon=folium.Icon(color=randomize_color())
        ))

    html_map.add_child(all_subs)

    folium.LayerControl(collapsed=False).add_to(html_map)
    html_map.save("templates/map.html")

import requests

from pprint import pprint


class WebService:
    def __init__(self, baseURL):
        self.baseURL = baseURL
        self.basicAuth = requests.auth.HTTPBasicAuth("andy", "testing")

    def locationExists(self, locationID):
        locations = self.locations()

        return len([x for x in locations if x['id'] == locationID]) != 0

    def locations(self):
        url = f"{self.baseURL}locations"

        response = requests.get(url, auth=self.basicAuth)
        if response:
            return response.json()["locations"]

        return None

    def addLocation(self, id, name, latitude, longitude, region_radius, temperature_scale, locale, country_code, timezone_id):
        location = {
            "id": id,
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "region_radius": region_radius,
            "temperature_scale": temperature_scale,
            "locale": locale,
            "country_code": country_code,
            "timezone_id": timezone_id,
        }

        response = requests.post(
            f"{self.baseURL}locations", auth=self.basicAuth, json=location)

        if response:
            return response.json()["location"]

        return None

    def roomExists(self, roomID):
        rooms = self.rooms()

        return len([x for x in rooms if x['id'] == roomID]) != 0

    def findRoomName(self, roomName):
        rooms = self.rooms()

        found = [x for x in rooms if x['name'] == roomName]

        if found:
            return found[0]

        return None

    def rooms(self):
        url = f"{self.baseURL}rooms"

        response = requests.get(url, auth=self.basicAuth)
        if response:
            return response.json()["rooms"]

        return None

    def addRoom(self, id, location_id, name, background_image):
        room = {
            "id": id,
            "location_id": location_id,
            "name": name,
            "background_image": background_image,
        }

        response = requests.post(
            f"{self.baseURL}rooms", auth=self.basicAuth, json=room)

        if response:
            return response.json()["room"]

        return None

    def addReading(self, room_id, ambient, set_point=None, humidity=None, state=None, away=None):
        reading = {
            "room_id": room_id,
            "set_point": set_point,
            "ambient": ambient,
            "humidity": humidity,
            "state": state,
            "away": away,
        }

        response = requests.post(
            f"{self.baseURL}readings", auth=self.basicAuth, json=reading)

        if response:
            return response.json()["reading"]

        return None

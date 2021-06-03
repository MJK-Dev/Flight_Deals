import requests
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

TEQUILA_KEY = os.getenv("TEQUILA_KEY")
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
FLY_FROM = "LON"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.tequila_headers = {
            "apikey": TEQUILA_KEY
        }


    def check_IATA_code(self, received_cities):
        self.cities = []
        self.not_found = []
        for city in received_cities:
            parameters={
                "term": city,
            }
            IATA_code_response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", params=parameters, headers=self.tequila_headers)
            IATA_code = IATA_code_response.json()
            pprint(IATA_code)
            pprint(len(IATA_code["locations"]))

            if not IATA_code["locations"] or IATA_code["locations"][0]["code"] == None:
                self.not_found.append(city.title())
            else:
                nr_loc = 0
                for location in IATA_code["locations"]:
                    try:
                        with_airports = location["airports"]
                    except KeyError:
                        nr_loc += 1
                    else:
                        city_code = IATA_code["locations"][nr_loc]["code"]
                        print(city_code)
                        break

                self.cities.append([city_code, city])

        print(self.not_found)
        print(self.cities)
        return self.cities


    def check_flights(self, city_from, city_to, max_price, date_from, date_to, min_days, max_days):

        parameters = {
            "fly_from": {city_from},
            "fly_to": f"city:{city_to}",
            "date_from": date_from,
            "date_to": date_to,
            "flight_type": "round",
            "price_to": max_price,
            "max_stopovers": 0,
            "nights_in_dst_from": min_days,
            "nights_in_dst_to": max_days,
            "curr": "EUR",
            "sort": "price",

        }

        IATA_code_response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=parameters, headers=self.tequila_headers)

        try:
            IATA_code = IATA_code_response.json()["data"][0]


        except IndexError or KeyError:
            parameters["max_stopovers"] = 3
            IATA_code_response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=parameters,
                                              headers=self.tequila_headers)
            try:
                IATA_code = IATA_code_response.json()["data"][0]

            except IndexError or KeyError:
                return False
            else:
                pprint(IATA_code)
                return IATA_code
        else:
            pprint(IATA_code)
            return IATA_code


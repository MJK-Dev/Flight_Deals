import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETY_KEY = os.getenv("SHEETY_KEY")
SHEETY_ENDPOINT = "https://api.sheety.co/1b7450ee2b31d06a6757fdf4064d6d72/flightDeals/prices"

class DataManager:
    def __init__(self):
        self.sheety_headers =  {
    "Authorization": SHEETY_KEY
}

    def check_IATAs(self):
        sheety_response = requests.get(url=SHEETY_ENDPOINT, headers=self.sheety_headers)
        result_sheety = sheety_response.json()["prices"]
        return result_sheety

    def replace_IATAs(self, code, id):
        new_data = {
            "price": {
                "iataCode": code
            }
        }
        sheety_response = requests.put(url=f"{SHEETY_ENDPOINT}/{id}", json=new_data, headers=self.sheety_headers)
        print(sheety_response.text)
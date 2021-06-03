from pprint import pprint
from datetime import datetime
from destination_info import DestinationInfo

di = DestinationInfo()

class FlightData:
    def __init__(self):

     self.deal_dict ={
         "city": "",
         "message": "",
     }
     self.destination = None
     self.price = None
     self.from_airport = None
     self.to_airport = None
     self.dept_date = None
     self.return_date = None
     self.return_from_airport = None
     self.return_to_airport = None
     self.number_stopovers = 0
     self.deep_link = None
     self.via_city =""

    def arrange_data(self, flight_data):

        arranged_data =[]
        for item in flight_data:
            if item[1] == False:
                new_item = {
                    "city": (item[0]).title(),
                    "price": 1000000,
                    "dept_date": False,
                }
                arranged_data.append(new_item)
            else:
                return_flight = 1
                self.number_stopovers = 0
                if len(item[1]["route"]) > 2:
                    return_flight = len(item[1]["route"]) - 1
                    self.number_stopovers = int((len(item[1]["route"]) / 2) - 1)
                    self.via_city = item[1]["route"][0]["cityTo"]

                self.price = item[1]["price"]
                self.from_airport = item[1]["route"][0]["flyFrom"]
                self.to_airport = item[1]["route"][self.number_stopovers]["flyTo"]
                self.dept_date = item[1]["route"][0]["local_departure"][:10]
                self.return_date = item[1]["route"][self.number_stopovers+1]["local_departure"][:10]
                self.return_from_airport = item[1]["route"][self.number_stopovers+1]["flyFrom"]
                self.return_to_airport = item[1]["route"][return_flight]["flyTo"]
                self.deep_link = item[1]["deep_link"]
                city = f"{item[0]} alert at €{self.price}!"
                message = f"Low price alert! Only €{self.price} from airport {self.from_airport}" \
                                            f" to {item[0]}-{self.to_airport}, from dates {self.dept_date}" \
                                            f" to {self.return_date}\n  Check the following link: " \
                                            f"https://www.google.co.uk/flights?hl=en#flt={self.from_airport}." \
                                            f"{self.to_airport}.{self.dept_date}*{self.return_from_airport}." \
                                            f"{self.return_to_airport}.{self.return_date}  "
                #if return_flight > 2:
                  #  message = message + f'Flight has {self.number_stopovers} stopovers via {self.via_city}'

             #   new_item_email = {
              #      "city": city,
              #      "message": message
              #  }
                new_item = {
                    "city": (item[0]).title(),
                    "price": self.price,
                    "from_airport": self.from_airport,
                    "to_airport": self.to_airport,
                    "dept_date": datetime.strptime(self.dept_date, "%Y-%m-%d").strftime("%d-%m-%y"),
                    "return_date": datetime.strptime(self.return_date, "%Y-%m-%d").strftime("%d-%m-%y"),
                    "total_days": (datetime.strptime(self.return_date, "%Y-%m-%d") - datetime.strptime(self.dept_date, "%Y-%m-%d")).days,
                    "return_from_airport": self.return_from_airport,
                    "return_to_airport": self.return_to_airport,
                    "number_stopovers": self.number_stopovers,
                    "via_city": self.via_city,
                    "deep_link": self.deep_link,
                    "deal_url":  f"https://www.google.co.uk/flights?hl=en#flt={self.from_airport}." \
                                            f"{self.to_airport}.{self.dept_date}*{self.return_from_airport}." \
                                            f"{self.return_to_airport}.{self.return_date}  ",
                    "wiki_url": di.get_wikipedia_link(item[0])
                }
                arranged_data.append(new_item)
        arranged_data = sorted(arranged_data, key = lambda i: i['price'])
        return arranged_data






class DestinationInfo:

    def __init__(self):
        pass

    def get_wikipedia_link(self, city):
        if len(city.split()) > 1:
            city = city.replace(" ", "_")
        return f"https://en.wikipedia.org/wiki/{city}"

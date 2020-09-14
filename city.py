import requests
from flask import Flask

class City:
    
    # initailize class and get json with city info
    def __init__(self, name):
        self.name = str(name).lower()
        self.response = requests.get(f'https://api.teleport.org/api/cities/?search={self.name}')
        self._json = self.response.json()
    
    # returns complete json object of city information
    def get(self):
        return self._json
    
    # return a list of possible cities
    def cityList(self):
        res = self._json['_embedded']['city:search-results']
        cities = list()

        for names in res:
            cities.append(names['matching_full_name'])

        return cities


app = Flask(__name__)

@app.route('/')
def hello():
    c = City("orlando")
    return str(c.cityList())

if __name__ == '__main__':
   app.run()

import requests, os
from flask import Flask, redirect, session, render_template, request, url_for

class City:
    
    # initialize class and get json with city info
    def __init__(self, name):
        self.name = str(name).lower()
        self.response = requests.get(f'https://api.teleport.org/api/cities/?search={self.name}')
        self._json = self.response.json()
    
    # returns complete json object of city information
    def get(self):
        return self._json
    
    # gets geotagID
    def id(self):
        data = self.get()
        data = data['_embedded']['city:search-results']

        if len(data) == 0:
            return

        data = data[0]['_links']['city:item']['href']
        return data

    # return a list of possible cities
    def cityList(self):
        res = self._json['_embedded']['city:search-results']
        cities = list()

        for names in res:
            cities.append(names['matching_full_name'])

        if len(cities) == 0:
            return "Error, no cities found"
        
        return cities[1:]
    
    def details(self):
        res = self._json['_embedded']['city:search-results']

        if len(res) == 0:
            return

        name = res[0]['matching_full_name']
        res = res[0]['_links']['city:item']['href']
        response = (requests.get(res)).json()

        coord = response['location']['latlon']
        population = 'Population: ' + str(response['population'])
        country = 'Country: ' + response['_links']['city:country']['name']
        timeZone = 'Time Zone: ' + response['_links']['city:timezone']['name'] + ' time'
        coordinates = 'Coordinates: ' + str((coord['latitude'], coord['longitude']))

        return [name, population, country, timeZone, coordinates]

    def ratings(self):
        data = self.id()
        data = requests.get(data)
        data = data.json()['_links']['city:urban_area']['href']

        req = requests.get(data).json()
        # categories = req['categories']
        print(data)

    def bundle(self):
        data = [self.details(), self.cityList()]
        return data

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        city = request.form['information']
        newCity = City(str(city))
        session['data'] = newCity.bundle()
        return redirect(url_for('cities'))
    else:
        return render_template('index.html')

@app.route("/city")
def cities():
    data = session.get('data', None)
    return render_template('city.html', data=data)

app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(processes=1, debug=True)
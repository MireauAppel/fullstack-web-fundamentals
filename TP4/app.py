from flask import Flask, request, render_template
from urllib.parse import unquote_plus, quote
import requests

app = Flask(__name__)

messages_db = ["Bienvenue sur le chat !", "Test de message"]

def gen_html(messages):
    html = "<h1>Chat Minimaliste</h1><ul>"
    for msg in messages:
        html += f"<li>{msg}</li>"
    html += "</ul>"
    return html


def add_message(messages, text):
    messages.append(text)


def remove_message(messages, index):
    if 0 <= index < len(messages):
        messages.pop(index)


@app.route('/', methods=['GET'])
def index():
   
    return gen_html(messages_db)

@app.route('/<message>', methods=['POST'])
def post_msg(message):
    
    decoded = unquote_plus(message)
    add_message(messages_db, decoded)
    return f"Message ajouté : {decoded}", 201

@app.route('/<int:indice>', methods=['DELETE'])
def delete_msg(indice):
    
    remove_message(messages_db, indice)
    return f"Message à l'indice {indice} supprimé", 200


#partie 3
API_KEY = "eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJtaXIuYXBsQGNhcmJvbi5zdXBlciIsImFwcGxpY2F0aW9uIjp7Im93bmVyIjoibWlyLmFwbCIsInRpZXJRdW90YVR5cGUiOm51bGwsInRpZXIiOiJVbmxpbWl0ZWQiLCJuYW1lIjoiRGVmYXVsdEFwcGxpY2F0aW9uIiwiaWQiOjM3MzEwLCJ1dWlkIjoiNmFiOWJhYTEtMGM0Ni00N2M3LTljMDUtOTJkOTgzM2Q3OWQzIn0sImlzcyI6Imh0dHBzOlwvXC9wb3J0YWlsLWFwaS5tZXRlb2ZyYW5jZS5mcjo0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyI1MFBlck1pbiI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0Ijoic2VjIn19LCJrZXl0eXBlIjoiUFJPRFVDVElPTiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6IkRvbm5lZXNQdWJsaXF1ZXNPYnNlcnZhdGlvbiIsImNvbnRleHQiOiJcL3B1YmxpY1wvRFBPYnNcL3YxIiwicHVibGlzaGVyIjoiYmFzdGllbmciLCJ2ZXJzaW9uIjoidjEiLCJzdWJzY3JpcHRpb25UaWVyIjoiNTBQZXJNaW4ifV0sImV4cCI6MTc3MTUzMjg5NywidG9rZW5fdHlwZSI6ImFwaUtleSIsImlhdCI6MTc3MTQ0NjQ5NywianRpIjoiYjE4MDc0ODgtMzI3ZC00MmYwLThkMmUtN2IzM2ZiNGQ2MmJlIn0=.Lddw4lhY5iPsw8Jbsv4ymX9lRvtyn30_egQM_vbBUktdtFM3fzGae0dVNnOczrhL7hLlIPdSeLr0CC2LrDyL4mIBlGz6SIjIuSvCF0qDg3PW3UvXC0dz5kmb80KyA9Vuwpuad1nBKKxDPC88Tz5Qkb8wLRwDj0I8KThHqz9LHAq-EHpr_MhtZth7QScUXpOhO5E1HDvsDG6iIEgeRVOH6ixfQJ5IIzcvJz4wJUu22aukSMIsZ4nI1wp7VBVjRh_rekMa-egSAdjSaBKcuvFoEUqUQXDJrglzgwbZaPL_a2gbBQLLNlNR3GvAcs7SXr__d1WQhqMdbmxWOmOpKiFLCQ=="
ENCODED_API_KEY = quote(API_KEY)
def get_station_list():
    url = f"https://public-api.meteofrance.fr/public/DPObs/v1/liste-stations?apikey={ENCODED_API_KEY}"
    response = requests.get(url)
    stations = []
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines[1:]:
            if line.strip():
                parts = line.split(';')
                if len(parts) > 1:
                    stations.append(parts[1])
    return stations

#def get_weather_data(city_name):
    #return {
     #   "city": city_name,
      #  "wind": "0.9",
       # "temp": "9.3",
        #""rain": "0"
    #}
def get_weather_data(city_name):
    print(f"\n--- RECHERCHE POUR : {city_name} ---")
    
    url_stations = f"https://public-api.meteofrance.fr/public/DPObs/v1/liste-stations?apikey={ENCODED_API_KEY}"
    resp_stations = requests.get(url_stations)

    
    station_id = None
    if resp_stations.status_code == 200:
        lines = resp_stations.text.split('\n')
        for line in lines[1:]:
            if line.strip() and city_name in line:
                station_id = line.split(';')[0]
                break
    if not station_id:
        return None

    url_weather = f"https://public-api.meteofrance.fr/public/DPObs/v1/station/horaire?id_station={station_id}&apikey={ENCODED_API_KEY}&format=json"
    
    resp_weather = requests.get(url_weather)
    
    if resp_weather.status_code == 200:
        data = resp_weather.json()
        if isinstance(data, list) and len(data) > 0:
           
            latest = data[0]
    
            
            # Conversion kelvin en celcius d'aprés la toute dernière documentation de meteofrance
            temp_k = latest.get('t')
            temp_c = round(temp_k - 273.15, 1) if temp_k is not None else "N/A"
            
            return {
                "city": city_name,
                "wind": latest.get('ff', 'N/A'),
                "temp": temp_c,
                "rain": latest.get('rr1', 'N/A')
            }
        
    return None

@app.route('/meteo', methods=['GET'])
def meteo_index():
    try:
        city = request.args['city']
    except KeyError:
        city = None

    stations = get_station_list()
    weather_info = None
    
    if city:
        weather_info = get_weather_data(city.upper())
        
    return render_template('weather.html', stations=stations, weather=weather_info)

@app.route('/meteo/<city>')
def weather_by_url(city):
    city_upper = city.upper()
    weather_info = get_weather_data(city_upper)
    stations = get_station_list()
    
    return render_template('weather.html', stations=stations, weather=weather_info)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

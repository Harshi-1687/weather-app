from flask import Flask,render_template,request
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY=os.getenv("WEATHER_API_KEY")

@app.route('/',methods=['GET','POST'])
def home():
    weather={}
    if request.method=='POST':
        city=request.form['city']
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        if response.status_code==200:
            data = response.json()
            weather = {
                'city': city,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 'N/A'),
                'pressure': data['main']['pressure'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
            }
            lat = data['coord']['lat']
            lon = data['coord']['lon']
            onecall_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
            oc_response = requests.get(onecall_url)
            if oc_response.status_code == 200:
                oc_data = oc_response.json()
                weather['uv_index'] = oc_data['current']['uvi']
                aqi_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
                aqi_response = requests.get(aqi_url)
                if aqi_response.status_code == 200:
                    aqi_data = aqi_response.json()
                    weather['aqi'] = aqi_data['list'][0]['main']['aqi']
                else:
                    weather['aqi'] = 'N/A'
            else:
                weather['uv_index'] = 'N/A'
                weather['aqi'] = 'N/A'   
        else:
            weather={'error':'city not found'}
    return render_template('index.html',weather=weather)

if __name__=='__main__':
    app.run(debug=True)
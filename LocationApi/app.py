# """ module containing an api endpoint that response only to a get request,
# it utilizes the `requests` library for making requests to other third party
# api endpoints 
# """

# import requests
# from flask import Flask, request, jsonify

# app = Flask(__name__)


# @app.route('/api/hello', methods=['GET'])
# def visitor_info():
# 	"""View for handling the request including a querry parameter
# 	"""

# 	client_ip = request.headers.get('X-Requested-For')
# 	if client_ip:
# 		client_ip = client_ip.split(',')[0]

# 	if not client_ip:
# 		client_ip = request.headers.get('X-Forwarded-For')
# 		if client_ip:
# 			client_ip = client_ip.split(',')[0]

# 	if not client_ip:
# 		client_ip = request.remote_addr
	
# 	location_api_url = 'http://ip-api.com/json/' + str(client_ip)
# 	location_response =  requests.get(location_api_url)
# 	if location_response.status_code == 200:
# 		location_data = location_response.json()
# 	else:
# 		return jsonify({"error": "your city was not loaded successfully"})

# 	location = location_data.get('city') 

# 	visitor_name = request.args.get('visitor_name', 'visitor')
	

# 	weather_api_url = f'http://api.weatherapi.com/v1/current.json?key=31d8e3e2f00a4cd1be0135729240107&q={location}'
# 	weather_response = requests.get(weather_api_url) 
# 	if weather_response.status_code == 200:
# 		weather_data = weather_response.json()
# 		temperature = weather_data.get('current')['temp_c']

# 	greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees celcius in {location}'
	

# 	return jsonify({'client_ip': client_ip,
# 			'location': location,
# 			'greeting': greeting
# 	})

# if __name__ == '__main__':
# 	app.run() 


import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def visitor_info():
    """View for handling the request including a query parameter"""
    
    client_ip = request.headers.get('X-Requested-For')
    if client_ip:
        client_ip = client_ip.split(',')[0]

    if not client_ip:
        client_ip = request.headers.get('X-Forwarded-For')
        if client_ip:
            client_ip = client_ip.split(',')[0]

    if not client_ip:
        client_ip = request.remote_addr
    location_api_url = f'https://ipapi.co/{client_ip}/json'
    location_response = requests.get(location_api_url)
    if location_response.status_code == 200:
        location_data = location_response.json()
    else:
        return jsonify({"error": "Your city was not loaded successfully"})

    location = location_data.get('city')
    
    if not location:
        return jsonify({"error": "Location not found"})

    visitor_name = request.args.get('visitor_name', 'Guest')

    weather_api_url = f'http://api.weatherapi.com/v1/current.json?key=31d8e3e2f00a4cd1be0135729240107&q={location}'
    weather_response = requests.get(weather_api_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        temperature = weather_data.get('current', {}).get('temp_c')
    else:
        return jsonify({"error": "Weather data information could not be loaded"})

    if temperature is None:
        return jsonify({"error": "Temperature data is not available"})

    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}'
    response = {
        'client_ip': client_ip,
        'location': location,
        'greeting': greeting
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()
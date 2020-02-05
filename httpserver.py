from flask import Flask
from flask import request
import json
import requests

def consultaroom(auth,roomId):
	url = "https://api.ciscospark.com/v1/messages?roomId="+roomId+"&max=1"
	payload = {}
	headers = {
		'Authorization': 'Bearer '+auth
	}

	response = requests.request("GET", url, headers=headers, data = payload)

	return(response.text.encode('utf8'))

def enviarunmensaje(auth,text,roomId):

	url = "https://api.ciscospark.com/v1/messages"

	payload = "{\n\t\"roomId\": \""+roomId+"\", \n\t\"text\": \""+text+"\"\n}"
	headers = {
	  'Authorization': 'Bearer ' +auth,
	  'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data = payload)

	return(response.text.encode('utf8'))

def consultadolar():

	url = "https://api.sbif.cl/api-sbifv3/recursos_api/dolar?apikey=63e26f6c5e9de115ba0c51dfe2dd1743609bcb69&formato=xml"

	payload = {}
	headers= {}

	response = requests.request("GET", url, headers=headers, data = payload)

	respuesta = response.text
	respuesta2 = respuesta.split('<Valor>')[1]
	respuesta2 = respuesta2.split('</Valor>')[0]
	return(respuesta2)


Authkey = "YTZjMTM2ZjUtNGE0ZC00NjY5LWE5NTQtM2I1OWM4ZmY5NWExZGUxNDVkMGQtNjFi_PF84_15138b39-24fd-48f5-9e28-e9d3db4c9b40"

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/test')
def test():
	return 'Esta es una ruta de prueba'

@app.route('/events', methods = ['GET', 'POST'])
def events():
	if request.method == 'GET':
		return 'Hola'
	if request.method == 'POST':
		data = json.loads(request.data)
		roomId = data['data']['roomId']
		personId = data['data']['personId']
		if personId != "Y2lzY29zcGFyazovL3VzL1BFT1BMRS83NmUzOTI4NC1kNGU1LTRlOWItOTE4Yi1mMTUzMTJhYzU2MjM":


			dataroom = json.loads(consultaroom(Authkey, roomId))
			message = dataroom['items'][0]['text']

			if message == "dolar":
				dolar = consultadolar()
				text = "El valor del dolar es $"+dolar + " pesos chilenos"
			else:
				text = "Por favor introduzca la palabra dolar para obtener resultados"
			

			enviarunmensaje(Authkey,text,roomId)
		return "ok"
	else:
		return "error"

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=3000)
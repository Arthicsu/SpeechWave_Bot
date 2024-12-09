import requests

url = "https://smartspeech.sber.ru/rest/v1/text:synthesizeе"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer MWM2M2FkNTUtYjI4NC00MjEwLTkwNzctYWRiNTE1YTVlNDliOjQwZDM4OWQ1LWY4MTQtNDFhZC04OGZmLTMwOTBmYTE0MjE2OA=='
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)
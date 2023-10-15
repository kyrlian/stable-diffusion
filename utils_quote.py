import requests

url="https://zenquotes.io/api/random"

def getquote(): 
    response = requests.get(url)
    # print(f"status code: {response.status_code}")
    json=response.json()
    # print(f"json: {json[0]}")
    quote=json[0]['q']
    # print(f"q: {quote}")
    return quote
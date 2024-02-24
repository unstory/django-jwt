import requests

url = "http://127.0.0.1:8000/api/token/"

data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(url, data=data)
print(response.status_code)

import requests
urls = ['http://qpaca_publisher_1:8000/publish/' for i in range(1000)]

for u in urls:
    requests.post(u, json={"payload": "Ola Mundo!"})

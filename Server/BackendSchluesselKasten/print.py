from signal import pause
from gpiozero import Button, LED
import requests

token_url = "https://127.0.0.1/api/get-Token/"
token_data = {"username": "Aus Sicherheitsgründen verändert",
              "password": "Aus Sicherheitsgründen verändert"}
r = requests.post(token_url, json=token_data, verify=False)
token = r.json()["token"]
print(token)


def request_print():
    print_url = "https://127.0.0.1/api/print"
    auth = {"Authorization": f"Token {token}"}
    r = requests.get(print_url, headers=auth, verify=False)
    print(r.text)


pin = 4  # set pin
button = Button(pin)
button.when_pressed = request_print
led = LED(17)
led.source = button
pause()

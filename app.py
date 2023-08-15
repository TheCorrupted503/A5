from flask import Flask, render_template, redirect, request
import socket
import requests
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def home_page():       
    return render_template('index.html')

@app.route('/details', methods=['POST'])
def server_program():
    if request.method == "POST":
        if request.form.get("Create"):
            city = request.form["cityName"]
            if city == "null":
                return render_template('index.html')
            else:
                valid_input = True
                while valid_input == True:

                    HEADER = 256
                    PORT = 1234
                    FORMAT = 'utf-8'
                    SERVER = "192.168.1.101"
                    ADDR = (SERVER, PORT)

                    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    c.connect(ADDR)

                    userAgents = [
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
                        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
                        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
                        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)' 
                    ]

                    msg = city

                    if msg:
                        message = msg.encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        c.send(send_length)
                        c.send(message)
                        data = c.recv(2048).decode(FORMAT)
                        print("Data has been sent to microservice\n")
                        print("Data received from microservice:")
                        print(data + '\n')
                        data_request = requests.get(data, headers={'User-Agent':random.choice(userAgents)})
                        soup = BeautifulSoup(data_request.content, "html.parser")
                        gas_station = soup.find('h3', class_ = "header__header3___1b1oq header__header___1zII0 header__midnight___1tdCQ header__snug___lRSNK StationDisplay-module__stationNameHeader___1A2q8")
                        location = soup.find('div', class_ = "StationDisplay-module__address___2_c7v")
                        price = soup.find('span', class_ = "text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL")
                        logo = soup.find('img', class_ = "image__image___1ZUby")
                        logo_value = logo.get('src')
                        gas_station_value = gas_station.get_text()
                        line_array = []
                        for line in location:
                            line_array.append(line.get_text())
                        address_line_one = line_array[0]
                        address_line_two = line_array[2]
                        price_value = price.get_text()
                        address_value = address_line_one + ' ' + address_line_two
                        print(gas_station_value)
                        print(address_value)
                        print(price_value)
                        print(logo_value)
                        return render_template('details.html', gas_station_value = gas_station_value, address_value = address_value, price_value = price_value, logo_value = logo_value)
if __name__ == "__main__":
    app.run(port=12345, debug=True)
    
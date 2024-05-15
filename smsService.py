# Citations:
# https://www.alfredosequeida.com/blog/how-to-send-text-messages-for-free-using-python-use-python-to-send-text-messages-via-email/ 

import email, smtplib, ssl
from providers import PROVIDERS
from env import ENV, openweather_key
import time
import json
import requests

def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple,
    subject: str = "sent using etext",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'

    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)

def main():
    message = None
    message_sent = False
    sender_credentials = ("smsmicroservice@gmail.com", ENV[0])

    info = {
        0: [],   # city
        1: [],   # latitude
        2: [],   # longitude
        3: [],   # pollen
        4: [],   # air quality
        5: [],   # forecast
        6: [],   # solar
        7: [],   # number
        8: []    # provider
    }


    counter = 0

    while message_sent is False:
        print('----READING DATA-----')
        with open('website\static\smsService.txt', 'r') as f:
            read_data = f.read()
            
            word = ''
            for char in read_data:
                if char == '#':
                    info[counter].append(word)
                    word = ''
                    counter += 1
                elif char == '*':   # End of user
                    info[counter].append(word)
                    word = ''
                    counter = 0
                else:
                    word += char
        
        city = info[0].copy()
        lat = info[1].copy()
        long = info[2].copy()
        pollen = info[3].copy()
        air_quality = info[4].copy()
        forecast = info[5].copy()
        solar = info[6].copy()
        numbers = info[7].copy()
        providers = info[8].copy()
        
        for i in range(len(city)):
            message = ''
            message += city[i]
            message += '\n'
            if pollen[i] != 'None':
                message += 'Pollen'
                message += '\n'
            if air_quality[i] != 'None':
                message += 'Air Quality'
                message += '\n'
            if forecast[i] != 'None':
                message += 'Forecast'
                message += '\n'
            if solar[i] != 'None':
                message += 'Solar'
                message += '\n'

            message = ''
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + openweather_key[0] + "&q=" + city[i]
            response = requests.get(complete_url)
            response_json = response.json()
            if response_json['cod'] != '404':
                y = response_json['main']
                z = response_json['weather']
                message += z[0]['description']
                message += '\n'
                current_temp = y['temp']
                current_temp = round((int(current_temp) - 273.15) * 9/5 + 32, 1)
                message += str(current_temp)
                message += ' F'
            
            print(message)
            send_sms_via_email(numbers[i], message, providers[i], sender_credentials)
            print('Message Sent!')
            message_sent = True

    
            
            time.sleep(.5)
        
        time.sleep(2)

if __name__ == "__main__":
    main()
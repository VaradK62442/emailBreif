# email brief
# send an email using smtp to specified user
# containing brief content

import smtplib
import ssl
from email.message import EmailMessage

import requests
import geocoder
from bdayData import get_pages
from datetime import *

def get_date():
    today = date.today()

    # format today's date
    today_formatted = today.strftime('%a %d %b %Y')
    result_str = f'Today is {today_formatted}.\n'

    return str(today), result_str


def get_birthdays(date, max_lim):
    # get all birthdays, sort manually
    # since sorting by days left is not working (?)
    birthdays = get_pages()
    result_str = f'Showing {max_lim} upcoming birthdays:\n'
    i = 0

    for person in birthdays:
        # check if person has upcoming birthday
        if person.bday_this_year >= date and i <= max_lim:
            # calculate days left
            today = datetime.strptime(date, "%Y-%m-%d")
            person_bday = datetime.strptime(person.bday_this_year, "%Y-%m-%d")
            diff = person_bday - today
            days_left = diff.days
            if days_left == 0:
                result_str += f"""> {person.name} has a birthday today, on {datetime.strptime(person.bday_this_year, "%Y-%m-%d").strftime('%d %b')}.\n"""
            else:
                result_str += f"""> {person.name} has a birthday on {datetime.strptime(person.bday_this_year, "%Y-%m-%d").strftime('%d %b')} with {days_left} days left.\n"""
            i += 1

    return result_str


def get_weather(date):
    result_str = ''
    API_KEY = "api key"
    g = geocoder.ip('me')
    lat, lon = g.latlng

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

    # send request
    res = requests.get(url)
    data = res.json()

    # extract data from json
    wind = round(data['wind']['speed'] * 2.237, 2) # convert m/s to mi/h
    main = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temp = round(data['main']['temp'], 2)
    temp_min = round(data['main']['temp_min'], 2)
    temp_max = round(data['main']['temp_max'], 2)
    city_name = data['name']

    result_str += f'''Weather forecast for {city_name} on {date}:\n> Weather: {main} - {description}\n> Temperature: {temp_min}°C - {temp}°C - {temp_max}°C\n> Winds: {wind} mph'''

    return result_str


def compile_body(date_result, bday_result, weather_result):
    body = 'Here is your daily brief:\n'

    body += date_result + '\n'
    body += bday_result + '\n'
    body += weather_result

    return body


def send_email(date, body):

    email_sender = 'sender@gmail.com'
    email_password = 'password'
    email_receiver = 'reciever@gmail.com'

    subject = 'Daily email: ' + date

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def main():
    date, date_result = get_date()
    bday_result = get_birthdays(date, 7)
    weather_result = get_weather(date)

    body = compile_body(date_result, bday_result, weather_result)
    # print(body)

    send_email(date, body)


if __name__ == "__main__":
    main()
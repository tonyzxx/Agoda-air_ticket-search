import time
import smtplib
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from email.mime.text import MIMEText

# define travel info
departure = 'TPE'
arrival = 'OKA'
depart_date = '2020-05-01'
return_date = '2020-05-06'
target_airline = 'EVA Air'

# define agoda web info
search_url = 'https://www.agoda.com/zh-tw/flights/results?cid=1804069&departureFrom={}&departureFromType=1&arrivalTo={}&arrivalToType=1&departDate={}&returnDate={}&adults=2&searchType=2&cabinType=Economy'.format(
    departure,
    arrival,
    depart_date,
    return_date
)

user = 'xxxxxxx@gmail.com'
price_threshold = 8000

def main():
    airline, lowest_price = get_price_info(search_url)
    isSend = check_price(airline, lowest_price, target_airline, price_threshold)

    if isSend is True:
        msg_text = edit_msg(airline, lowest_price)
        send_mail(msg_text, user)

def get_price_info(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    airline = []
    for i, agency in enumerate(soup.select('.FlightIcon__Name')):
        if i % 2 == 1:
            airline.append(agency.text)

    lowest_price = []
    for price in soup.select('.FlightPrice__Amount--OuterDisplay'):
        lowest_price.append(price.text)

    return airline, lowest_price

def check_price(airline, lowest_price, target_airline, threshold):
    dic = {
        "airline": airline,
        "price":lowest_price
    }
    df = pd.DataFrame(dic)

    for i in df[df['airline'] == target_airline].price:
        if int(i.replace(',', '')) < threshold:
            return True

def edit_msg(airline, lowest_price):
    msg_text = """
    Airline             price
    --------------------------
    """

    for al, p in zip(airline, lowest_price):
        t = al + " " * (20-len(al)) + p + '\n'
        msg_text += t
    
    return msg_text

def send_mail(msg_text, user):
    gmail_user = 'xxxxxx@gmail.com'
    gmail_password = 'xxxxxxxx'

    msg = MIMEText(msg_text)
    msg['Subject'] = '機票價格'
    msg['From'] = gmail_user
    msg['To'] = user

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    main()

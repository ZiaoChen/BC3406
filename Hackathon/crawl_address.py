import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv


def get_postal_code(url):
    postal = "000000"
    try:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        address = soup.find('address')

        if address:
            try:
                if 'singapore' in str(address):
                    postal = str(address).split('singapore ')[1][:6]
                else:
                    postal = str(address).split('Singapore ')[1][:6]
                # postal = a[a.index("Singapore")-1].split(" ")[-1]
                print(postal)
            except:
                print("Cannot get postal code from %s" % str(address))
    except:
        print("Connection Error")
        pass
    return postal


with open('customer_address.csv', 'wb') as file:
    writer = csv.DictWriter(file, fieldnames=["email", "postal code"])
    writer.writeheader()
    data = pd.read_csv('temp2.csv')
    cust_address_dict = {}
    for i in range(data.shape[0]):
        email = data.iloc[i, :]['email']

        if email not in cust_address_dict and not pd.isnull(data.iloc[i, :]['abandoned_checkout_url']):
            print(data.iloc[i, :]['abandoned_checkout_url'])
            print(email)
            postal = get_postal_code(data.iloc[i, :]['abandoned_checkout_url'])
            if postal != "000000":
                cust_address_dict[email] = postal
                writer.writerow({'email': email, 'postal code': postal})
                file.flush()

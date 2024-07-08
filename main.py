import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

Product_name = []
Product_price = []
Product_description = []
Product_review = []
Product_link = []


for i in range(2, 12):
    url = "https://www.flipkart.com/search?q=mobile+under+20000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+ str(i)


    r = requests.get(url)

    soup = bs(r.text, "lxml")

    box = soup.find("div", class_="DOjaWF gdgoEp")
    if box:
        names = box.find_all("div", class_ = "KzDlHZ")
        prices = box.find_all("div", class_ = "Nx9bqj _4b5DiR")
        desc = box.find_all("ul", class_="G4BRas")
        reviews = box.find_all("div", class_="XQDdHH")
        links = box.find_all("a", class_="CGtC98")

        for i in names:
            name = i.text
            Product_name.append(name)


        for i in prices:
            price = i.text
            Product_price.append(price)


        for i in desc:
            description = i.text
            Product_description.append(description)


        for i in reviews:
            review = i.text
            Product_review.append(review)


        for i in links:
            link = i.get("href")
            Product_link.append("https://www.flipkart.com" + link)
    else:
        print("Data not found")



df = pd.DataFrame({"Product Name": Product_name, "Prices": Product_price, "Description": Product_description, "Reviews": Product_review, "Product Link": Product_link})
print(df)

df.to_csv("flipkart.csv", index=False)



# Entry program 


import winsound
import os
import re
import time
from num2words import num2words

def generate_sound(inp):
    if inp == 1:
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 5000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
    elif inp == 2:
        beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
        beep(3)


def check_fk_price(url, amount):

    request = requests.get(url)
    soup = bs(request.content,'html.parser')

    product_name = soup.find("span", {"class":"B_NuCI"})
    if product_name:
        product_name = product_name.get_text()
    else:
        product_name = "Product name not found"

    price = soup.find("div", {"class":"_30jeq3 _16Jk6d"})
    if price:
        price_text = price.get_text()
        if re.search(r'₹', price_text):
            price_text = re.sub(r'₹', '', price_text)
        if re.search(r',', price_text):
            prince_int = int(price_text.replace(',', ''))
        elif re.search(' crore', price_text):
            prince_int = int(num2words(int(re.search(r'\d+', price_text).group(0).replace(' crore', '')))[:-5])
        elif re.search(' lakh', price_text):
            prince_int = int(num2words(int(re.search(r'\d+', price_text).group(0).replace(' lakh', ''))[:-4]))
        else:
            prince_int = int(re.findall(r'\d+', price_text)[0])
    else:
        prince_int = 0
        

    if product_name and price:
        print(product_name + " is at " + str(price))
    else:
        print("Either product name or price was not found")
    if prince_int < amount:
        print("Book Quickly")
        generate_sound(1)
    else:
        print("No Slots found")



def main():
    URL = "https://www.flipkart.com/apple-macbook-air-m1-8-gb-256-gb-ssd-mac-os-big-sur-mgn93hn-a/p/itmb53580bb51a7e?pid=COMFXEKMXWUMGPHW&lid=LSTCOMFXEKMXWUMGPHW40HAM7&marketplace=FLIPKART&q=macbook+air+m1&store=search.flipkart.com&srno=s_1_3&otracker=AS_Query_HistoryAutoSuggest_1_7_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_7_na_na_na&fm=SEARCH&iid=cf486f4b-8d24-4747-8fa5-4b17cb4b3a7b.COMFXEKMXWUMGPHW.SEARCH&ppt=hp&ppn=homepage&ssid=npbt1mddr40000001622911909542&qH=be9862f704979d6e"
    while True:
        check_fk_price(URL, 90000)
        time.sleep(3600)

if __name__ == "__main__":
    main()

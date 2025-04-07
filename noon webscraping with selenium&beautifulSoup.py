import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv

user_input = 'smart watch'
url = f"https://www.noon.com/uae-en/search/?q={user_input.replace(' ', '%20')}"

product_details = []

def noon(link):
    try:
        # إعداد المتصفح
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)

        browser.get(link)

        # جلب المنتجات
        product_list = browser.find_elements('class name', 'productContainer')

        for product in product_list:
            html_code = product.get_attribute('outerHTML')
            soup = BeautifulSoup(html_code, 'html.parser')

            # استخراج اسم المنتج
            try:
                product_name = soup.find('div', {'class': 'ProductDetailsSection_title__JorAV'}).text
            except:
                product_name = "No product name found"

            # استخراج السعر
            try:
                product_price = soup.find('strong', {'class': 'Price_amount__2sXa7'}).text
            except:
                product_price = "No product price found"

            # استخراج الخصم
            try:
                product_discount = soup.find('span', {'class': 'PriceDiscount_discount__1ViHb PriceDiscount_pBox__eWMKb'}).text
            except:
                product_discount = "No discount found"

            # التقييم
            try:
                product_rate = soup.find('div', {'class': 'RatingPreviewStar_textCtr__sfsJG'}).text
            except:
                product_rate = "No product rate found"

            # رابط المنتج
            try:
                product_link = soup.find("a").get('href')
            except:
                product_link = "No link found"

            # حفظ التفاصيل
            product_details.append({
                'product_name': product_name,
                'product_price': product_price,
                'product_discount': product_discount,
                'product_rate': product_rate,
                'product_link': f"https://www.noon.com{product_link}" if "http" not in product_link else product_link,
            })

        browser.quit()

    except Exception as e:
        print(f"Something went wrong with noon: {e}")

# تشغيل الدالة
noon(url)

with open('noon_products.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['product_name', 'product_price', 'product_discount', 'product_rate', 'product_link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for product in product_details:
        writer.writerow(product)

print("Data saved to 'noon_products.csv'")
import os

print("File will be saved to:", os.path.abspath("noon_products.csv"))

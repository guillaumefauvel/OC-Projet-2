import requests
from bs4 import BeautifulSoup
import csv


product_page_url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
reponse_book = requests.get(product_page_url)
page = reponse_book
soup = BeautifulSoup(page.content, "html.parser")

table = []
# 'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)',
# 'Tax', 'Availability', 'Number of reviews'
for i in soup.find_all("td"):
    table.extend(i)

liste_title = [(soup.find("li", {"class": "active"})).text]
product_description = (soup.find("meta", {"name": "description"})['content']).replace("    ", "")
liste_product_description = [product_description]
liste_category = [soup.find("ul", "breadcrumb").find_next("a").find_next("a").find_next("a").text]
liste_image_url = ["https://books.toscrape.com" +
                   (((soup.find("div", {"class": "item active"})).find("img")["src"]).replace("../..", ""))]
liste_upc = [str(table[0])]
liste_price_including_tax = [str(table[3])]
liste_price_excluding_tax = [str(table[2])]
liste_number_available = [str(table[5])]
liste_review = [str(table[6])]
liste_url = [product_page_url]

en_tete = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
           'number_available', 'product_description', 'category', 'review_rating', 'image_url']

with open('DataSetOneBook.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(en_tete)
    for liste_url, liste_upc, liste_title, liste_price_including_tax, liste_price_excluding_tax, \
        liste_number_available, liste_product_description, liste_category, liste_review, liste_image_url \
            in zip(liste_url, liste_upc, liste_title, liste_price_including_tax, liste_price_excluding_tax,
                   liste_number_available, liste_product_description, liste_category, liste_review, liste_image_url):
        writer.writerow([liste_url, liste_upc, liste_title, liste_price_including_tax, liste_price_excluding_tax,
                         liste_number_available, liste_product_description,
                         liste_category, liste_review, liste_image_url])

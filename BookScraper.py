import requests
from bs4 import BeautifulSoup
import csv
import shutil
import os


def souper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        return "La requête a échoué."


def makemydir(whatever):
    try:
        os.makedirs(whatever)
    except OSError:
        pass
    os.chdir(whatever)


# Initialisation du dossier d'export
makemydir("Output")
my_cwd = os.getcwd()

soup_main = souper("https://books.toscrape.com")
searched_category = soup_main.find('ul', class_="nav nav-list")
category_dict = {}

for link in searched_category.find_all('a', href=True):

    category_name = link.text.strip()
    category_dict[category_name] = ("https://books.toscrape.com/" + link['href'])

for category in category_dict:

    if category == "Books":
        pass
    else:
        makemydir(category)

        soup_category = souper(category_dict[category])
        links_books = []
        # Vérifier s'il y a plusieurs pages ou s'il n'y en a qu'une seule
        try:
            pagination = (soup_category.find("li", {"class": "current"})).text.strip()
            num_of_page = pagination[-2:].strip()
        except AttributeError:
            num_of_page = 1

        for i in range(int(num_of_page)):
            links = soup_category.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

            for link in links:
                a = "https://books.toscrape.com/catalogue"+(link.find('h3')).find("a")["href"].replace("../../..", "")
                links_books.append(a)

            lst_title = []
            lst_description = []
            lst_category = []
            lst_image_url = []
            lst_upc = []
            lst_price_including_tax = []
            lst_price_excluding_tax = []
            lst_number_available = []
            lst_review = []
            lst_url = []

        # Récupération des valeurs propres à chaque livre
        for link in links_books:

            soup_book = souper(link)
            table = []

            # 'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)',
            # 'Tax', 'Availability', 'Number of reviews'
            for value in soup_book.find_all("td"):
                table.extend(value)

            lst_title.append((soup_book.find("li", {"class": "active"})).text)
            lst_description.append((soup_book.find("meta", {"name": "description"})['content']).replace("    ", ""))
            lst_category.append(soup_book.find("ul", "breadcrumb").find_next("a").find_next("a").find_next("a").text)
            lst_image_url.append(str("https://books.toscrape.com" + (((soup_book.find("div", {"class": "item active"}))
                                 .find("img")["src"]).replace("../..", ""))))
            lst_upc.append((table[0]))
            lst_price_including_tax.append((str(table[3])).replace("Â", ""))
            lst_price_excluding_tax.append((str(table[2])).replace("Â", ""))
            lst_number_available.append(str(table[5]))
            lst_review.append(str(table[6]))
            lst_url.append(link)

        en_tete = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
                   'number_available', 'product_description', 'category', 'review_rating', 'image_url']

        with open((str(category)+".csv"), 'w', encoding="utf-8", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(en_tete)
            for lst_url, lst_upc, lst_title, lst_price_including_tax, lst_price_excluding_tax, lst_number_available, \
                lst_description, lst_category, lst_review, lst_image_url \
                    in zip(lst_url, lst_upc, lst_title, lst_price_including_tax, lst_price_excluding_tax,
                           lst_number_available, lst_description, lst_category, lst_review, lst_image_url):
                writer.writerow([lst_url, lst_upc, lst_title, lst_price_including_tax, lst_price_excluding_tax,
                                 lst_number_available, lst_description, lst_category, lst_review, lst_image_url])

                # Récupération des images
                r = requests.get(lst_image_url, stream=True)
                if r.status_code == 200:
                    with open((lst_title[0:18].replace("*", "")).replace("?", "").replace(".", "")
                              .replace("\"", "").replace(":", "") + ".jpg", 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)

        os.chdir(my_cwd)

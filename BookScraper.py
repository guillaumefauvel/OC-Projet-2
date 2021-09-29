import requests
from bs4 import BeautifulSoup
import csv
import shutil
import os

# Définition de la fonction souper() pour récupérer le résultat parsé de l'url inséré.


def souper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        return "La requête a échoué."


# Définition de la fonction makemydir() : Permet de créer un fichier et de ce placer à l'intérieur.


def makemydir(folder_name):
    try:
        os.makedirs(folder_name)
    except OSError:
        pass
    os.chdir(folder_name)


# Initialisation du dossier d'export.
makemydir("Output")
my_cwd = os.getcwd()


soup_main = souper("https://books.toscrape.com")
searched_category = soup_main.find('ul', class_="nav nav-list")
category_dict = {}

# Récupération des liens propre à chaque catégorie
for link in searched_category.find_all('a', href=True):

    category_name = link.text.strip()
    category_dict[category_name] = ("https://books.toscrape.com/" + link['href'])

# Itération sur le dictionnaire contenant pour clé : la catégorie et comme valeur : le lien de la catégorie
for category in category_dict:

    if category == "Books":
        pass
    else:
        makemydir(category)

        soup_category = souper(category_dict[category])
        links_books = []
        # Vérifier s'il y a plusieurs pages ou s'il n'y en a qu'une
        try:
            pagination = (soup_category.find("li", {"class": "current"})).text.strip()
            num_of_page = pagination[-2:].strip()
        except AttributeError:
            num_of_page = 1

        # Récupération des liens de chaque livre présent sur la page
        # S'il y plusieurs pages nous passons à la page suivante
        for i in range(int(num_of_page)):
            links = soup_category.findAll('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

            # Création des liens et ajout à la liste links_books
            for link in links:
                a = "https://books.toscrape.com/catalogue"+(link.find('h3')).find("a")["href"].replace("../../..", "")
                links_books.append(a)

            # Déclaration des listes pour la réception des valeurs
            list_title = []
            list_description = []
            list_category = []
            list_image_url = []
            list_upc = []
            list_price_including_tax = []
            list_price_excluding_tax = []
            list_number_available = []
            list_review = []
            list_url = []

        # Récupération des valeurs propres à chaque livre
        for link in links_books:

            soup_book = souper(link)
            # Liste réceptionnant les valeurs présentes dans le tableau ( td )
            table = []

            # 'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)',
            # 'Tax', 'Availability', 'Number of reviews'
            for value in soup_book.find_all("td"):
                table.extend(value)

            # Ajout des valeurs récupéréés et transformées à leurs listes respectives.
            list_title.append((soup_book.find("li", {"class": "active"})).text)
            list_description.append((soup_book.find("meta", {"name": "description"})['content']).replace("    ", ""))
            list_category.append(soup_book.find("ul", "breadcrumb").find_next("a").find_next("a").find_next("a").text)
            list_image_url.append(str("https://books.toscrape.com" + (((soup_book.find("div", {"class": "item active"}))
                                  .find("img")["src"]).replace("../..", ""))))
            list_upc.append((table[0]))
            list_price_including_tax.append((str(table[3])).replace("Â", ""))
            list_price_excluding_tax.append((str(table[2])).replace("Â", ""))
            list_number_available.append(str(table[5]))
            list_review.append(str(table[6]))
            list_url.append(link)

        en_tete = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
                   'number_available', 'product_description', 'category', 'review_rating', 'image_url']

        # Création d'un fichier nom_categorie.csv et écriture du contenu.
        with open((str(category)+".csv"), 'w', encoding="utf-8", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(en_tete)
            for list_url, list_upc, list_title, list_price_including_tax, list_price_excluding_tax, \
                list_number_available, list_description, list_category, list_review, list_image_url \
                    in zip(list_url, list_upc, list_title, list_price_including_tax, list_price_excluding_tax,
                           list_number_available, list_description, list_category, list_review, list_image_url):
                writer.writerow([list_url, list_upc, list_title, list_price_including_tax, list_price_excluding_tax,
                                 list_number_available, list_description, list_category, list_review, list_image_url])

                # Récupération et téléchargement des images.
                r = requests.get(list_image_url, stream=True)
                if r.status_code == 200:
                    with open((list_title.replace("*", "")).replace("?", "").replace(".", "")
                              .replace("\"", "").replace(":", "") + ".jpg", 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)

        # Nous avons finis de boucler sur une catégorie, donc nous revenons au dossier parent.
        os.chdir(my_cwd)

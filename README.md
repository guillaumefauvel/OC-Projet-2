# Readme - BookScraper.py - [Lien Github](https://github.com/guillaumefauvel/OCProjet2)

**Version 1.0.0**

## Fonction

Le programme BookScraper est développé en Python. Il permet de récupérer une série de données sur le site https://books.toscrape.com.
Au terme d'un processus ETL il récupère les données désirées et les exporte dans plusieurs fichiers CSV. 
Il récupère également la première de couverture pour chacun des livres. 

## Utilisation

Pour lancer ce code vous avez besoin de python, rendez vous sur ce [lien](https://www.python.org/downloads/) pour l'installer.

Pour utiliser le programme il est fortement recommander de lancer un environnement virtuel.
- Vérifiez que votre version de python est supérieure ou égale à la 3.3. Tapez `python --version` pour vérifier que vous possédez cette fonctionnalité. 
- Si vous ne savez pas initialiser un environnement virtuel référez vous à ce [lien](https://openclassrooms.com/fr/courses/6951236-mettez-en-place-votre-environnement-python/7014018-creez-votre-premier-environnement-virtuel) :
- Si vous utilisez le PowerShell, au moment d'activer l'environnement virtuel utiliser la commande : `env/scripts/activate.ps1` 

    
Une fois l'environnement créé et activé, installez les dépendances en entrant `pip install -r requirements.txt`

Lorsque tout les modules ont été installé vous pouvez lancer le programme en tapant `python bookscraper.py`

##

*Le programme dure une trentaine de minutes*


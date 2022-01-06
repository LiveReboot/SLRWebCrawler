import time
import urllib.parse
import requests
import datetime
import sys

import animation
from bs4 import BeautifulSoup


from models.Publication import Publication
from utils.String import String
from utils.Terminal import Terminal
from utils.Waiting import waiting

# 1) Je remplis token et cookie
# 2) Je vérifie le User Agent
# 3) Je connecte mon Neo4J
# 4) Je lance la requête en Python
# 5) Chaque ligne Téléchargement correspond à la création d'un noeud et de lien dans Neo4J

class Sciencedirect:
    # Token
    token = ""

    # Header
    headers = {
        'Host': 'www.sciencedirect.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'https://www.sciencedirect.com/search?qs=%22ant%20colony%20algorithm%22',
        'Cookie': cookie,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    # Domaine URL
    domain = "https://www.sciencedirect.com"

    # Nombre de résultat par page
    maxResults = 100

    def __init__(self):
        pass

    # Rechercher la liste des publications
    def makeUrl(self, qs, page=1, params={}):
        # Calculer l'offset
        offset = (page - 1) * self.maxResults

        # Initialiser l'URL
        url = self.domain + "/search/api?"

        # Query
        url += "qs=" + urllib.parse.quote(qs, safe='')
        # Affichage
        url += "&show=" + str(self.maxResults)
        # Page
        url += "&offset=" + str(offset)
        # Token
        url += "&t=" + str(self.token)

        # Ajouter tous les paramètres supplémentaires
        for paramId in params:
            url += "&" + paramId + "=" + params[paramId]

        # Afficher l'URL
        Terminal.danger(url, "Exploration : ")

        return url

    # Envoyer la requête
    def request(self, query, page=1, params={}):
        # Préparer l'url de la requête
        url = self.makeUrl(query, page, params)
        # Télécharger la page
        response = requests.get(url, headers=self.headers)
        # Récupérer le JSON
        return response.json()

    # Rechercher la liste des publications
    @waiting(color="red")
    def list(self, query):

        # Première page
        page = 1
        # Nombre de résultats
        count = 1
        # Récupérer le nombre de résultat
        resultsFound = 0

        # Initialiser la variable de retour
        publications = []

        # Tant qu'on n'a pas autant de publication que le nombre trouvé
        while page == 1 or len(publications) < resultsFound:

            # Passer à la page suivante
            json = self.request(query, page)

            # Nombre de résultats
            if resultsFound == 0 and 'resultsFound' in json:
                resultsFound = json['resultsFound']

            # Aucun résultat
            if 'searchResults' not in json:
                return publications

            # Pour tous les résultats de la page
            for result in json['searchResults']:
                # Créer une publication
                p = Publication()

                # Interpréter le résultat
                publication = p.sciencedirect(result)

                # Charger les données
                Terminal.info(
                    publication.title,
                    "Téléchargement (" + str(count) + "/" + str(resultsFound) + ") : "
                )

                # Parser la publication
                soup = self.parse(publication)
                publication.keywords = self.keywords(soup)
                publication.authors = self.authors(soup)
                publication.abstract = String.addslashed(self.abstract(soup))

                # Ajouter à la liste
                publications.append(publication)

                # Enregistrer en base de données
                publication.neo4j(query)

                # Passer au suivant
                count += 1

            # Passer à la page suivante
            page += 1

        return publications

    # Parser une page Html
    def parse(self, publication):
        # Parser le lien pour récupérer les Keywords
        full_link = self.domain + publication.link
        Terminal.info(full_link, "Link : ")
        html = requests.get(full_link, headers=self.headers).text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    # Parser un article pour renvoyer les mots-clés
    def keywords(self, soup):

        # Renvoyer les mots clés
        keywords = []

        # Rechercher la partie "Keywords"
        attrs = {'class': 'keywords-section'}
        div_keywords = soup.find('div', attrs)
        if div_keywords is not None:

            # Récupérer le span
            spanKeywords = div_keywords.findChildren('span')

            # Ajouter tous les mots clés
            for k in spanKeywords:
                keywords.append(String.addslashed(k.text))

        return keywords

    # Parser un article pour renvoyer les auteurs
    def authors(self, soup):

        # Renvoyer les auteurs
        authors = []

        # Rechercher la partie "Auteurs"
        attrs = {'class': 'author-group'}
        div_authors = soup.find('div', attrs)
        if div_authors is not None:

            # Récupérer la liste
            a = div_authors.findChildren('span', {'class': 'content'})
            for track in a:
                author = ""
                name = track.find('span', {'class': 'given-name'})
                if name is not None:
                    subname = track.find('span', {'class': 'surname'})
                    if subname is not None:
                        author = String.addslashed(name.text + " " + subname.text)
                if len(author) > 0:
                    authors.append(author)

        return authors

    # Parser un article pour renvoyer l'abstract
    def abstract(self, soup):

        # Renvoyer les auteurs
        abstract = ""

        # Rechercher la partie "Abstract"
        attrs = {'class': 'abstract'}
        div_abstract = soup.find('div', attrs)
        if div_abstract is not None:
            # Récupérer l'abstract
            p_abstract = div_abstract.find('p')
            if p_abstract is not None:
                abstract = p_abstract.text

        return abstract

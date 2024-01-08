from datetime import datetime, timedelta
from dates import *
from parsing import stripProtocol, addProtocol
from typing import Tuple, Dict, List
import requests
import sys, os
import re
from time import sleep
from cleaning import nettoie

def generate_filename(url: str, date: datetime) -> str:
    """
        Pour une URL donnée, crée le nom de fichier sur le pattern url_date

        Traitements supplémentaires :
        - remplace les / par des _
        - ajoute la date au format YYYY-MM-DD à la fin
    """
    url_strip = stripProtocol(url)
    url_sans_slash = url_strip.replace('/', '_')
    return url_sans_slash + '-' + toString(date)

def checkCache(url: str, date: datetime) -> bool:
    """
        Teste si une url a déjà téléchargée dans le cache
    """
    all_directories = os.listdir('.')

    if ("cache" not in all_directories):
        print("Le dossier cache/ n'existe pas.")
        return False

    files_in_cache = os.listdir("./cache")
    filename = generate_filename(url, date)

    if (filename in files_in_cache):
        return True
    else:
        return False

def website_or_archive(url: str, date: datetime) -> str:
    """
        Renvoie la 'bonne' url :
        - l'url elle-même si la date est aujourd'hui
        - l'adress Web Archive si elle est avant
    """
    if (today(date)):
        return addProtocol(url)
    elif (dansLePasse(date)):
        webArchiveURL = "https://web.archive.org/web/" + toString(date, '') + "/" + url
        return webArchiveURL

def get_url(url: str, date: datetime) -> str:
    """
        Retourne le contenu de l'URL demandée :
        - depuis le cache si le fichier a déjà été téléchargé
        - l'enregistre dans le cache puis l'affiche sinon
    """
    # si le fichier est dans le cache
    if (checkCache(url, date)):
        print(f"En cache : {url}")
        # on affiche le contenu du fichier correspondant
        filename = generate_filename(url, date)
        path = "cache/" + filename
        with open(path, 'r') as f:
            content = f.read()
        return content
    # sinon, il faut télécharger le fichier
    else:
        print(f"Téléchargement : {url}")
        try:
            response = requests.get(url)
            sleep(4) # pause de 4 secondes
        except requests.ConnectionError:
            print("Erreur de connexion à " + url)
            return None
        except requests.Timeout:
            print("Délai dépassé pour " + url)
            return None
        except requests.RequestException:
            print("Erreur pour connexion à " + url)
            return None

        # si on a une bonne réponse du serveur
        if (response.status_code == requests.codes.ok):
            # on télécharge le contenu
            filename = generate_filename(url, date)
            path = "cache/" + filename
            content = response.text
            with open(path, 'w') as f:
                f.write(nettoie(content))
            # une fois le téléchargement réussi, on renvoie le contenu
            return content
        # sinon, on abandonne
        else:
            print(f"Téléchargement impossible, réponse HTTP : {response.status_code}")
            return None

def get_all_urls(date: datetime, site: str, empanFocus: int, empanWindow: int) -> Tuple[Dict[datetime, str], Dict[datetime, str]]:
    """
        Étant donné les paramètres du script, renvoie deux dictionnaires d'URL
        - url_focus : date -> URL
        - url_window : date -> URL
    """
    url_focus = {}
    url_window = {}

    # dans la fenêtre focus
    for i in range(-empanFocus, empanFocus+1):
        date_ = date + timedelta(days=i)
        if not dansLeFutur(date_):
            url = website_or_archive(site, date_)
            url_focus[date_] = url

    # dans la fenêtre window
    for i in range(-empanWindow, empanWindow+1):
        date_ = date + timedelta(days=i)
        # on n'inclut pas les dates déjà dans focus
        if (not dansLeFutur(date_)) and (date_ not in url_focus.keys()):
            url = website_or_archive(site, date_)
            url_window[date_] = url

    return (url_focus, url_window)

def charge_corpus(url_focus: Dict[datetime, str], url_window: Dict[datetime, str]) -> Tuple[str, str]:
    """
        Étant donnés les dictionnaires date->url pour focus et window,
        renvoie deux chaînes dont le contenu est la concaténation des pages
        web nettoyées de chaque catégorie
    """
    corpus_focus = ""
    corpus_window = ""

    for (date, url) in url_focus.items():
        content = get_url(url, date)
        if content is not None:
            corpus_focus = corpus_focus + nettoie(content) + '\n'

    for (date, url) in url_window.items():
        content = get_url(url, date)
        if content is not None:
            corpus_window = corpus_window + nettoie(content) + '\n'

    return (corpus_focus, corpus_window)

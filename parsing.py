import argparse
from datetime import datetime
import re

def checkDateFormat(entree: str) -> bool:
    try:
        datetime.strptime(entree, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def stringToDatetime(date: str) -> datetime:
    """
        Convertit une chaîne de caractères YYYY-MM-DD en objet datetime
    """
    try:
        datetimeDate = datetime.strptime(date, "%Y-%m-%d")
        return datetimeDate
    except ValueError:
        raise argparse.ArgumentTypeError(f"Format de date invalide : {date}")

def checkURLFormat(url: str) -> bool:
    pattern = re.compile(r'^(https?://)?[a-zA-Z0-9/.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(pattern, url))

def checkInteger(entier: str) -> bool:
    try:
        valeur_entiere = int(entier)
        return True
    except ValueError:
        return False

def stripProtocol(url: str) -> str:
    """
        Enlève le protocole http(s) devant le début de l'URL
        pour faciliter la gestion des fichiers cache
    """
    if ("http://" in url):
        return url.replace("http://", "")
    elif ("https://" in url):
        return url.replace("https://", "")
    else:
        return url

def addProtocol(url: str) ->str:
    """
        Ajoute le protocole https:// à l'url
    """
    return "https://" + url

def initArguments():
    """
        Vérifie la conformité de tous les arguments.
        Retourne le args pour accéder aux variables dans le main
    """
    parser = argparse.ArgumentParser()
    # paramètres obligatoires
    parser.add_argument('date', type=stringToDatetime, help="Date au format YYYY-MM-JJ")
    parser.add_argument('site', help="Une adresse de site web avec ou sans protocole")
    # paramètres facultatifs
    parser.add_argument("-f", "--focus", type=int, dest="empanFocus", help="empan de la fenêtre focus", default=1, required=False)
    parser.add_argument("-w", "--window", type=int, dest="empanWindow", help="empan de la fenêtre window", default=7, required=False)

    args = parser.parse_args()

    if (not checkURLFormat(args.site)):
        raise argparse.ArgumentTypeError(f"Format d'URL invalide : {args.site}")
    
    # on enlève le protocole pour simplifier les noms de fichier
    args.site = stripProtocol(args.site)

    if args.empanFocus:
        if (not checkInteger(args.empanFocus)):
            raise argparse.ArgumentTypeError(f"L'empan de la fenêtre focus n'est pas un entier : {args.empanFocus}")
    if args.empanWindow:
        if (not checkInteger(args.empanWindow)):
            raise argparse.ArgumentTypeError(f"L'empan de la fenêtre window n'est pas un entier : {args.empanWindow}")

    return args

from datetime import datetime
import re

def dansLePasse(date: datetime) -> bool:
    """
        Teste si une date est dans le passé
    """
    return date < datetime.today()

def dansLeFutur(date: datetime) -> bool:
    """
        Teste si une date est dans le futur
    """
    return date > datetime.today()

def today(date: datetime) -> bool:
    """
        Teste si une date est aujourd'hui
    """
    return date.date() == datetime.today().date()

def toString(date: datetime, separateur='-') -> str:
    """
        Retourne la chaîne YYYY-MM-DD à partir d'un objet datetime
    """
    return date.strftime('%Y' + separateur + '%m' + separateur + '%d')

def formatWebArchiveDate(dateWA: str) -> datetime:
    """
        Prend une date au format YYYYMMDD et renvoie l'objet datetime correpondant
    """
    # on vérifie qu'on a bien une suite de 8 chiffres
    pattern = re.compile(r"^[0-9]{8}$")
    if (re.match(dateWA, pattern)):
        # ok, on peut convertir en objet datetime
        datetimeWAdate = datetime.strptime(dateWA, "%Y%m%d")
        return datetimeWAdate
    else:
        print(f"Format invalide : {dateWA}")
        return None

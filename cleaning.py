import re
from bs4 import BeautifulSoup, Comment

def sur_une_ligne(entree: str) ->str:
    """
        Prend une chaîne de caractères en entrée et renvoie la même
        chaîne sur une seule ligne
    """
    return re.sub(r'\n', ' ', entree)

def enleve_balises(entree: str) -> str:
    """
        Supprime les balises :
        - script
        - noscript
        - head
        - style
        et tout leur contenu.
    """
    balises_a_supprimer = ['script', 'noscript', 'style', 'head']
    soup = BeautifulSoup(entree, 'html.parser')
    for balise in balises_a_supprimer:
        for element in soup.find_all(balise):
            element.decompose()
    return str(soup)

def efface_avant_endwayback(entree: str) -> str:
    """
        Efface le contenu situé avant <!-- END WAYBACK TOOLBAR INSERT -->
    """
    soup = BeautifulSoup(entree, 'html.parser')
    commentaire = "END WAYBACK TOOLBAR INSERT"
    endwayback = soup.find(text=lambda text: isinstance(text, Comment) and commentaire in text)
    # si le commentaire est bien dans la page HTML
    if endwayback:
        while endwayback.find_previous_sibling():
            endwayback.find_previous_sibling().decompose()
        return str(soup)
    # sinon on ne change rien
    else:
        return entree

def efface_commentaires(entree: str) -> str:
    """
        Efface tous les commentaires HTML d'une chaîne
    """
    soup = BeautifulSoup(entree, 'html.parser')
    for commentaire in soup.find_all(string=lambda text: isinstance(text, Comment)):
        commentaire.extract()
    return str(soup)

def efface_balises(entree: str) -> str:
    """
        Efface les balises
    """
    pattern = re.compile(r"<[^>]+>")
    return re.sub(pattern, ' ', entree)

def efface_espaces(entree: str) -> str:
    """
        Efface tous les espaces, potentiellement multiples
    """
    sans_espaces_multiples = re.sub(r'\s{2,}', ' ', entree)
    # on enlève aussi les espaces à gauche et à droite
    return sans_espaces_multiples.strip()

def nettoie(html_text: str) -> str:
    """
        Applique tous les traitements à une aspiration HTML,
        et retourne le résultat
    """
    return efface_espaces(efface_balises(efface_commentaires(efface_avant_endwayback(enleve_balises(sur_une_ligne(html_text))))))

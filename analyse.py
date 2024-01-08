import spacy
import math
from typing import Dict, List
from collections import defaultdict
import subprocess

# Installer le modèle de langue pour spacy
# python -m spacy download fr_core_news_sm

# charger le modèle de langue
nlp = spacy.load("fr_core_news_sm")
import fr_core_news_sm
nlp = fr_core_news_sm.load()

# on récupère les fréquences de chaque lemme nominal
def frequences_lemmes_nom(document: str) -> Dict[str, int]:
    """
        Prend un string et renvoie un dictionnaire lemme -> fréquence
        pour chaque lemme nominal (NOUN ou PROPN)
    """
    document_spacy = nlp(document)
    freq = defaultdict(int)
    for token in document_spacy:
        # on prend les tokens de + de 2 caractères
        if len(token.lemma_) > 1 and token.pos_ in ['NOUN', 'PROPN']:
            # on enregistre le lemme et on incrémente la fréquence
            freq[token.lemma_] += 1
    return freq

def specif(f: int, F: int, t: int, T: int) -> float:
    """
        Fait le calcul de spécificité
    """
    try:
        assert F < T
    except AssertionError:
        print(f"Le paramètre F(={f}) doit être inférieur à T(={T}).")

    lien_avec_parametres = "https://pro.aiakide.net/r-script/?f=" + str(f) + "&F=" + str(F) + "&t=" + str(t) +"&T=" + str(T)

    sortie_R = subprocess.run(['wget', '-q', '-O', '-', lien_avec_parametres], stdout=subprocess.PIPE, text=True).stdout.strip()

    # on gère cette sortie pour notre calcul de spécificité
    lignes = sortie_R.split('\n')

    mode = float(lignes[1].split(" ")[1])
    proba = float(lignes[3].split(" ")[1])

    if mode <= f:
        return abs(math.log10(abs(proba)))
    else:
        return -abs(math.log10(abs(proba)))

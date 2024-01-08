# Spécificité
Calcul de spécificités sur un site web scrapé
Ce script permet de collecter différentes versions d'un site web à partir d'une date donnée, dans une fenêtre paramétrable. On nettoies les pages html obtenues, on les traite avec spacy avant d'appliquer un script R qui calcule les spécificités de Lafon pour chaque lemme. On affiche enfin les 10 termes les moins spécifiques et les 10 plus spécifiques de la période.

# Exemple d'utilisation :
`python3 main.py 2024-01-02 https://www.frustrationmagazine.fr -f 1 -w 3`

# Sortie obtenue :
```
En cache : https://web.archive.org/web/20240101/www.frustrationmagazine.fr
En cache : https://web.archive.org/web/20240102/www.frustrationmagazine.fr
En cache : https://web.archive.org/web/20240103/www.frustrationmagazine.fr
En cache : https://web.archive.org/web/20231230/www.frustrationmagazine.fr
En cache : https://web.archive.org/web/20231231/www.frustrationmagazine.fr
En cache : https://web.archive.org/web/20240104/www.frustrationmagazine.fr
En cache : https://web.archive.org/web/20240105/www.frustrationmagazine.fr
Moins spécifiques :
l’	-0.2665909375378211
galerie	-0.24947934016684895
loi	-0.24733521470061517
travail	-0.2263554916090991
frustration	-0.2263554916090991
victime	-0.2263554916090991
commission	-0.2263554916090991
inceste	-0.2263554916090991
violence	-0.2263554916090991
enfant	-0.2263554916090991
Plus spécifiques :
écologie	-0.16556111101519597
économie	-0.16556111101519597
éducation	-0.16556111101519597
Féminisme	-0.16556111101519597
santé	-0.16556111101519597
contre-portrait	-0.16556111101519597
Communauté	-0.16556111101519597
chère	-0.16556111101519597
chronique	-0.16556111101519597
abonnement	-0.16556111101519597
```

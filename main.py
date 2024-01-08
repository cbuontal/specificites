from parsing import *
from dates import *
from download import *
from cleaning import *
from analyse import *

# initialisation des arguments
args = initArguments()
(date, site, empanFocus, empanWindow) = (args.date, args.site, args.empanFocus, args.empanWindow)

# téléchargement des "bonnes" pages web
(url_focus, url_window) = get_all_urls(date, site, empanFocus, empanWindow)

(corpus_focus, corpus_window) = charge_corpus(url_focus, url_window)

(freq_focus, freq_window) = (frequences_lemmes_nom(corpus_focus), frequences_lemmes_nom(corpus_window))

# dictionnaire des spécificités: lemme -> score de spécificité
spec_focus = {}

# on calcule la spécificité pour chaque terme du sous-corpus focus
F = len(corpus_focus)
T = len(corpus_window)
for (lemme, f) in freq_focus.items():
    t = freq_window[lemme] if lemme in freq_window.keys() else 0
    spec_focus[lemme] = specif(f, F, t, T)

    # on écrit dans le cache
    filepath = "cache/" + "spec" + "-" + str(f) + "-" + str(F) + "-" + str(t) + "-" + str(T)
    with open(filepath, 'w') as file:
      file.write(str(spec_focus[lemme]))

print("Moins spécifiques :")
for (lemme, specificite) in sorted(spec_focus.items(), key=lambda paire: paire[1])[:10]:
  print(f"{lemme}\t{specificite}")

print("Plus spécifiques :")
for (lemme, specificite) in sorted(spec_focus.items(), key=lambda paire: paire[1], reverse=True)[:10]:
  print(f"{lemme}\t{specificite}")

#spec = specif(1, 10, 100, 1000)
#print(f"Score de spécificité : {spec}")

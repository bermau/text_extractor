# text_extractor
## Python tools to study log files.
This program is in infancy and should not be used.

J'ai créé ce programme pour analyser des logs sous windows en Python. Je voulais un outil similaire à grep / uniq etc. du monde unix..

Ce travail est très embryonnaire et vous ne devriez sans doute pas l'utiliser.

# Etude d'un log
[graph_log_study.py](dms_log_study%2Fgraph_log_study.py) : permet de rechercher des erreurs dans un log. 
## Présentation :
  * Permet de recherche l'occurence des mots de type ERROR, WARNING.
  * Cumule les observations par période de temps variable (60 min par défaut)
  * Liste des erreurs avec leur contexte (2 lignes par défaut)
  * Génère un graphique
  * Les fichiers d'entrées sont spécifiés par un répertoire et un motif.
  * Les fichiers doivent être importés dans le répertoire d'entrée. 
## Limitation : 
  * le motif recherché doit être dans uen ligne comportant une date. 
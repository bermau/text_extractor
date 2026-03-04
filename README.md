# text_extractor
## Python tools to study log files
This program is in its infancy and should not be used except by its author.

J'ai créé ce programme pour analyser des logs sous windows en Python. Je voulais un outil apportant des fonctionnalités 
comme les outils unix de base (grep, uniq etc.). Ce travail est très embryonnaire et vous ne devriez sans doute pas l'utiliser.

# Etude d'un log
[graph_log_study.py](dms_log_study%2Fgraph_log_study.py) : permet de rechercher des erreurs dans un log. 
## Présentation :
  * Permet de recherche occurrence des mots de type ERROR, WARNING.
  * Cumule les observations par période de temps variable (60 min par défaut)
  * Liste des erreurs avec leur contexte (2 lignes par défaut)
  * Génère un graphique
  * Les fichiers d'entrées sont spécifiés par un répertoire et un motif.
  * Les fichiers doivent être importés dans le répertoire d'entrée.
  * Les fonctions débutant par `demo_` décrivent des scénarios fréquents.

[log_recuperator.py](dms_log_study%2Flog_recuperator.py) : programme pour récupérer les logs d'un serveur 
depuis un PC sur Windows. 

## Limitation : 
  * On peut chercher un mot dans une ligne contenant une date ainsi que l'occurrence d'un autre mot la même ligne, 
la précédente ou la suivante. On ne peut recherche un mot s'il n'y a pas de date.
  * Pas de regex pour l'instant.
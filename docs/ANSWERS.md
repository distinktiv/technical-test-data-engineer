# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

_Inscrire la documentation technique_

## Questions (étapes 4 à 7)

### Étape 4
Pour stocker les informations récupérées des trois sources de données (tracks, users, listen history) 
une base de données relationnelle tel que PostgreSQL serait utilisé pour préserver la structure relationelle des donnés.
![My Local Image](diagram_bd.png)


### Étape 5

Pour suivre la santé du pipeline, quelques outils peuvent être mis en place:
- Logs: Permet de capturer les erreurs qui surviennent lors de l'ingestion des données.
- Monitoring: Des outils tel que Sentry, Datadog, Kibana vont servir d'interface visuel pour surveiller et analyser les logs.

Métriques Clés à Suivre:
- Surveillance: 
  - Monitoring des erreurs.
  - Suivie des appels API externes.
- Performance: le temps d'exécution du pipeline 
- Fiabilité: Taux de reussite de l'ingestion des ressources
- Ressource CPU: utilisation des ressources CPU

### Étape 6

_votre réponse ici_

### Étape 7

_votre réponse ici_

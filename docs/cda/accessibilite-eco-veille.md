# Accessibilite, eco-conception et veille - Staffly

## 1. Accessibilite

Le projet a ete renforce pour mieux repondre aux principes du RGAA :

- ajout d'un lien d'evitement vers le contenu principal ;
- ajout d'un focus visible pour la navigation clavier ;
- ajout de roles et d'attributs ARIA utiles sur les messages et formulaires ;
- ajout d'une legende invisible pour le tableau des taches ;
- ajout d'etiquettes et d'aides de saisie sur les champs importants ;
- meilleure clarification des statuts affiches a l'utilisateur.

Limites actuelles :

- audit RGAA complet non realise ;
- contraste et navigation clavier encore a verifier sur l'ensemble des ecrans ;
- absence de tests automatisees d'accessibilite.

## 2. Eco-conception

Les choix actuels vont dans le sens d'une application legere :

- rendu serveur simple avec Flask et Jinja ;
- peu de JavaScript ;
- peu de dependances front ;
- interface sobre avec ressources limitees ;
- architecture simple a maintenir.

Ameliorations futures possibles :

- mesure de performance Lighthouse ;
- optimisation des polices et ressources externes ;
- reduction de certaines dependances de demonstration ;
- suivi plus formel des indicateurs d'eco-conception.

## 3. Veille technique et securite

Une veille CDA peut etre presentee autour de :

- recommandations ANSSI sur les mots de passe et la securisation web ;
- bonnes pratiques OWASP pour les sessions, CSRF et validation des entrees ;
- evolutions Railway, Docker et GitHub Actions ;
- securite des dependances Python ;
- accessibilite web et RGAA.

Exemples de sujets de veille pertinents pour Staffly :

- comment limiter les risques CSRF ;
- comment proteger les cookies de session ;
- comment automatiser les controles qualite en CI ;
- comment mieux securiser une application Flask en production.

## 4. Valeur pour le CDA

Cette partie permet de montrer que le projet ne se limite pas au developpement
fonctionnel. Elle prouve une prise en compte :

- de l'accessibilite ;
- de l'eco-conception ;
- de la veille continue sur la securite et les pratiques de developpement.

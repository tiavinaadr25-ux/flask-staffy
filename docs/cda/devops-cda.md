# DevOps et deploiement - Staffly

## Objectif

Cette note formalise les premiers elements DevOps ajoutes au projet pour
rapprocher Staffly des attendus CDA.

## 1. Conteneurisation

Fichiers ajoutes :
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

Services declares dans `docker-compose.yml` :
- `web` : application Flask / Gunicorn
- `postgres` : base relationnelle
- `mongo` : base NoSQL

## 2. Automatisation de la qualite

Le projet dispose deja de :
- `black`
- `flake8`
- `pytest`
- `pre-commit`

Ces outils permettent de verifier :
- le formatage ;
- la qualite statique ;
- les tests automatises.

## 3. Integration continue

Pipeline ajoute :
- `.github/workflows/ci.yml`

Etapes du pipeline :
1. checkout du depot ;
2. installation de Python ;
3. installation des dependances ;
4. verification `black --check` ;
5. verification `flake8` ;
6. execution de `pytest`.

Un service PostgreSQL est lance dans le workflow afin de rapprocher les
tests de l'environnement cible.

## 4. Commandes utiles

Le `Makefile` fournit des commandes simples :
- `make format`
- `make lint`
- `make test`
- `make up`
- `make down`

## 5. Limites actuelles

Le projet n'est pas encore sur une chaine DevOps complete.
Les evolutions futures possibles sont :
- deployment automatique sur environnement de recette ;
- tests end-to-end ;
- migrations automatisees ;
- strategie de rollback ;
- suivi de couverture de tests ;
- scan de securite des dependances.

## 6. Valeur pour le CDA

Les ajouts realises montrent :
- une application deployee dans un environnement structure ;
- l'usage d'outils qualite ;
- une premiere demarche CI ;
- une base technique pour aller vers une vraie mise en production DevOps.

# Plan de tests - Staffly

## Objectif

Ce document formalise un plan de tests simple et presentable au niveau CDA.

## Environnements

- local developpement : SQLite ou PostgreSQL local ;
- integration continue : PostgreSQL via GitHub Actions ;
- production : PostgreSQL Railway.

## Perimetre teste

### Authentification

- ouverture de la page de connexion ;
- connexion avec compte valide ;
- refus d'acces sans authentification ;
- creation de compte ;
- refus d'email deja existant.

### Taches

- acces protege a la page des taches ;
- creation d'une tache ;
- controle CSRF sur creation de tache ;
- interdiction d'acceder a une tache d'un autre manager.

### IA

- generation de suggestions en mode fallback ;
- affichage des suggestions dans la page taches.

## Jeu d'essai principal

Compte de test :
- email : `manager@staffly.com`
- mot de passe : `Staffly123!`

Donnees attendues :
- un manager de test ;
- un employe de test ;
- des taches manipulables pendant les tests.

## Cas de test representatifs

| ID | Fonctionnalite | Entree | Resultat attendu |
|---|---|---|---|
| T01 | Dashboard protege | GET `/dashboard` sans session | redirection vers `/login` |
| T02 | Connexion | email + mot de passe valides | acces au dashboard |
| T03 | Inscription | nouvel email | compte cree et session ouverte |
| T04 | Inscription en doublon | email existant | erreur 409 |
| T05 | Creation de tache | formulaire valide | tache enregistree |
| T06 | CSRF | POST sans token | erreur 400 |
| T07 | Isolation des donnees | acces a une tache d'un autre manager | erreur 404 |
| T08 | Suggestions IA | prompt texte | suggestions visibles |

## Outils utilises

- `pytest`
- client de test Flask
- base de test isolee
- job CI GitHub Actions avec PostgreSQL

## Resultat actuel

Le projet dispose de tests automatises dans :
- `tests/conftest.py`
- `tests/test_app.py`

Ces tests couvrent :
- le parcours d'authentification ;
- la creation de compte ;
- la protection d'acces ;
- la creation de tache ;
- la protection CSRF ;
- l'isolation des donnees ;
- la suggestion IA en mode de secours.

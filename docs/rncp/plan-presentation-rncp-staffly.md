# Plan de presentation RNCP - Staffly

Ce document adapte la structure du PDF `Presentation_RNCP.pdf` au projet Staffly.

L'idee est de garder la meme logique de soutenance :

1. Conception du projet
2. Front-end
3. Back-end
4. Questions / entretien technique

---

## Structure generale de la presentation

### Slide 1 - Couverture

**Titre :** RNCP Developpeur Web et Web Mobile  
**Projet :** Staffly  
**Sous-titre conseille :** SaaS de gestion des taches pour managers de restaurants  
**Nom / date :** a completer

### Slide 2 - Sommaire

Reprendre le meme format :

- 01. Conception du projet
- 02. Front-end
- 03. Back-end
- 04. Questions / entretien technique

---

## 01. Conception du projet

### Slide 3 - Transition

Titre :

**01. Conception du projet**

### Slide 4 - Le projet

Titre :

**Le projet**

Texte conseille :

> Staffly est une application web de type SaaS qui aide les managers de restaurants a organiser leurs taches quotidiennes, gagner du temps et structurer leurs services.

Mots-cles a mettre :

- SaaS
- restauration
- organisation
- taches
- gain de temps
- demonstration

### Slide 5 - Planification des etapes

Comme dans le modele :

- Cahier des charges
- Charte graphique
- Maquettes
- Developpement
- Tests
- Deploiement

### Slide 6 - Cahier des charges

Mettre :

- Objectif du site
- Cible du site
- Type de site
- Plan du site
- Aspect visuel du site

Version Staffly :

- **Objectif** : aider un manager a organiser ses taches et preparer ses services
- **Cible** : managers de restaurants
- **Type de site** : SaaS web
- **Plan du site** : landing, inscription, connexion, dashboard, taches
- **Aspect visuel** : interface simple, professionnelle, orientee productivite

### Slide 7 - Charte graphique

Mettre :

- logo Staffly
- couleurs principales
- police DM Sans
- esprit general du design

### Slide 8 - Zoning

Montrer :

- zoning de la landing page
- zoning de la page des taches si possible

### Slide 9 - Wireframe

Montrer :

- wireframe de la landing
- wireframe connexion
- wireframe dashboard
- wireframe taches

### Slide 10 - Mock-up : page d'accueil

Mettre la landing finale Staffly.

### Slide 11 - Mock-up : page de connexion

Mettre la page de connexion Staffly.

### Slide 12 - Mock-up : page principale du SaaS

Comme ton projet ne tourne plus autour d'une page detail recette, adapte cette slide en :

**Mock-up : page des taches**

Montrer :

- formulaire de suggestion IA
- suggestions generees
- liste des taches

---

## 02. Front-end

### Slide 13 - Transition

Titre :

**02. Front-end**

### Slide 14 - Configuration de l'environnement de travail

Reprendre l'esprit de la slide du modele avec tes outils :

- Python
- Flask
- PostgreSQL
- MongoDB
- GitHub
- Visual Studio Code
- Railway
- Tally
- Make

### Slide 15 - Architecture MVC

Titre :

**Architecture Modele - Vue - Controleur**

Contenu Staffly :

- **Modele** : PostgreSQL, SQLAlchemy, MongoDB
- **Vue** : HTML, Jinja, CSS, JavaScript
- **Controleur** : Flask, `app.py`

### Slide 16 - Initialisation Flask

Montrer :

- creation de l'application Flask
- configuration
- rendu des templates
- premiere route

### Slide 17 - Interfaces statiques

Montrer :

- heritage Jinja
- structure `base.html`
- reutilisation des templates

### Slide 18 - Design et composants

Dans ton projet tu n'utilises pas Bootstrap au coeur de l'interface finale, donc adapte la slide comme ceci :

**Design et composants UI**

Montrer :

- boutons
- formulaires
- cartes
- navigation

### Slide 19 - Interfaces dynamiques

Montrer :

- inscription
- connexion
- affichage des taches

### Slide 20 - Interfaces dynamiques

Montrer :

- formulaire de suggestion IA
- resultat affiche dynamiquement dans la page des taches

---

## 03. Back-end

### Slide 21 - Transition

Titre :

**03. Back-end**

### Slide 22 - Modelisation base de donnees

Tu peux reprendre exactement la logique du modele :

1. Recueil du besoin des utilisateurs (UML)
2. Regles de gestion
3. Dictionnaire de donnees
4. MCD
5. MLD
6. MPD

### Slide 23 - Diagramme UML

Montrer le Use Case Diagram Staffly avec :

- Prospect
- Manager
- consulter la landing
- demander une demo
- creer un compte
- se connecter
- acceder au dashboard
- consulter les taches
- creer / modifier / supprimer une tache
- generer des suggestions de taches

### Slide 24 - Dictionnaire de donnees

Montrer un extrait du dictionnaire :

- table `managers`
- table `tasks`

Tu peux t'appuyer sur :

- [dictionnaire-donnees.md](/Users/beauvoir/Documents/New%20project/flask-staffy/docs/rncp/dictionnaire-donnees.md)

### Slide 25 - Dictionnaire de donnees

Deuxieme slide possible avec :

- collection `ai_suggestions`
- donnees Tally

### Slide 26 - Modele conceptuel des donnees

Montrer le MCD du MVP :

- MANAGER
- TASK
- relation CREER

### Slide 27 - Modele logique des donnees

Montrer :

- table `MANAGER`
- table `TASK`
- cle primaire / cle etrangere

### Slide 28 - Modele physique des donnees

Montrer le MPD avec types SQL :

- `SERIAL`
- `VARCHAR`
- `TEXT`
- `DATE`
- `TIMESTAMPTZ`

### Slide 29 - Securite, confidentialite et integrite des donnees

Comme dans le modele, tu peux mettre 5 points :

1. Securite des connexions
2. Securite des acces a la base de donnees
3. Gestion des sessions et des utilisateurs
4. Controle des formulaires et validation des donnees
5. Variables d'environnement

### Slide 30 - Securite, confidentialite et integrite des donnees

Montrer :

- hashage Bcrypt
- CSRF
- headers de securite
- session cookie
- controle d'acces aux donnees

### Slide 31 - Acces aux donnees SQL et NoSQL

Titre adapte :

**Developper des composants d'acces aux donnees SQL et NoSQL**

Montrer :

- modeles SQLAlchemy
- acces PostgreSQL
- acces MongoDB
- suggestion IA

### Slide 32 - Exemple table dans BDD SQL

Montrer la table `managers` ou `tasks`.

### Slide 33 - Exemple table dans BDD NoSQL

Montrer un document MongoDB `ai_suggestions`.

### Slide 34 - Base de donnees de test

Montrer :

- base locale
- ou environnement de test Pytest

### Slide 35 - Tests unitaires

Montrer :

- pourquoi Pytest a ete utilise
- environnement de test
- interet des tests

### Slide 36 - Tests unitaires

Montrer un exemple de test :

- dashboard protege
- login
- creation de tache

### Slide 37 - Tests unitaires

Montrer les resultats :

- `pytest`
- nombre de tests passes

### Slide 38 - Tests de securite

Comme tu n'as pas un outil de pentest lourd dans le projet, adapte la slide en montrant :

- verification CSRF
- verification acces aux routes
- validation des formulaires

### Slide 39 - Documentation et qualite du code

Montrer :

- docstrings
- commentaires
- typage
- bonnes pratiques
- pre-commit
- Flake8
- Black

### Slide 40 - Documentation et qualite du code

Montrer :

- README
- documents RNCP
- structure du dossier `docs/rncp`

### Slide 41 - Deploiement

Reprendre la logique du modele mais adaptee :

1. `requirements.txt`
2. `gunicorn`
3. connexion GitHub / Railway
4. variables d'environnement
5. PostgreSQL
6. MongoDB

Tu peux aussi dire que Docker a ete laisse de cote pour rester sur un MVP simple.

### Slide 42 - Deploiement

Montrer :

- Railway
- services
- variables
- domaine public

### Slide 43 - Deploiement

Montrer l'URL de ton application Staffly en ligne.

### Slide 44 - Questions / entretien technique

Slide simple de transition :

**04. Questions / entretien technique**

### Slide 45 - Fin

Titre :

**Merci ! Des questions ?**

---

## Slides les plus importantes a soigner

Si tu manques de temps, soigne en priorite :

- slide 4 : vue d'ensemble du projet
- slide 10 : landing page
- slide 12 : page taches
- slide 23 : UML
- slide 26 : MCD
- slide 28 : MPD
- slide 30 : securite
- slide 42 : Railway
- slide 43 : URL de production

---

## Captures a utiliser

### Captures produit

- landing page
- page connexion
- dashboard
- page taches
- suggestions IA

### Captures techniques

- GitHub
- Railway
- PostgreSQL
- MongoDB
- Tally
- Make
- email automatique recu
- Pytest

### Captures modelisation

- UML
- MCD
- MLD
- MPD
- dictionnaire de donnees

---

## Conseils de soutenance

- garde une slide = une idee
- privilegie les captures et schémas aux longs paragraphes
- relie toujours le visuel a une competence du Bloc 2
- insiste sur le fait que tu as volontairement reduit le perimetre pour livrer un MVP propre, teste et deploye

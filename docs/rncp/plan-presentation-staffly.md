# Plan de presentation - Staffly

Ce document reprend la structure de la presentation `Miaouff` et l'adapte au projet `Staffly`.

L'objectif est de produire une presentation de groupe ou individuelle d'environ 20 minutes, avec une logique claire :

- conception du projet ;
- front-end ;
- back-end ;
- securite ;
- deploiement ;
- automatisation.

---

## Structure generale

### Slide 1 - Couverture

**Titre :** Staffly  
**Sous-titre :** SaaS de gestion des taches pour managers de restaurants  
**Nom / session / date :** a completer

Contenu conseille :

- logo Staffly ;
- nom de la candidate ;
- date de soutenance ;
- phrase courte de presentation.

### Slide 2 - Sommaire

Comme dans l'exemple Miaouff :

1. Conception du projet  
2. Front-end  
3. Back-end  

### Slide 3 - Conception du projet

Slide de transition avec le titre :

**Conception du projet**

### Slide 4 - Vue d'ensemble du projet

Expliquer Staffly avec quelques mots-cles :

- organisation ;
- taches ;
- gain de temps ;
- demo ;
- IA ;
- automatisation.

Phrase possible :

> Staffly est une application web qui aide les managers de restaurants a organiser leurs taches quotidiennes, gagner du temps et structurer leur activite.

### Slide 5 - Planification des etapes

Comme dans Miaouff, presenter la logique de conception :

- cahier des charges ;
- maquettes ;
- charte graphique ;
- developpement ;
- tests ;
- deploiement.

### Slide 6 - Cahier des charges

Mettre :

- objectif du site ;
- cible ;
- type de site ;
- fonctionnalites principales ;
- contraintes techniques.

Pour Staffly :

- cible : managers de restaurants ;
- type : SaaS web ;
- besoin : creer et suivre des taches, demander une demo ;
- technologies : Flask, PostgreSQL, MongoDB, Railway.

### Slide 7 - Charte graphique

Montrer :

- logo Staffly ;
- couleurs principales ;
- police DM Sans ;
- ambiance generale.

### Slide 8 - Zoning

Montrer le zoning de la landing page et, si possible, de la page `Taches`.

### Slide 9 - Wireframe

Montrer le wireframe principal :

- landing
- connexion
- dashboard
- page taches

### Slide 10 - Mockup

Montrer la maquette finale Staffly.

### Slide 11 - GitHub

Montrer :

- le depot GitHub ;
- la branche de developpement ;
- quelques commits significatifs.

### Slide 12 - Kanban

Montrer ton tableau Notion / Kanban.

### Slide 13 - Vue calendrier

Montrer la planification jusqu'au 17 avril.

### Slide 14 - Hierarchie du site

Adapter la slide de hierarchie de Miaouff a Staffly.

Exemple :

- Landing page
- Creer un compte
- Connexion
- Dashboard
- Taches
- Demander une demo

### Slide 15 - Modele Vue Controleur

Montrer le MVC du projet Staffly :

- **Modele** : PostgreSQL, SQLAlchemy, MongoDB
- **Vue** : HTML, Jinja, CSS, JavaScript
- **Controleur** : Flask, `app.py`

Tu peux aussi placer :

- Tally ;
- Make ;
- Hugging Face.

### Slide 16 - Architecture de l'infrastructure

Montrer :

- navigateur utilisateur ;
- front-end ;
- back-end Flask ;
- PostgreSQL ;
- MongoDB ;
- Railway ;
- Tally ;
- Make ;
- Hugging Face.

---

## Partie Front-end

### Slide 17 - Front-end

Slide de transition :

**Front-end**

### Slide 18 - Landing page

Montrer :

- capture de la landing ;
- structure HTML ;
- but marketing de la page.

### Slide 19 - CSS / design

Montrer :

- le style CSS ;
- la cohérence visuelle ;
- la typographie ;
- les couleurs.

### Slide 20 - Dashboard

Montrer :

- le dashboard ;
- la logique de simplification du MVP ;
- les taches recentes.

### Slide 21 - Page Taches

Montrer :

- la page des taches ;
- le formulaire de suggestion IA ;
- la liste des taches.

### Slide 22 - Formulaire Tally

Montrer :

- le formulaire `Demander une demo Staffly`.

### Slide 23 - Integration du formulaire Tally

Montrer :

- le bouton sur la landing ;
- la variable `TALLY_DEMO_URL` ;
- la redirection vers le formulaire public.

---

## Partie Back-end

### Slide 24 - Back-end

Slide de transition :

**Back-end**

### Slide 25 - Diagramme UML

Montrer :

- le diagramme de cas d'utilisation UML

Acteurs proposes :

- Prospect
- Manager

### Slide 26 - Dictionnaire de donnees

Montrer un extrait du dictionnaire :

- `managers`
- `tasks`
- `ai_suggestions`

### Slide 27 - MCD

Montrer le MCD du MVP.

### Slide 28 - MLD

Montrer le MLD / LMD.

### Slide 29 - MLD detaille

Si besoin :

- zoom sur les relations ;
- detail des cles.

### Slide 30 - MPD

Montrer le MPD avec les types SQL.

### Slide 31 - Integration SQLAlchemy

Montrer :

- le modele `Manager`
- le modele `Task`
- la relation avec SQLAlchemy

### Slide 32 - Creation des tables

Montrer :

- `init-db`
- `seed-demo-data`
- ou la creation via SQLAlchemy.

### Slide 33 - Tables de la base de donnees

Montrer :

- `managers`
- `tasks`

### Slide 34 - CREATE

Montrer un exemple de creation de tache.

### Slide 35 - READ

Montrer l'affichage des taches dans le dashboard ou la page `Taches`.

### Slide 36 - UPDATE

Montrer la modification d'une tache.

### Slide 37 - DELETE

Montrer la suppression d'une tache.

### Slide 38 - Base NoSQL MongoDB

Montrer :

- MongoDB dans Railway ;
- la collection `ai_suggestions` ;
- l'utilite de l'historique technique IA.

### Slide 39 - Tests unitaires

Montrer :

- le fichier `test_app.py`
- les tests principaux

### Slide 40 - Resultat des tests

Montrer :

- `pytest`
- `flake8`

---

## Securite, deploiement, automatisation

### Slide 41 - Securite et RGPD

Mettre :

- hachage des mots de passe ;
- variables d'environnement ;
- CSRF ;
- sessions ;
- consentement Tally ;
- finalite des donnees.

### Slide 42 - Deploiement

Montrer :

- Railway ;
- domaine public ;
- PostgreSQL ;
- MongoDB ;
- environnement de production.

### Slide 43 - Hebergement

Montrer le choix Railway et pourquoi il a ete retenu.

### Slide 44 - Automatisation avec Make

Montrer :

- scenario Tally -> Make -> Email ;
- email recu ;
- valeur pour le produit.

### Slide 45 - Conclusion

Comme dans Miaouff :

**MERCI**

Tu peux ajouter :

- resume tres court du projet ;
- ce que le Bloc 2 a permis de construire ;
- ouverture vers la suite CDA.

---

## Conseils de presentation

### 1. Ce qu'il faut mettre en avant

- la continuite Bloc 1 -> Bloc 2 ;
- le choix d'un MVP simple mais fonctionnel ;
- la partie SQL ;
- la partie NoSQL ;
- l'IA ;
- Tally + Make ;
- le deploiement Railway.

### 2. Ce qu'il faut eviter

- trop de code sur une slide ;
- trop de texte ;
- trop de fonctionnalites secondaires.

### 3. Regle simple

Une slide = une idee principale.

### 4. Slides a illustrer en priorite

- landing ;
- page taches ;
- UML ;
- MCD ;
- Tally ;
- Make ;
- Railway.

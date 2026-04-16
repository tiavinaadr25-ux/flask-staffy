# Dossier Projet RNCP - Bloc 2

## Page de garde

**Titre du projet :** Staffly  
**Type de projet :** Application web de gestion operationnelle pour managers de restaurants  
**Bloc concerne :** Bloc 2 - Developper la partie back-end d'une application web ou web mobile securisee  
**Technologies principales :** Flask, PostgreSQL, MongoDB, Railway, Tally, Make  
**Nom de la candidate :** A completer  
**Session :** A completer  

---

## Sommaire

1. Contexte du projet  
2. Presentation generale de Staffly  
3. Cahier des charges et objectifs  
4. Perimetre fonctionnel du MVP  
5. Methodologie et organisation du projet  
6. Conception fonctionnelle  
7. Conception technique et architecture  
8. Front-end  
9. Back-end  
10. Base de donnees  
11. Integrations externes : IA, Tally, Make  
12. Tests et qualite  
13. Securite et RGPD  
14. Infrastructure et deploiement  
15. Bilan du projet  
16. Annexes et captures a integrer  

---

## 1. Contexte du projet

Staffly est un projet de SaaS imagine pour aider les managers de restaurants a mieux organiser leur activite quotidienne. Dans un restaurant, le manager doit souvent jongler entre plusieurs besoins :

- preparer les services ;
- organiser les taches prioritaires ;
- coordonner l'equipe ;
- gagner du temps dans la gestion quotidienne ;
- centraliser les demandes de demonstration ou de prise de contact.

Dans un premier temps, le projet a commence par une landing page et une direction visuelle definies dans le Bloc 1. Le Bloc 2 a permis de faire evoluer cette base vers une application web dynamique avec :

- un back-end Flask ;
- une base de donnees relationnelle ;
- des composants serveur ;
- une authentification ;
- une logique metier ;
- des integrations externes.

L'objectif du Bloc 2 n'etait pas seulement de produire une interface visuelle, mais de transformer l'idee initiale en un MVP fonctionnel, deployee et presentable.

---

## 2. Presentation generale de Staffly

Staffly est une application web qui propose deux niveaux d'usage :

### 2.1 Partie publique

La landing page permet de :

- decouvrir la proposition de valeur du projet ;
- comprendre le gain de temps apporte par l'outil ;
- acceder a l'inscription ;
- demander une demonstration via un formulaire Tally.

### 2.2 Partie privee

La partie privee est reservee au manager connecte. Elle permet de :

- se connecter a son espace ;
- acceder a un dashboard ;
- creer et suivre des taches ;
- generer des suggestions de taches a l'aide de l'IA ;
- utiliser un outil simple, rapide a prendre en main et adapte a un MVP.

---

## 3. Cahier des charges et objectifs

### 3.1 Besoin initial

Le projet devait repondre aux attendus suivants :

- partir d'un projet Flask existant ;
- versionner le code avec Git et GitHub ;
- structurer l'application avec une base de donnees locale puis distante ;
- preparer un deploiement Railway ;
- ajouter des tests et des bonnes pratiques de code ;
- produire une documentation de projet compatible RNCP ;
- integrer des outils externes comme Tally, Make et une API IA.

### 3.2 Objectifs du MVP

Pour respecter le delai et produire une soutenance claire, le projet a ete volontairement reduit a un MVP realiste.

Objectifs retenus :

- permettre a un manager de creer un compte et se connecter ;
- afficher un dashboard simple ;
- gerer des taches ;
- proposer des suggestions de taches IA ;
- utiliser PostgreSQL pour les donnees metier ;
- utiliser MongoDB comme preuve NoSQL pour l'historique IA ;
- utiliser Tally et Make pour automatiser les demandes de demonstration ;
- deployer le projet sur Railway.

### 3.3 Choix de reduction du perimetre

Certaines parties initialement envisagees ont ete retirees de l'interface finale pour garder un projet plus clair et plus demonstrable :

- la gestion visible des employes ;
- la gestion visible des conges.

Ces structures existent encore partiellement dans le code comme base d'evolution future, mais elles ne sont pas au coeur du MVP presente.

---

## 4. Perimetre fonctionnel du MVP

### 4.1 Fonctionnalites visibles

Le MVP final inclut :

- landing page Staffly ;
- creation de compte manager ;
- connexion manager ;
- dashboard ;
- creation, consultation, modification et suppression de taches ;
- suggestions de taches avec IA ;
- bouton "Demander une demo" sur la landing ;
- formulaire Tally ;
- automatisation Make apres soumission du formulaire.

### 4.2 Fonctionnalites techniques

Le projet inclut egalement :

- base relationnelle PostgreSQL ;
- base NoSQL MongoDB ;
- sessions et securite de base ;
- tests avec Pytest ;
- qualite de code avec Flake8 ;
- variables d'environnement ;
- deploiement Railway.

---

## 5. Methodologie et organisation du projet

### 5.1 Organisation de travail

Le projet a ete realise seule. Le brief mentionnait une organisation par branches pour une equipe, mais dans ce contexte, le choix retenu a ete :

- une branche de developpement dediee ;
- un suivi des evolutions via Git et GitHub ;
- une simplification du perimetre pour livrer un MVP stable.

### 5.2 Versionning

Le code a ete gere avec Git et GitHub.

Points importants :

- travail sur une branche de developpement ;
- commits regulierement realises ;
- push sur GitHub ;
- deploiement depuis GitHub vers Railway.

### 5.3 Demarche projet

La demarche adoptee a ete iterative :

1. analyser le prototype existant ;
2. stabiliser l'application Flask ;
3. mettre en place la base de donnees ;
4. ajouter les routes et la logique metier ;
5. simplifier le perimetre du MVP ;
6. integrer l'IA ;
7. integrer Tally et Make ;
8. preparer les livrables RNCP.

---

## 6. Conception fonctionnelle

### 6.1 Utilisateurs cibles

Le projet vise principalement :

- les managers de restaurants ;
- les responsables d'equipe en restauration ;
- les prospects qui souhaitent demander une demonstration du produit.

### 6.2 Parcours utilisateur principal

#### Parcours prospect

1. Le prospect consulte la landing page.
2. Il comprend la promesse de valeur de Staffly.
3. Il clique sur "Demander une demo".
4. Il remplit le formulaire Tally.
5. La demande declenche une automatisation Make et un email.

#### Parcours manager

1. Le manager cree un compte.
2. Il se connecte.
3. Il accede au dashboard.
4. Il consulte ses taches.
5. Il cree une tache.
6. Il peut aussi utiliser la suggestion IA pour preparer son service.

### 6.3 Use cases principaux

Les principaux cas d'utilisation du MVP sont :

- consulter la landing page ;
- demander une demo ;
- creer un compte ;
- se connecter ;
- acceder au dashboard ;
- consulter les taches ;
- creer une tache ;
- modifier une tache ;
- supprimer une tache ;
- generer des suggestions de taches.

Le diagramme UML de cas d'utilisation devra etre integre comme annexe visuelle dans le dossier final.

---

## 7. Conception technique et architecture

### 7.1 Architecture generale

Le projet repose sur une architecture web simple :

- **Front-end** : templates HTML/CSS/JS ;
- **Back-end** : Flask ;
- **BDD relationnelle** : PostgreSQL ;
- **BDD NoSQL** : MongoDB ;
- **Outils externes** : Tally, Make, Hugging Face ;
- **Hebergement** : Railway.

### 7.2 Logique MVC simplifiee

Le projet suit une logique proche du modele MVC :

- **Model** : classes SQLAlchemy comme `Manager`, `Task`, `Employee`, `LeaveRequest` ;
- **View** : templates HTML dans le dossier `templates/` ;
- **Controller** : routes Flask definies dans `app.py`.

### 7.3 Documents de modelisation

Les documents de modelisation prepares pour le projet sont :

- [modelisation-bloc2.md](/Users/beauvoir/Documents/New%20project/flask-staffy/docs/rncp/modelisation-bloc2.md)
- [dictionnaire-donnees.md](/Users/beauvoir/Documents/New%20project/flask-staffy/docs/rncp/dictionnaire-donnees.md)

Ces documents contiennent :

- UML ;
- MCD ;
- MLD / LMD ;
- MPD ;
- dictionnaire de donnees.

---

## 8. Front-end

### 8.1 Base graphique

Le design de la landing page a ete conserve depuis le Bloc 1 afin d'assurer une continute visuelle entre conception et developpement.

Choix retenus :

- landing page simple et lisible ;
- identite visuelle Staffly conservee ;
- typographie harmonisee ;
- calculateur marketing de gain de temps ;
- bouton "Demander une demo" relie a Tally.

### 8.2 Interfaces produites

Interfaces principales :

- landing page ;
- page d'inscription ;
- page de connexion ;
- dashboard ;
- page de taches ;
- formulaire de tache.

### 8.3 Approche UX

Le choix UX a ete de rester simple :

- navigation legere ;
- peu d'ecrans ;
- texte clair ;
- focalisation sur la tache et la demonstration ;
- limitation volontaire des fonctionnalites visibles.

Cette simplification est coherente avec un MVP court et plus facile a presenter.

### 8.4 Elements a integrer dans le dossier final

Il faudra ajouter :

- zoning ;
- wireframes ;
- mockups ;
- captures des interfaces finales.

---

## 9. Back-end

### 9.1 Framework retenu

Le back-end a ete developpe en Python avec Flask.

Pourquoi Flask :

- framework leger ;
- rapide a mettre en place ;
- adapte a un MVP ;
- compatible avec SQLAlchemy, Bcrypt et Railway.

### 9.2 Fonctionnalites serveur principales

Le back-end gere :

- l'inscription d'un manager ;
- la connexion ;
- la deconnexion ;
- l'acces protege au dashboard ;
- le CRUD des taches ;
- la generation de suggestions de taches ;
- l'integration avec MongoDB pour l'historique IA.

### 9.3 Composants metier

Les principaux composants metier du serveur sont :

- verification de la session manager ;
- chargement des taches du manager courant ;
- creation et modification des taches ;
- generation de suggestions via Hugging Face ou fallback local ;
- enregistrement de l'historique technique en MongoDB.

### 9.4 Interet pour le Bloc 2

Cette partie valide fortement :

- le developpement de composants metier cote serveur ;
- l'acces aux donnees SQL ;
- l'utilisation d'une base NoSQL ;
- la securisation des routes ;
- la preparation du deploiement.

---

## 10. Base de donnees

### 10.1 Base relationnelle : PostgreSQL

Le coeur des donnees metier est stocke en PostgreSQL.

Dans le MVP final, les tables principales mises en avant sont :

- `managers`
- `tasks`

Cette base permet de :

- stocker les comptes managers ;
- stocker les taches ;
- gerer les relations entre les donnees.

### 10.2 Base NoSQL : MongoDB

MongoDB est utilise pour :

- enregistrer l'historique technique des suggestions de taches generees ;
- montrer un usage NoSQL dans le projet ;
- stocker des donnees documentaires plus souples.

### 10.3 Choix SQL / NoSQL

Le choix retenu est le suivant :

- **PostgreSQL** pour les donnees relationnelles et structurees ;
- **MongoDB** pour les documents lies a l'IA.

Cette separation est logique et facile a justifier :

- les taches et les comptes managers sont fortement relationnels ;
- l'historique des suggestions IA est plus souple et semi-structure.

### 10.4 Modelisation

La modelisation detaillee est disponible dans :

- [modelisation-bloc2.md](/Users/beauvoir/Documents/New%20project/flask-staffy/docs/rncp/modelisation-bloc2.md)
- [dictionnaire-donnees.md](/Users/beauvoir/Documents/New%20project/flask-staffy/docs/rncp/dictionnaire-donnees.md)

---

## 11. Integrations externes : IA, Tally, Make

### 11.1 Hugging Face

L'application utilise une integration Hugging Face pour generer des suggestions de taches.

Logique :

- le manager saisit un contexte de service ;
- le back-end appelle un modele Hugging Face ;
- si le service externe ne repond pas, un mode fallback local genere des suggestions cohentes ;
- le resultat est affiche dans la page des taches.

### 11.2 Tally

Tally est utilise sur la landing page pour collecter les demandes de demonstration.

Avantages :

- mise en place rapide ;
- formulaire public ;
- pas besoin de redevelopper un formulaire complet cote back-end ;
- preuve d'integration no-code dans le projet.

### 11.3 Make

Make est connecte au formulaire Tally.

Scenario retenu :

1. un prospect remplit le formulaire ;
2. Tally transmet la reponse ;
3. Make recupere la nouvelle reponse ;
4. Make envoie automatiquement un email de notification.

### 11.4 Interet projet

Cette chaine permet de demontrer :

- une integration entre plusieurs outils ;
- une automatisation metier simple ;
- un lien concret entre la landing page et un usage reel.

---

## 12. Tests et qualite

### 12.1 Tests

Des tests ont ete ecrits avec Pytest pour verifier les parcours principaux :

- chargement de la landing page ;
- protection du dashboard ;
- protection de la page taches ;
- connexion manager ;
- inscription manager ;
- creation de tache ;
- generation de suggestions de taches.

### 12.2 Outils de qualite

Le projet inclut :

- `pytest`
- `flake8`
- `black`
- `pre-commit`

Ces outils permettent :

- de verifier la stabilite fonctionnelle ;
- de conserver un code propre ;
- de standardiser le style de code.

### 12.3 Interet pour le RNCP

Cette partie montre que le projet ne se limite pas a coder une fonctionnalite, mais s'inscrit dans une demarche qualite.

---

## 13. Securite et RGPD

Le detail complet est disponible dans :

- [securite-rgpd-deploiement.md](/Users/beauvoir/Documents/New%20project/flask-staffy/docs/rncp/securite-rgpd-deploiement.md)

### 13.1 Securite appliquee

Mesures deja implementees :

- mot de passe hashe avec Bcrypt ;
- variables d'environnement pour les secrets ;
- protection CSRF sur les formulaires ;
- routes protegees par session ;
- headers HTTP de securite ;
- controle d'appartenance des donnees.

### 13.2 RGPD

Le projet prend en compte :

- la limitation du perimetre de donnees ;
- la finalite des informations collectees ;
- la presence d'un consentement sur le formulaire Tally ;
- la separation entre donnees d'application et outils externes ;
- la possibilite de justifier les usages des donnees.

### 13.3 Positionnement

Le projet est un MVP. Il ne couvre pas toute la profondeur d'un produit final en production, mais il integre deja des bonnes pratiques solides et presentables.

---

## 14. Infrastructure et deploiement

### 14.1 Deploiement sur Railway

Railway a ete retenu pour deployer rapidement le projet.

Le deploiement comprend :

- un service web Flask ;
- une base PostgreSQL ;
- une base MongoDB ;
- des variables d'environnement ;
- un domaine public.

### 14.2 Configuration

Variables principales utilisees :

- `SECRET_KEY`
- `DATABASE_URL`
- `MONGO_URI`
- `MONGO_DB_NAME`
- `MONGO_COLLECTION_NAME`
- `HUGGING_FACE_API_TOKEN`
- `HUGGING_FACE_MODEL_URL`
- `TALLY_DEMO_URL`
- `SESSION_COOKIE_SECURE`

### 14.3 Procedure

Procedure suivie :

1. push du code sur GitHub ;
2. connexion du depot a Railway ;
3. ajout de PostgreSQL ;
4. ajout de MongoDB ;
5. configuration des variables ;
6. commande de demarrage `gunicorn app:app` ;
7. verification du site deploye ;
8. verification des integrations Tally et Make.

### 14.4 Resultat

Le projet est deploye et testable en ligne, ce qui renforce la valeur de la demonstration.

---

## 15. Bilan du projet

### 15.1 Resultats obtenus

Le projet Staffly permet aujourd'hui de presenter un MVP coherent :

- une landing page orientee conversion ;
- un formulaire de demande de demonstration ;
- une automatisation no-code fonctionnelle ;
- une application Flask avec authentification ;
- une gestion des taches ;
- une integration IA ;
- une base SQL ;
- une base NoSQL ;
- un deploiement Railway.

### 15.2 Difficultes rencontrees

Les principales difficultes ont ete :

- maintenir un perimetre realiste dans un delai court ;
- arbitrer entre richesse fonctionnelle et clarte du MVP ;
- integrer des outils externes sans alourdir le projet ;
- produire en parallele le code, la documentation et les livrables RNCP.

### 15.3 Choix de simplification

Pour garder un projet defendable :

- les sections employees et conges ont ete retirees de l'interface visible ;
- le coeur du MVP a ete recentre sur les taches ;
- les integrations externes ont ete limitees a une demonstration simple et fonctionnelle ;
- la modelisation a ete adaptee au perimetre reellement montre.

### 15.4 Evolutions possibles

Pour une version plus complete, les evolutions possibles sont :

- retour de la gestion visible des employes ;
- retour de la gestion des conges ;
- role et permissions plus avances ;
- notifications supplementaires ;
- tableaux de bord plus riches ;
- historique IA visible en interface ;
- fonction de planning plus poussee.

---

## 16. Annexes et captures a integrer

### 16.1 Captures fonctionnelles

- landing page Staffly ;
- bouton "Demander une demo" ;
- formulaire Tally ;
- page de connexion ;
- page d'inscription ;
- dashboard ;
- page des taches ;
- suggestion IA ;
- mail recu apres Make.

### 16.2 Captures techniques

- GitHub avec la branche et les commits ;
- Railway avec les services ;
- variables Railway ;
- base PostgreSQL Railway ;
- base MongoDB Railway ;
- code `app.py` ;
- tests Pytest.

### 16.3 Schémas

- UML Use Case Diagram ;
- MCD ;
- MLD / LMD ;
- MPD.

---

## Conclusion

Le projet Staffly montre la transformation d'une idee et d'une maquette initiale en une application web dynamique, testee, deployee et documentee. Le Bloc 2 a permis de construire une vraie base back-end securisee, en mobilisant a la fois des technologies relationnelles, NoSQL, des integrations externes, une logique metier serveur et une documentation technique compatible avec les attendus RNCP.

La force du projet tient dans sa clarte : plutot que de viser trop large, le perimetre a ete recentre pour produire un MVP simple, coherent, demonstrable et defendable a l'oral.

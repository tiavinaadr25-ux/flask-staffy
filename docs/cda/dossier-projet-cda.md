# Dossier projet CDA - Staffly

## 1. Presentation generale

### 1.1 Intitule du projet

Staffly est une application web SaaS destinee aux managers de restaurants.

### 1.2 Finalite

L'application aide a centraliser l'organisation quotidienne, creer et suivre
des taches, et generer des suggestions de taches avec une assistance IA.

### 1.3 Objectifs

- structurer les actions quotidiennes du manager ;
- limiter les oublis et la gestion informelle ;
- proposer un MVP evolutif vers une application CDA plus complete.

## 2. Competences CDA mobilisees

- installer et configurer son environnement de travail ;
- developper des interfaces utilisateur ;
- developper des composants metier ;
- contribuer a la gestion d'un projet informatique ;
- analyser les besoins et maquetter une application ;
- definir l'architecture logicielle ;
- concevoir et mettre en place une base relationnelle ;
- developper des composants SQL et NoSQL ;
- preparer et executer les plans de tests ;
- preparer et documenter le deploiement ;
- contribuer a la mise en production dans une demarche DevOps.

## 3. Besoin et perimetre

### 3.1 Constat

- les informations utiles sont dispersees ;
- les taches sont souvent gerees de maniere informelle ;
- le manager manque d'un outil simple de pilotage.

### 3.2 Perimetre retenu

- landing page ;
- inscription / connexion ;
- dashboard manager ;
- gestion des taches ;
- suggestion IA ;
- integration Tally / Make ;
- base SQL PostgreSQL ;
- historique IA MongoDB.

## 4. Conception fonctionnelle

### 4.1 Acteurs

- prospect ;
- manager ;
- services externes : Hugging Face, Tally, Make.

### 4.2 Cas d'utilisation principaux

- consulter la landing page ;
- demander une demo ;
- creer un compte ;
- se connecter ;
- consulter le dashboard ;
- creer, modifier et supprimer des taches ;
- generer des suggestions IA.

### 4.3 Maquettage

Documents a annexer :
- zoning ;
- wireframes ;
- mockups ;
- enchainement des ecrans.

## 5. Architecture technique

Le projet repose sur une architecture multicouche :

- couche presentation : templates Jinja / CSS / JS ;
- couche routes : Flask ;
- couche services : logique metier ;
- couche repositories : acces SQL ;
- couche modeles : SQLAlchemy ;
- couche NoSQL : MongoDB pour l'historique IA.

Document associe :
- `docs/cda/architecture-couches.md`

## 6. Base de donnees

### 6.1 Relationnel

Base principale :
- PostgreSQL

Entites :
- managers
- employees
- tasks
- leave_requests

### 6.2 NoSQL

Base secondaire :
- MongoDB

Collection :
- ai_suggestions

Documents associes :
- `docs/cda/base-donnees-migrations.md`
- `docs/rncp/modelisation-bloc2.md`
- `docs/rncp/dictionnaire-donnees.md`

## 7. Securite

Mesures deja presentes :
- hashage des mots de passe ;
- protection CSRF ;
- controle des acces par session ;
- isolation des donnees par manager ;
- headers HTTP de securite ;
- variables d'environnement ;
- cookies de session securises.

## 8. Tests

Le projet dispose :
- de tests Pytest ;
- d'un plan de tests ;
- d'une CI GitHub Actions ;
- d'un endpoint `/health`.

Documents associes :
- `docs/cda/plan-tests-cda.md`

## 9. Deploiement et DevOps

Le projet comprend :
- un `Procfile` pour Railway ;
- un `Dockerfile` ;
- un `docker-compose.yml` ;
- une CI GitHub Actions ;
- un `Makefile` pour les commandes frequentes.

Document associe :
- `docs/cda/devops-cda.md`

## 10. Accessibilite, eco-conception et veille

Le projet prend en compte :
- premiers renforcements RGAA ;
- principes de simplicite et legerete ;
- veille ANSSI / OWASP / CI / Flask.

Document associe :
- `docs/cda/accessibilite-eco-veille.md`

## 11. Limites actuelles

- audit accessibilite encore incomplet ;
- migrations presentes mais non encore testees en exploitation reelle locale ;
- couverture de tests encore perfectible ;
- deploiement continu encore partiel.

## 12. Pistes d'evolution

- gestion avancee des roles ;
- affectation d'employes aux taches dans l'interface ;
- tableaux de bord plus riches ;
- migrations automatisees dans la CI ;
- tests end-to-end ;
- meilleure observabilite en production.

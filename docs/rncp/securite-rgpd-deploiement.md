# Securite, RGPD et Deploiement - Staffly

## 1. Objectif du document

Ce document presente les choix retenus pour :

- la securite de l'application ;
- la conformite RGPD au niveau du MVP ;
- le deploiement de l'application sur Railway.

Le but est de montrer que le projet Staffly ne se limite pas a une interface, mais integre aussi des bonnes pratiques techniques et organisationnelles attendues dans le Bloc 2.

## 2. Securite appliquee dans le projet

### 2.1 Authentification manager

Le projet utilise une authentification par email et mot de passe.

Mesures appliquees :

- les mots de passe ne sont jamais stockes en clair ;
- les mots de passe sont hashes avec `Flask-Bcrypt` ;
- la connexion cree une session securisee cote serveur ;
- les pages du SaaS sont protegees par un decorateur `login_required`.

Concretement, cela permet de limiter l'acces a l'espace manager aux seuls utilisateurs authentifies.

### 2.2 Protection des formulaires

Tous les formulaires principaux de l'application utilisent un jeton CSRF.

Mesures appliquees :

- un token de securite est genere pour la session ;
- chaque formulaire envoie ce token ;
- le serveur verifie le token avant de traiter la requete ;
- une requete sans token ou avec un token invalide est rejetee.

Cela permet de limiter les attaques de type `Cross-Site Request Forgery`.

### 2.3 Gestion de session

La session est configuree avec des parametres de securite adaptes a un projet web :

- `SESSION_COOKIE_HTTPONLY=True`
- `SESSION_COOKIE_SAMESITE="Lax"`
- `SESSION_COOKIE_SECURE` active en production

Interet :

- `HttpOnly` empeche l'acces au cookie depuis du JavaScript malveillant ;
- `SameSite=Lax` limite certains usages frauduleux inter-sites ;
- `Secure` impose l'envoi du cookie uniquement en HTTPS.

### 2.4 Variables d'environnement

Les secrets et la configuration sensible ne sont pas ecrits en dur dans le code de production.

Variables utilisees :

- `SECRET_KEY`
- `DATABASE_URL`
- `MONGO_URI`
- `HUGGING_FACE_API_TOKEN`
- `HUGGING_FACE_MODEL_URL`
- `TALLY_DEMO_URL`
- `SESSION_COOKIE_SECURE`

Cela permet :

- de separer la configuration du code ;
- d'eviter de publier des secrets sur GitHub ;
- d'utiliser des valeurs differentes en local et en production.

### 2.5 Headers HTTP de securite

Le projet ajoute des headers HTTP simples :

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`

Ces headers reduisent plusieurs risques web classiques :

- interpretation incorrecte des contenus ;
- affichage du site dans une iframe externe ;
- fuite excessive du referer.

### 2.6 Controle d'acces aux donnees

Les routes metier verifient que les donnees manipulees appartiennent bien au manager connecte.

Exemples :

- une tache est chargee uniquement si elle appartient au bon manager ;
- les routes protegent l'acces par ID pour eviter qu'un utilisateur consulte les donnees d'un autre.

Cela renforce l'isolation des donnees entre comptes.

## 3. Limites actuelles de securite

Le projet est un MVP. Certaines mesures pourraient etre renforcees dans une version plus avancee :

- politique de mot de passe plus stricte ;
- limitation du nombre de tentatives de connexion ;
- journalisation securisee des connexions ;
- gestion plus avancee des roles et permissions ;
- politique de suppression automatique des anciennes donnees ;
- ajout eventuel d'un CSP plus complet.

Ces points peuvent etre presentes comme pistes d'amelioration futures.

## 4. RGPD - Donnees personnelles traitees

### 4.1 Donnees collectees dans l'application

Dans le MVP Staffly, les donnees personnelles traitees sont les suivantes :

#### Cote application Flask

- nom du manager ;
- nom du restaurant ;
- email du manager ;
- mot de passe hashe ;
- contenu des taches saisies ;
- prompts de suggestions IA relies a un compte manager ;
- historique technique des suggestions IA en MongoDB.

#### Cote formulaire Tally

- nom complet ;
- email professionnel ;
- nom du restaurant ;
- nombre d'employes ;
- besoin principal ;
- message libre ;
- consentement pour etre recontacte.

### 4.2 Finalite du traitement

Les donnees sont collectees pour des finalites precises :

- permettre la connexion et l'utilisation du SaaS ;
- permettre au manager de creer et suivre ses taches ;
- generer des suggestions IA utiles a l'organisation ;
- traiter les demandes de demonstration envoyees via la landing page ;
- envoyer un email de notification via Make.

### 4.3 Base legale

Dans le cadre du MVP, on peut presenter la base legale comme suit :

- **execution du service** pour les donnees necessaires au fonctionnement du compte manager ;
- **consentement** pour les demandes de demonstration envoyees via Tally.

### 4.4 Mesures RGPD visibles dans le projet

Mesures deja presentes ou justifiables :

- minimisation du perimetre fonctionnel du MVP ;
- variables d'environnement pour separer les secrets ;
- mot de passe hashe ;
- formulaire Tally avec case de consentement ;
- finalite simple et claire du formulaire de demo ;
- possibilite de supprimer ou anonymiser des donnees dans une evolution future.

### 4.5 Points a expliquer dans le dossier

Pour renforcer la partie RGPD dans le rapport, il faut preciser :

- quelles donnees sont collectees ;
- pourquoi elles sont collectees ;
- combien de temps elles sont conservees ;
- qui y a acces ;
- comment un utilisateur pourrait demander la suppression de ses donnees.

### 4.6 Formulation simple pour la soutenance

Exemple :

> Les donnees collectees dans Staffly sont limitees a ce qui est utile pour le fonctionnement du compte manager et pour le traitement des demandes de demonstration. Les mots de passe sont hashes, les secrets sont places en variables d'environnement, et le formulaire Tally inclut un consentement explicite pour le recontact.

## 5. Deploiement sur Railway

### 5.1 Choix de l'hebergement

Railway a ete retenu pour :

- deploiement rapide depuis GitHub ;
- gestion simple des variables d'environnement ;
- ajout facile de PostgreSQL ;
- ajout facile de MongoDB ;
- mise en ligne rapide pour la demonstration.

### 5.2 Architecture de deploiement

Le projet deploie :

- un service web Flask ;
- une base PostgreSQL ;
- une base MongoDB ;
- un formulaire Tally externe ;
- une automatisation Make externe.

### 5.3 Commande de demarrage

Le projet utilise :

```txt
gunicorn app:app
```

Le `Procfile` present dans le projet contient :

```txt
web: gunicorn app:app
```

### 5.4 Variables configurees sur Railway

Variables principales :

```txt
SECRET_KEY
DATABASE_URL
MONGO_URI
MONGO_DB_NAME
MONGO_COLLECTION_NAME
HUGGING_FACE_API_TOKEN
HUGGING_FACE_MODEL_URL
TALLY_DEMO_URL
SESSION_COOKIE_SECURE
```

Ces variables sont configurees dans Railway afin d'eviter de mettre des secrets dans le code.

### 5.5 Procedure de deploiement

Procedure simple a presenter :

1. Pousser le code sur GitHub.
2. Connecter le depot GitHub a Railway.
3. Selectionner la branche de deploiement.
4. Ajouter PostgreSQL dans Railway.
5. Ajouter MongoDB dans Railway.
6. Configurer les variables d'environnement.
7. Lancer le deploiement.
8. Generer le domaine public Railway.
9. Tester l'application en ligne.

### 5.6 Tests apres deploiement

Tests realises ou a presenter :

- ouverture de la landing page ;
- bouton `Demander une demo` ;
- inscription / connexion manager ;
- acces au dashboard ;
- creation d'une tache ;
- suggestion IA dans la page des taches ;
- verification du formulaire Tally ;
- verification de l'email automatique via Make.

## 6. Synthese pour le dossier RNCP

### Ce que le projet demontre deja

- securisation minimale mais reelle d'une application web ;
- usage d'une base relationnelle PostgreSQL ;
- usage d'une base NoSQL MongoDB ;
- deploiement d'une application Flask sur Railway ;
- integration d'un formulaire externe Tally ;
- automatisation no-code avec Make.

### Ce qu'il faut mettre en avant dans le rapport

- les choix de securite appliques ;
- les donnees personnelles traitees ;
- la justification RGPD du formulaire de demo ;
- l'architecture de deploiement ;
- les variables d'environnement ;
- les tests realises apres mise en ligne.

## 7. Captures a prevoir

Pour le dossier et la soutenance, il est recommande de prendre des captures de :

- la page de connexion ;
- les variables Railway ;
- le service PostgreSQL dans Railway ;
- le service MongoDB dans Railway ;
- la landing page avec le bouton Tally ;
- le formulaire Tally ;
- le scenario Make ;
- l'email automatique recu ;
- la page des taches avec suggestion IA ;
- la version deployee en ligne.

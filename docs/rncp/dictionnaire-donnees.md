# Dictionnaire de donnees - Staffly

## 1. Objet du document

Ce dictionnaire de donnees recense les donnees manipulees dans le MVP Staffly pour le Bloc 2.

Le projet repose sur :

- une base relationnelle PostgreSQL pour les donnees metier ;
- une base NoSQL MongoDB pour l'historique technique des suggestions IA ;
- un formulaire Tally pour les demandes de demonstration.

## 2. Perimetre retenu

Le MVP visible presente :

- la gestion d'un compte manager ;
- la gestion des taches ;
- la suggestion de taches avec IA ;
- la demande de demonstration via Tally ;
- l'automatisation Make apres soumission du formulaire.

Note :

- certaines structures comme `Employee` et `LeaveRequest` existent encore dans le code ;
- elles sont gardees comme base d'evolution ;
- elles ne sont pas au centre du MVP final affiche.

## 3. Conventions de lecture

- **Nom du champ** : nom technique du champ ou de l'attribut
- **Type** : type logique ou type SQL / NoSQL
- **Obligatoire** : indique si la valeur doit etre renseignee
- **Exemple** : exemple de valeur possible
- **Description** : role du champ dans l'application

## 4. Base relationnelle PostgreSQL

### 4.1 Table `managers`

| Nom du champ | Type | Obligatoire | Exemple | Description |
|---|---|---:|---|---|
| `id` | `SERIAL` / `Integer` | Oui | `1` | Identifiant unique du manager |
| `full_name` | `VARCHAR(120)` | Oui | `Tia Manager` | Nom complet du manager |
| `restaurant_name` | `VARCHAR(120)` | Oui | `Staffly Bistro` | Nom du restaurant ou de l'etablissement |
| `email` | `VARCHAR(120)` | Oui | `manager@staffly.com` | Email de connexion du manager |
| `password_hash` | `VARCHAR(255)` | Oui | `"$2b$12$..."` | Mot de passe hashe |
| `created_at` | `TIMESTAMPTZ` | Oui | `2026-04-15 09:30:00+00` | Date de creation du compte |

### 4.2 Table `tasks`

| Nom du champ | Type | Obligatoire | Exemple | Description |
|---|---|---:|---|---|
| `id` | `SERIAL` / `Integer` | Oui | `12` | Identifiant unique de la tache |
| `manager_id` | `INTEGER` | Oui | `1` | Cle etrangere vers le manager proprietaire |
| `employee_id` | `INTEGER` | Non | `4` | Champ prevu dans le code pour une extension future d'assignation |
| `title` | `VARCHAR(140)` | Oui | `Preparer la salle avant le service` | Titre de la tache |
| `description` | `TEXT` | Non | `Verifier les tables, les couverts et la terrasse.` | Description detaillee de la tache |
| `status` | `VARCHAR(40)` | Oui | `todo` | Etat de la tache (`todo`, `in_progress`, `done`) |
| `due_date` | `DATE` | Non | `2026-04-16` | Date limite de realisation |
| `created_at` | `TIMESTAMPTZ` | Oui | `2026-04-15 10:00:00+00` | Date de creation de la tache |

### 4.3 Regles relationnelles SQL

| Regle | Description |
|---|---|
| `managers.id` | Cle primaire de la table `managers` |
| `tasks.id` | Cle primaire de la table `tasks` |
| `tasks.manager_id -> managers.id` | Une tache appartient a un manager |
| `tasks.employee_id -> employees.id` | Liaison deja prevue dans le code, reservee a une version future |

## 5. Base NoSQL MongoDB

### 5.1 Collection `ai_suggestions`

| Nom du champ | Type | Obligatoire | Exemple | Description |
|---|---|---:|---|---|
| `_id` | `ObjectId` | Oui | `67fa0d2c...` | Identifiant technique MongoDB |
| `manager_email` | `String` | Oui | `manager@staffly.com` | Email du manager ayant lance la suggestion |
| `manager_name` | `String` | Oui | `Tia Manager` | Nom du manager |
| `restaurant_name` | `String` | Oui | `Staffly` | Nom du restaurant rattache a la suggestion |
| `prompt` | `String` | Oui | `service du midi avec terrasse` | Contexte saisi par le manager |
| `suggestions` | `Array[String]` | Oui | `["Lancer la mise en place...", "Preparer la terrasse..."]` | Liste des suggestions generees |
| `source` | `String` | Oui | `hugging_face` | Source de generation (`hugging_face` ou `fallback`) |
| `created_at` | `DateTime` / `String` | Oui | `2026-04-15T10:30:00+00:00` | Date de generation de la suggestion |

### 5.2 Utilite metier de la collection

Cette collection sert a :

- conserver une trace des generations IA ;
- demontrer l'usage d'une base NoSQL dans le projet ;
- garder un historique technique des prompts et des reponses.

## 6. Formulaire Tally - Demande de demonstration

### 6.1 Donnees collectees

| Nom du champ | Type | Obligatoire | Exemple | Description |
|---|---|---:|---|---|
| `full_name` | `String` | Oui | `Camille Martin` | Nom complet du prospect |
| `professional_email` | `Email` | Oui | `camille@restaurant.fr` | Email de contact professionnel |
| `restaurant_name` | `String` | Oui | `Le Comptoir de Paris` | Nom du restaurant concerne |
| `employee_count` | `String` ou `Number` | Non | `8` | Nombre d'employes ou taille de l'equipe |
| `main_need` | `String` | Non | `Mieux organiser les taches` | Besoin principal exprime par le prospect |
| `message` | `Text` | Non | `Je souhaite voir comment Staffly peut m'aider pendant le service du midi.` | Message libre laisse par le prospect |
| `consent` | `Boolean` | Oui | `true` | Consentement pour etre recontacte |

### 6.2 Utilisation de ces donnees

Ces donnees servent a :

- traiter une demande de demonstration ;
- declencher une automatisation Make ;
- envoyer un email de notification ou de suivi.

## 7. Annexe - Donnees deja presentes dans le code

Les elements ci-dessous existent dans le code actuel mais ne sont pas au centre du MVP final.

### 7.1 Table `employees`

| Nom du champ | Type | Obligatoire | Exemple | Description |
|---|---|---:|---|---|
| `id` | `SERIAL` / `Integer` | Oui | `4` | Identifiant unique de l'employe |
| `manager_id` | `INTEGER` | Oui | `1` | Cle etrangere vers le manager |
| `full_name` | `VARCHAR(120)` | Oui | `Aina Rakoto` | Nom complet de l'employe |
| `role_title` | `VARCHAR(120)` | Oui | `Chef de rang` | Poste ou fonction |
| `email` | `VARCHAR(120)` | Oui | `aina@staffly.com` | Email de l'employe |
| `phone` | `VARCHAR(40)` | Oui | `+33 6 11 22 33 44` | Telephone |
| `status` | `VARCHAR(40)` | Oui | `active` | Statut de l'employe |
| `created_at` | `TIMESTAMPTZ` | Oui | `2026-04-15 11:00:00+00` | Date de creation |

### 7.2 Table `leave_requests`

| Nom du champ | Type | Obligatoire | Exemple | Description |
|---|---|---:|---|---|
| `id` | `SERIAL` / `Integer` | Oui | `3` | Identifiant unique de la demande |
| `manager_id` | `INTEGER` | Oui | `1` | Cle etrangere vers le manager |
| `employee_id` | `INTEGER` | Oui | `4` | Cle etrangere vers l'employe |
| `start_date` | `DATE` | Oui | `2026-04-20` | Date de debut du conge |
| `end_date` | `DATE` | Oui | `2026-04-22` | Date de fin du conge |
| `reason` | `TEXT` | Non | `Rendez-vous medical` | Motif de la demande |
| `status` | `VARCHAR(40)` | Oui | `pending` | Statut de la demande |
| `created_at` | `TIMESTAMPTZ` | Oui | `2026-04-15 11:10:00+00` | Date de creation |

## 8. Synthese

Le dictionnaire de donnees du projet Staffly montre :

- une base SQL simple et structuree pour le coeur metier ;
- une base NoSQL pour les donnees souples de l'IA ;
- un flux externe Tally / Make pour la partie prospection et demonstration ;
- un MVP centre sur les taches, mais deja prepare pour des extensions futures.

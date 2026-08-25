# Base de donnees et migrations - Staffly

## 1. Objectif

Cette note formalise la gestion de schema de base de donnees au niveau CDA.
Le projet ne repose plus uniquement sur `db.create_all()`, mais dispose aussi
d'une base de migrations versionnees.

## 2. Outil retenu

- `Alembic`

Pourquoi :
- versionner l'evolution du schema relationnel ;
- tracer les modifications de structure ;
- faciliter le passage entre environnements ;
- disposer d'une preuve technique attendue dans un contexte CDA.

## 3. Fichiers ajoutes

- `alembic.ini`
- `migrations/env.py`
- `migrations/script.py.mako`
- `migrations/versions/20260825_01_initial_staffly_schema.py`

## 4. Premiere migration

La migration initiale cree :
- `managers`
- `employees`
- `tasks`
- `leave_requests`

Elle couvre donc le perimetre relationnel complet actuellement code dans
les modeles SQLAlchemy.

## 5. Scripts SQL conserves

Le projet conserve aussi des scripts SQL dans `database/` :

- `init_local_postgres.sql`
- `schema_postgresql.sql`
- `test_fixture_postgresql.sql`

Cette double approche est utile pour le CDA :
- scripts SQL lisibles pour le dossier ;
- migrations versionnees pour la pratique professionnelle.

## 6. Commandes utiles

Apres installation des dependances :

```bash
make migration-current
make migration-upgrade
make migration-downgrade
```

Ou directement :

```bash
python -m alembic upgrade head
```

## 7. Valeur pour le CDA

Cette partie permet de montrer :
- la conception d'une base relationnelle ;
- la gestion maitrisee de son evolution ;
- la preparation d'environnements coherents entre local, test et production ;
- une pratique plus professionnelle de la persistence des donnees.

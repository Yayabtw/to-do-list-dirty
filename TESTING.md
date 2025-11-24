# Guide de Test et Qualité du Code

## Linter (Ruff)

### Installation
```bash
pipenv install --dev
```

### Exécution
```bash
pipenv run ruff check .
```

### Auto-fix
```bash
pipenv run ruff check --fix .
```

## Tests

### Lancer tous les tests
```bash
pipenv run python manage.py test tasks.tests
```

### Tests spécifiques
```bash
# Test des vues
pipenv run python manage.py test tasks.tests.TaskViewsTestCase

# Test du modèle
pipenv run python manage.py test tasks.tests.TaskModelTestCase

# Test de l'import du dataset
pipenv run python manage.py test tasks.tests.DatasetImportTestCase
```

## Couverture de Tests

### Générer le rapport de couverture
```bash
pipenv run coverage run --source='.' manage.py test tasks.tests
pipenv run coverage report
```

### Générer un rapport HTML
```bash
pipenv run coverage html
```

Le rapport HTML sera disponible dans `htmlcov/index.html`.

### Générer un rapport XML (pour les IDE)
```bash
pipenv run coverage xml
```

## Visualisation de la Couverture dans VSCode

1. Installer l'extension "Coverage Gutters" dans VSCode
2. Générer le rapport de couverture XML : `pipenv run coverage xml`
3. Cliquer sur "Watch" dans la barre de statut VSCode
4. Les lignes non testées seront surlignées en rouge dans l'éditeur

## Dataset de Test

### Importer le dataset
```bash
pipenv run python manage.py loaddata dataset.json
```

### Exporter des données
```bash
pipenv run python manage.py dumpdata tasks.task --indent 2 > dataset.json
```

## Tests Multi-Versions

### Avec Tox
```bash
pipenv install --dev tox
pipenv run tox
```

### Avec le script shell
```bash
./test_multi_versions.sh
```

Ce script teste l'application avec :
- Python 3.9 + Django 3.2
- Python 3.9 + Django 4.2
- Python 3.13 + Django 4.2
- Python 3.13 + Django 5.0

**Note**: Python 2.7 n'est plus supporté par Django depuis la version 2.0.

## Script de Build

Le script `build.sh` intègre automatiquement :
1. Vérification du linter
2. Mise à jour de la version
3. Commit et tag Git
4. Création d'une archive

### Utilisation
```bash
./build.sh version=1.2.0
```

Le build échouera si le linter détecte des erreurs.

## Résumé des Commandes Rapides

```bash
# Installer les dépendances
pipenv install --dev

# Linter
pipenv run ruff check .

# Tests
pipenv run python manage.py test tasks.tests

# Couverture
pipenv run coverage run --source='.' manage.py test tasks.tests && pipenv run coverage report

# Build
./build.sh version=1.2.0
```

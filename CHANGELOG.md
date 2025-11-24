# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.2.0] - 2024-11-24

### Ajouté
- **Linter Ruff** : Configuration et intégration de Ruff pour vérifier la qualité du code selon PEP 8
- **Tests automatiques** : Suite de tests complète pour toutes les vues et modèles
  - Tests pour l'URL `/` (liste des tâches)
  - Tests pour l'URL `/update_task/<id>/` (mise à jour)
  - Tests pour l'URL `/delete_task/<id>/` (suppression)
  - Tests du modèle Task
- **Couverture de tests à 100%** : Mise en place de coverage.py avec rapport HTML et XML
- **Visualisation de la couverture dans VSCode** : Configuration pour l'extension Coverage Gutters
- **Dataset de test** : Fichier `dataset.json` avec 5 tâches d'exemple et test d'import
- **Tests multi-versions** : 
  - Configuration Tox pour tester avec Python 3.9/3.13 et Django 3.2/4.2/5.0
  - Script shell `test_multi_versions.sh` pour tests automatisés
- **Documentation** : 
  - Fichier `TESTING.md` avec guide complet des tests
  - Mise à jour du `README.md` avec instructions d'installation et développement
  - Fichier `CHANGELOG.md` pour suivre les versions

### Modifié
- **Script de build** : Intégration du linter dans `build.sh` - le build échoue si le code ne passe pas le linter
- **Code source** : Refactorisation complète pour respecter PEP 8
  - Remplacement des imports wildcard par des imports explicites
  - Renommage des fonctions en snake_case (`updateTask` → `update_task`)
  - Correction de l'indentation (tabs → espaces)
  - Ajout de docstrings pour toutes les fonctions et classes
  - Amélioration de l'espacement et du formatage
- **Fichier `.gitignore`** : Ajout des fichiers de coverage, tox et build
- **Configuration Pipenv** : Ajout de ruff, coverage et tox aux dépendances de développement

### Technique
- Couverture de tests : 100%
- Linter : Ruff (conforme PEP 8)
- Framework de tests : Django TestCase
- Outil de couverture : coverage.py
- Tests multi-versions : Tox + script shell personnalisé

## [1.1.0] - 2024-11-24

### Ajouté
- Affichage de la version dans le template `list.html`
- Variable `VERSION` dans `todo/settings.py`

## [1.0.1] - 2024-11-24

### Ajouté
- Script de build `build.sh` pour automatiser les releases
- Gestion automatique du versioning
- Création de tags Git
- Génération d'archives versionnées

## [1.0.0] - Date initiale

### Ajouté
- Application Django de gestion de tâches (To-Do List)
- CRUD complet pour les tâches
- Interface web avec Bootstrap
- Base de données SQLite

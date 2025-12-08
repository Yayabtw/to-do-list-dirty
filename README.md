# to-do-list app
To-Do-List application built with django to Create, Update and Delete tasks.
<br>
<br>
![todolist](https://user-images.githubusercontent.com/65074901/125083144-a5e03900-e0e5-11eb-9092-da716a30a5f3.JPG)

## Gestion des commits

Nous utilisons la convention **Conventional Commits** pour nommer nos commits.

Format général :

`type(scope): message clair au présent`

Exemples de types utilisés :

- `feat` : ajout d’une nouvelle fonctionnalité  
- `fix` : correction de bug  
- `docs` : modification de la documentation  
- `refactor` : refonte du code sans changement de comportement  
- `test` : ajout ou modification de tests  
- `chore` : tâches diverses (config, dépendances, etc.)

Exemples :

- `feat(auth): ajouter la connexion par Google`
- `fix(api): corriger l’erreur 500 sur /users`
- `docs: mettre à jour le README`

Cette convention permet d’avoir un historique de commits lisible, de faciliter la génération de changelog et d’automatiser les versions.

---

## Gestion des versions

Nous utilisons la version sémantique (**Semantic Versioning / SemVer**), au format :

`MAJEURE.MINEURE.CORRECTIVE` (ex : `1.4.2`)

- **MAJEURE** : changement incompatible avec les versions précédentes  
  - Ex : `1.0.0` → `2.0.0`
- **MINEURE** : ajout de fonctionnalités rétro-compatibles  
  - Ex : `1.2.0` → `1.3.0`
- **CORRECTIVE** : corrections de bugs rétro-compatibles  
  - Ex : `1.2.3` → `1.2.4`

Les numéros de version sont mis à jour en fonction des changements introduits dans le projet, afin de refléter clairement l’impact pour les utilisateurs et les développeurs.

---

## Installation et Développement

### Prérequis
- Python 3.9 ou supérieur
- pipenv
- Node.js et npm (pour les tests d'accessibilité)

### Installation
```bash
# Installer les dépendances Python
pipenv install --dev

# Installer les dépendances Node.js (pour les tests d'accessibilité)
npm install

# Appliquer les migrations
pipenv run python manage.py migrate

# Charger le dataset de test (optionnel)
pipenv run python manage.py loaddata tasks/fixtures/dataset.json

# Lancer le serveur de développement
pipenv run python manage.py runserver
```

### Qualité du Code

Le projet utilise **Ruff** comme linter pour garantir la qualité du code selon PEP 8.

```bash
# Vérifier le code
pipenv run ruff check .

# Corriger automatiquement les erreurs
pipenv run ruff check --fix .
```

### Tests

Le projet dispose d'une suite de tests complète avec **100% de couverture**.

```bash
# Lancer les tests
pipenv run python manage.py test tasks.tests

# Générer le rapport de couverture
pipenv run coverage run --source='.' manage.py test tasks.tests
pipenv run coverage report
pipenv run coverage html
```

Pour plus de détails sur les tests, voir [TESTING.md](TESTING.md).

### Accessibilité

L'application est conforme au standard **WCAG 2.1 niveau A**.

```bash
# Lancer les tests d'accessibilité
# (le serveur Django doit être en cours d'exécution)
./scripts/test_accessibility.sh
```

Pour plus de détails, voir [ACCESSIBILITY.md](ACCESSIBILITY.md).

### Build et Release

```bash
# Créer une nouvelle version
./scripts/build.sh version=X.Y.Z
```

Le script de build :
1. Vérifie que le code passe le linter
2. Vérifie la conformité WCAG 2.1 niveau A (accessibilité)
3. Met à jour la version dans `settings.py`
4. Crée un commit et un tag Git
5. Génère une archive versionnée
# FAQ - Tests d'Accessibilité

## ❓ pa11y n'existe pas sur pip, comment l'ajouter au Pipfile ?

### Réponse courte

**pa11y n'est PAS un package Python**, c'est un outil Node.js. Il ne peut donc pas être ajouté au `Pipfile`.

### Pourquoi ?

pa11y est écrit en JavaScript et utilise Puppeteer (navigateur Chrome headless) pour tester l'accessibilité. C'est un choix technique qui le rend plus performant et fiable.

### Solutions

#### ✅ Solution 1 : Garder pa11y (RECOMMANDÉ)

**C'est la solution actuelle du projet.**

**Prérequis :**
- Node.js et npm installés

**Installation :**
```bash
npm install
```

**Utilisation :**
```bash
./test_accessibility.sh
```

**Avantages :**
- ✅ Standard de l'industrie
- ✅ Plus performant
- ✅ Meilleur support
- ✅ Utilisé par de nombreux projets Django

**Fichiers concernés :**
- `package.json` : Dépendances Node.js
- `.pa11yci.json` : Configuration
- `test_accessibility.sh` : Script de test

---

#### 🐍 Solution 2 : Alternative Python pure

Si vous ne pouvez vraiment pas installer Node.js, utilisez `axe-selenium-python`.

**Installation :**

1. Décommenter dans `Pipfile` :
```toml
[dev-packages]
axe-selenium-python = "*"
selenium = "*"
```

2. Installer :
```bash
pipenv install --dev
```

**Utilisation :**
```bash
pipenv run python test_accessibility_python.py
```

**Avantages :**
- ✅ 100% Python
- ✅ Pas besoin de Node.js

**Inconvénients :**
- ⚠️ Moins utilisé
- ⚠️ Plus lent
- ⚠️ Nécessite Chrome/Chromium

---

## ❓ Pourquoi mélanger Python et Node.js ?

C'est une pratique **très courante** dans les projets web modernes :

### Exemples de projets Django utilisant Node.js

1. **Django lui-même** : Utilise npm pour les outils de build
2. **Wagtail CMS** : Utilise npm pour le frontend
3. **Django REST framework** : Documentation avec npm
4. **Sentry** : Utilise npm pour les assets

### Outils Node.js couramment utilisés avec Django

- **Webpack** : Bundler JavaScript
- **Tailwind CSS** : Framework CSS
- **ESLint** : Linter JavaScript
- **Prettier** : Formateur de code
- **pa11y** : Tests d'accessibilité ← Nous sommes ici

### Séparation des responsabilités

```
Python (Backend)          Node.js (Outils)
├── Django               ├── pa11y (tests a11y)
├── Tests unitaires      ├── Webpack (build)
├── Ruff (linter)        ├── Prettier (format)
└── Coverage             └── ESLint (linter JS)
```

---

## ❓ Comment gérer les dépendances ?

### Dépendances Python (Pipfile)

```toml
[packages]
django = "*"

[dev-packages]
ruff = "*"
coverage = "*"
tox = "*"
```

**Installation :**
```bash
pipenv install --dev
```

### Dépendances Node.js (package.json)

```json
{
  "devDependencies": {
    "pa11y": "^6.2.3",
    "pa11y-ci": "^3.0.1"
  }
}
```

**Installation :**
```bash
npm install
```

### Les deux sont nécessaires

```bash
# Installation complète
pipenv install --dev  # Python
npm install           # Node.js
```

---

## ❓ Comment ça marche dans le CI/CD ?

### GitHub Actions (exemple)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      # Python
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      
      - name: Install Python dependencies
        run: |
          pip install pipenv
          pipenv install --dev
      
      # Node.js
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install Node dependencies
        run: npm install
      
      # Tests
      - name: Run Django tests
        run: pipenv run python manage.py test
      
      - name: Run accessibility tests
        run: |
          pipenv run python manage.py runserver &
          sleep 5
          ./test_accessibility.sh
```

---

## ❓ Puis-je utiliser uniquement Python ?

**Oui**, avec `axe-selenium-python`, mais ce n'est **pas recommandé** pour ce projet.

### Pourquoi pa11y est meilleur ?

| Critère | pa11y | axe-selenium-python |
|---------|-------|---------------------|
| Performance | ⚡ Rapide | 🐢 Lent |
| Popularité | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Maintenance | ✅ Active | ✅ Active |
| CI/CD | ✅ Simple | ⚠️ Complexe |
| Dépendances | Node.js | Chrome + Selenium |

### Cas d'usage pour axe-selenium-python

- Vous ne pouvez vraiment pas installer Node.js
- Vous voulez intégrer aux tests Django
- Vous avez déjà Selenium

---

## ❓ Dois-je commiter node_modules/ ?

**NON !** ❌

Le fichier `.gitignore` exclut déjà :
```
node_modules/
package-lock.json
```

**À commiter :**
- ✅ `package.json` : Liste des dépendances
- ✅ `.pa11yci.json` : Configuration
- ❌ `node_modules/` : Dossier des packages (généré)

**Sur un nouveau poste :**
```bash
git clone <repo>
npm install  # Recrée node_modules/
```

---

## ❓ Résumé : Que dois-je faire ?

### Pour utiliser le projet (recommandé)

```bash
# 1. Cloner le projet
git clone <repo>
cd to-do-list-dirty

# 2. Installer Python
pipenv install --dev

# 3. Installer Node.js
npm install

# 4. Lancer les tests
pipenv run python manage.py runserver &
./test_accessibility.sh
```

### Pour utiliser uniquement Python (alternative)

```bash
# 1. Modifier Pipfile (décommenter axe-selenium-python)

# 2. Installer
pipenv install --dev

# 3. Lancer les tests
pipenv run python manage.py runserver &
pipenv run python test_accessibility_python.py
```

---

## 📚 Ressources

- [ACCESSIBILITY_TOOLS.md](ACCESSIBILITY_TOOLS.md) : Comparaison détaillée
- [ACCESSIBILITY.md](ACCESSIBILITY.md) : Guide complet
- [pa11y Documentation](https://github.com/pa11y/pa11y)
- [axe-selenium-python](https://github.com/mozilla-services/axe-selenium-python)

---

## ✅ Conclusion

**pa11y (Node.js) est la solution recommandée** pour ce projet car :
- C'est le standard de l'industrie
- Plus performant et fiable
- Bien maintenu et documenté
- Facile à intégrer au CI/CD

**L'alternative Python existe** mais est moins optimale pour les tests d'accessibilité.

**Mélanger Python et Node.js** est une pratique courante et professionnelle dans les projets web modernes.

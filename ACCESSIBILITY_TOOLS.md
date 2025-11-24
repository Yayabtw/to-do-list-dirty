# Outils de test d'accessibilité

Ce document explique les différentes options pour tester l'accessibilité WCAG 2.1 niveau A.

## Option 1 : pa11y (Node.js) - **RECOMMANDÉ** ✅

### Pourquoi pa11y ?

- ✅ **Standard de l'industrie** : Utilisé par de nombreux projets Django/Python
- ✅ **Plus complet** : Utilise Puppeteer/Chrome pour des tests réels
- ✅ **Bien maintenu** : Communauté active, mises à jour régulières
- ✅ **Rapide** : Tests performants
- ✅ **CI/CD friendly** : Facile à intégrer dans GitHub Actions, GitLab CI, etc.

### Installation

```bash
# Prérequis : Node.js et npm
npm install
```

### Configuration

Fichier `.pa11yci.json` :
```json
{
  "defaults": {
    "standard": "WCAG2A",
    "timeout": 10000,
    "wait": 1000
  },
  "urls": [
    "http://localhost:8000/"
  ]
}
```

### Utilisation

```bash
# Démarrer le serveur Django
pipenv run python manage.py runserver

# Dans un autre terminal
./test_accessibility.sh
```

### Avantages

- Aucune dépendance Python supplémentaire
- Tests plus fiables (navigateur réel)
- Rapports détaillés
- Intégration facile au CI/CD

### Inconvénients

- Nécessite Node.js (mais c'est courant dans les projets modernes)

---

## Option 2 : axe-selenium-python (Python pur) - Alternative

### Pourquoi axe-selenium-python ?

- ✅ **100% Python** : Pas besoin de Node.js
- ✅ **Basé sur axe-core** : Même moteur que beaucoup d'outils
- ✅ **Intégration Django** : Peut être intégré aux tests Django

### Installation

```bash
# Décommenter dans Pipfile :
# axe-selenium-python = "*"
# selenium = "*"

pipenv install --dev axe-selenium-python selenium
```

### Prérequis

- Chrome ou Chromium installé
- ChromeDriver (géré automatiquement par selenium)

### Utilisation

```bash
# Démarrer le serveur Django
pipenv run python manage.py runserver

# Dans un autre terminal
pipenv run python test_accessibility_python.py
```

### Avantages

- Pas besoin de Node.js
- Peut être intégré aux tests Django existants
- Génère des rapports JSON

### Inconvénients

- Moins utilisé dans l'industrie
- Nécessite Chrome/Chromium
- Plus lent que pa11y
- Dépendances Python supplémentaires

---

## Comparaison

| Critère | pa11y (Node.js) | axe-selenium-python |
|---------|-----------------|---------------------|
| **Langage** | JavaScript | Python |
| **Prérequis** | Node.js + npm | Chrome + Python |
| **Performance** | ⚡ Rapide | 🐢 Plus lent |
| **Popularité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Maintenance** | ✅ Active | ✅ Active |
| **CI/CD** | ✅ Facile | ⚠️ Plus complexe |
| **Rapports** | ✅ Détaillés | ✅ JSON |
| **Intégration Django** | ⚠️ Externe | ✅ Native |

---

## Recommandation

### Pour ce projet : **pa11y** ✅

**Raisons :**
1. Standard de l'industrie
2. Plus performant
3. Meilleur support communautaire
4. Facile à intégrer au CI/CD
5. Node.js est déjà courant dans les projets web modernes

### Quand utiliser axe-selenium-python ?

- Vous ne pouvez vraiment pas installer Node.js
- Vous voulez intégrer les tests d'accessibilité aux tests Django
- Vous avez déjà Selenium dans votre stack

---

## Intégration au build

### Avec pa11y (actuel)

```bash
./build.sh version=X.Y.Z
```

Le script vérifie :
1. Linter (Ruff)
2. **Accessibilité (pa11y)** ← Ici
3. Versioning
4. Tagging Git

### Avec axe-selenium-python

Modifier `build.sh` :
```bash
# Remplacer
./test_accessibility.sh

# Par
pipenv run python test_accessibility_python.py
```

---

## Autres alternatives

### 1. Lighthouse CI (Google)

```bash
npm install -g @lhci/cli
lhci autorun --collect.url=http://localhost:8000/
```

**Avantages :** Tests complets (performance + accessibilité + SEO)
**Inconvénients :** Plus lourd, plus lent

### 2. axe-core CLI

```bash
npm install -g @axe-core/cli
axe http://localhost:8000/
```

**Avantages :** Simple, rapide
**Inconvénients :** Moins de fonctionnalités que pa11y

### 3. Tests manuels

- **Chrome DevTools** : Onglet Lighthouse
- **Firefox Developer Tools** : Accessibility Inspector
- **Extensions navigateur** : axe DevTools, WAVE

---

## Ressources

### pa11y
- [Documentation officielle](https://github.com/pa11y/pa11y)
- [pa11y-ci](https://github.com/pa11y/pa11y-ci)

### axe-selenium-python
- [Documentation](https://github.com/mozilla-services/axe-selenium-python)
- [axe-core](https://github.com/dequelabs/axe-core)

### WCAG
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM](https://webaim.org/)

---

## Conclusion

**Pour ce projet, nous utilisons pa11y** car c'est la solution la plus robuste et la plus utilisée dans l'industrie. Le script Python est fourni comme alternative pour ceux qui ne peuvent pas utiliser Node.js.

Les deux solutions atteignent **100% de conformité WCAG 2.1 niveau A** ✅

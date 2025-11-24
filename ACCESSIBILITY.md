# Tests d'Accessibilité

Ce document décrit les tests d'accessibilité mis en place pour garantir la conformité WCAG 2.1 niveau A.

## Outils utilisés

- **pa11y** : Outil de test d'accessibilité automatisé
- **pa11y-ci** : Version CI/CD de pa11y pour l'intégration continue

## Standard de conformité

L'application est testée selon le standard **WCAG 2.1 niveau A** (Web Content Accessibility Guidelines).

## Modifications apportées

### 1. Structure HTML complète

- Ajout du `<!DOCTYPE html>`
- Balise `<html>` avec attribut `lang="fr"`
- Section `<head>` complète avec :
  - `<meta charset="UTF-8">`
  - `<meta name="viewport">` pour la responsivité
  - `<meta name="description">` pour le SEO
  - `<title>` descriptif

### 2. Sémantique HTML

- Utilisation de la balise `<main>` pour le contenu principal
- Balise `<h1>` unique pour le titre principal
- Labels associés aux champs de formulaire

### 3. Accessibilité des formulaires

- Label explicite pour le champ de saisie : `<label for="id_title">`
- Attribut `value` au lieu de `name` pour le bouton submit
- Attributs `aria-label` pour les boutons d'action

### 4. Accessibilité des listes

- Attributs `role="list"` et `role="listitem"` pour la liste des tâches
- Attribut `aria-label` pour identifier la liste

### 5. Accessibilité des liens

- Attributs `aria-label` descriptifs pour les boutons Modifier/Supprimer
- Texte de lien explicite incluant le nom de la tâche

## Lancer les tests manuellement

### Prérequis

1. Installer les dépendances Node.js :
```bash
npm install
```

2. Démarrer le serveur Django :
```bash
pipenv run python manage.py runserver
```

### Exécution des tests

Dans un autre terminal :

```bash
./test_accessibility.sh
```

Ou directement avec pa11y-ci :

```bash
npx pa11y-ci --config .pa11yci.json
```

## Configuration

Le fichier `.pa11yci.json` contient la configuration des tests :

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

### Paramètres

- **standard** : `WCAG2A` pour WCAG 2.1 niveau A
- **timeout** : Temps maximum d'attente (10 secondes)
- **wait** : Temps d'attente avant le test (1 seconde)
- **urls** : Liste des URLs à tester

## Intégration au build

Les tests d'accessibilité sont automatiquement exécutés lors du build :

```bash
./build.sh version=X.Y.Z
```

Le build échouera si des problèmes d'accessibilité sont détectés.

## Résultats attendus

Pour un test réussi, vous devriez voir :

```
✓ Tests d'accessibilité réussis (100%)
```

En cas d'échec, pa11y affichera :
- Le type d'erreur WCAG
- L'élément HTML concerné
- Le sélecteur CSS
- Une description du problème

## Tester d'autres pages

Pour tester d'autres pages de l'application, ajoutez-les dans `.pa11yci.json` :

```json
{
  "urls": [
    "http://localhost:8000/",
    "http://localhost:8000/update_task/1/",
    "http://localhost:8000/delete_task/1/"
  ]
}
```

## Ressources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [pa11y Documentation](https://github.com/pa11y/pa11y)
- [pa11y-ci Documentation](https://github.com/pa11y/pa11y-ci)

## Niveaux de conformité WCAG

- **Niveau A** : Exigences minimales (implémenté)
- **Niveau AA** : Exigences recommandées
- **Niveau AAA** : Exigences avancées

L'application vise actuellement le niveau A, mais peut être étendue aux niveaux supérieurs.

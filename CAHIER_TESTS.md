# Cahier de Tests - To-Do List Application

Ce document décrit les 15 tests essentiels à réaliser à chaque modification de l'application.

## Légende

- **[AUTO]** : Test automatisé (via Django test framework)
- **[MANUEL]** : Test manuel nécessitant une interaction humaine
- **[VISUEL]** : Contrôle visuel de l'interface
- **[ACCESSIBILITE]** : Test d'accessibilité automatisé (pa11y)

---

## 1. [AUTO] Test d'affichage de la liste des tâches
**Fichier**: `tasks/tests.py:15` - `test_index_view`

**Objectif**: Vérifier que la page d'accueil affiche correctement toutes les tâches.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskViewsTestCase.test_index_view
```

**Résultat attendu**:
- Code HTTP 200
- Toutes les tâches présentes dans le HTML
- Template `tasks/list.html` utilisé

---

## 2. [AUTO] Test de création d'une tâche
**Fichier**: `tasks/tests.py:23` - `test_index_view_post`

**Objectif**: Vérifier la création d'une nouvelle tâche via POST.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskViewsTestCase.test_index_view_post
```

**Résultat attendu**:
- Redirection (code 302)
- Tâche créée en base de données

---

## 3. [AUTO] Test d'affichage du formulaire de modification
**Fichier**: `tasks/tests.py:29` - `test_update_task_view_get`

**Objectif**: Vérifier l'affichage de la page de modification d'une tâche.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskViewsTestCase.test_update_task_view_get
```

**Résultat attendu**:
- Code HTTP 200
- Formulaire prérempli avec les données de la tâche
- Template `tasks/update_task.html` utilisé

---

## 4. [AUTO] Test de modification d'une tâche
**Fichier**: `tasks/tests.py:38` - `test_update_task_view_post`

**Objectif**: Vérifier la modification d'une tâche existante.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskViewsTestCase.test_update_task_view_post
```

**Résultat attendu**:
- Redirection (code 302)
- Tâche mise à jour en base de données

---

## 5. [AUTO] Test d'affichage de la confirmation de suppression
**Fichier**: `tasks/tests.py:49` - `test_delete_task_view_get`

**Objectif**: Vérifier l'affichage de la page de confirmation de suppression.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskViewsTestCase.test_delete_task_view_get
```

**Résultat attendu**:
- Code HTTP 200
- Template `tasks/delete.html` utilisé

---

## 6. [AUTO] Test de suppression d'une tâche
**Fichier**: `tasks/tests.py:57` - `test_delete_task_view_post`

**Objectif**: Vérifier la suppression effective d'une tâche.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskViewsTestCase.test_delete_task_view_post
```

**Résultat attendu**:
- Redirection (code 302)
- Tâche supprimée de la base de données

---

## 7. [AUTO] Test du modèle Task
**Fichier**: `tasks/tests.py:70` - `test_task_creation`

**Objectif**: Vérifier la création d'un objet Task et ses valeurs par défaut.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskModelTestCase.test_task_creation
```

**Résultat attendu**:
- Tâche créée avec titre correct
- `complete` à False par défaut
- `created` défini automatiquement

---

## 8. [AUTO] Test de la représentation string du modèle
**Fichier**: `tasks/tests.py:77` - `test_task_str`

**Objectif**: Vérifier que la méthode `__str__` retourne le titre.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.TaskModelTestCase.test_task_str
```

**Résultat attendu**:
- `str(task)` retourne le titre de la tâche

---

## 9. [AUTO] Test d'import du dataset
**Fichier**: `tasks/tests.py:88` - `test_dataset_import`

**Objectif**: Vérifier que le fixture dataset.json se charge correctement.

**Procédure**:
```bash
pipenv run python manage.py test tasks.tests.DatasetImportTestCase.test_dataset_import
```

**Résultat attendu**:
- 5 tâches importées
- Données correspondant au fixture

---

## 10. [ACCESSIBILITE] Test de conformité WCAG 2.1 niveau A
**Script**: `scripts/test_accessibility.sh`

**Objectif**: Vérifier la conformité d'accessibilité de toutes les pages.

**Procédure**:
```bash
# Lancer le serveur Django
pipenv run python manage.py runserver &

# Attendre que le serveur démarre
sleep 2

# Lancer les tests d'accessibilité
./scripts/test_accessibility.sh

# Arrêter le serveur
pkill -f "manage.py runserver"
```

**Résultat attendu**:
- 0 erreur d'accessibilité sur toutes les pages
- Conformité WCAG 2.1 niveau A

---

## 11. [MANUEL] Test de création d'une tâche vide
**Type**: Test fonctionnel négatif

**Objectif**: Vérifier le comportement lors d'une tentative de création d'une tâche sans titre.

**Procédure**:
1. Accéder à `http://localhost:8000/`
2. Cliquer sur "Créer une tâche" sans remplir le champ
3. Observer le comportement

**Résultat attendu**:
- Message d'erreur ou validation HTML5 empêchant la soumission
- Aucune tâche vide créée en base

---

## 12. [MANUEL] Test de modification d'une tâche inexistante
**Type**: Test d'erreur

**Objectif**: Vérifier le comportement lors de l'accès à une tâche inexistante.

**Procédure**:
1. Accéder à `http://localhost:8000/update_task/99999/`
2. Observer le comportement

**Résultat attendu**:
- Page d'erreur 404 ou message approprié
- Pas de crash de l'application

---

## 13. [VISUEL] Test d'affichage des tâches complétées
**Type**: Contrôle visuel

**Objectif**: Vérifier le style visuel des tâches marquées comme complétées.

**Procédure**:
1. Accéder à `http://localhost:8000/`
2. Créer une nouvelle tâche
3. La modifier pour la marquer comme complétée (cocher la case "complete")
4. Retourner à la liste

**Résultat attendu**:
- La tâche complétée doit avoir un style barré (text-decoration: line-through)
- L'opacité doit être réduite (opacity: 0.8)
- Les couleurs doivent respecter le contraste WCAG

---

## 14. [VISUEL] Test de responsive design
**Type**: Contrôle visuel multi-dispositifs

**Objectif**: Vérifier l'affichage sur différentes tailles d'écran.

**Procédure**:
1. Accéder à `http://localhost:8000/`
2. Tester sur les résolutions suivantes:
   - Mobile (375px)
   - Tablette (768px)
   - Desktop (1920px)
3. Utiliser les outils de développement du navigateur

**Résultat attendu**:
- Contenu lisible sur toutes les résolutions
- Pas de débordement horizontal
- Boutons cliquables facilement (zone de toucher suffisante sur mobile)

---

## 15. [MANUEL] Test de la persistance des données
**Type**: Test d'intégration

**Objectif**: Vérifier que les données persistent après redémarrage du serveur.

**Procédure**:
1. Créer 3 nouvelles tâches
2. Arrêter le serveur Django (`Ctrl+C`)
3. Redémarrer le serveur (`pipenv run python manage.py runserver`)
4. Accéder à `http://localhost:8000/`

**Résultat attendu**:
- Les 3 tâches créées sont toujours présentes
- Toutes les données sont intactes

---

## Exécution de tous les tests automatiques

Pour exécuter tous les tests automatiques en une seule commande:

```bash
# Tests unitaires et d'intégration
pipenv run python manage.py test tasks.tests

# Couverture de code
pipenv run coverage run --source='.' manage.py test tasks.tests
pipenv run coverage report
```

**Résultat attendu**:
- Tous les tests passent (9/9)
- Couverture de code à 100%

---

## Notes importantes

- Les tests automatiques doivent TOUS passer avant chaque commit
- Les tests d'accessibilité doivent être exécutés avant chaque release
- Les tests visuels doivent être vérifiés après toute modification CSS
- Les tests manuels doivent être documentés si un comportement change

## Fréquence recommandée

- **À chaque commit**: Tests automatiques (1-9)
- **À chaque PR**: Tests automatiques + accessibilité (1-10)
- **À chaque release**: Tous les tests (1-15)
- **Après modif CSS/UI**: Tests visuels (13-14)
- **Après modif backend**: Tests manuels fonctionnels (11-12, 15)

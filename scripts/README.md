# Scripts

Ce dossier contient tous les scripts shell utilisés pour le développement, les tests et le build du projet.

## Scripts disponibles

### `build.sh`

Script de build et de release pour créer une nouvelle version de l'application.

**Usage :**
```bash
./scripts/build.sh version=X.Y.Z
```

**Fonctionnalités :**
- Vérifie que le code passe le linter (Ruff)
- Vérifie la conformité WCAG 2.1 niveau A (accessibilité)
- Met à jour la version dans `todo/settings.py`
- Crée un commit et un tag Git
- Génère une archive ZIP dans `releases/`

**Exemple :**
```bash
./scripts/build.sh version=1.4.0
```

### `test_accessibility.sh`

Script de test d'accessibilité utilisant pa11y-ci pour vérifier la conformité WCAG 2.1 niveau A.

**Usage :**
```bash
./scripts/test_accessibility.sh
```

**Prérequis :**
- Le serveur Django doit être en cours d'exécution sur `http://localhost:8000/`
- Les dépendances Node.js doivent être installées (`npm install`)

**Exemple :**
```bash
# Dans un terminal, démarrer le serveur
pipenv run python manage.py runserver

# Dans un autre terminal, lancer les tests
./scripts/test_accessibility.sh
```

### `test_multi_versions.sh`

Script pour tester l'application avec plusieurs versions de Python et Django.

**Usage :**
```bash
./scripts/test_multi_versions.sh
```

**Fonctionnalités :**
- Teste avec Python 3.9 et Django 3.2, 4.2
- Teste avec Python 3.13 et Django 4.2, 5.0
- Crée des environnements virtuels temporaires pour chaque combinaison
- Affiche les résultats avec des codes couleur

**Note :** Les versions de Python doivent être installées sur le système pour être testées.

### `send_notification.py`

Script pour envoyer des notifications à Discord, Slack ou autres services via webhook.

**Usage :**
```bash
python scripts/send_notification.py <status> <message> [webhook_url]
```

**Paramètres :**
- `status` : `start`, `success`, ou `failure`
- `message` : Message de notification
- `webhook_url` : URL du webhook (optionnel, peut être fournie via variable d'environnement)

**Variables d'environnement :**
- `WEBHOOK_URL` : URL du webhook (prioritaire)
- `DISCORD_WEBHOOK` : URL du webhook Discord
- `SLACK_WEBHOOK` : URL du webhook Slack

**Exemple :**
```bash
# Avec URL en paramètre
python scripts/send_notification.py success "Tests réussis" https://discord.com/api/webhooks/...

# Avec variable d'environnement
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."
python scripts/send_notification.py start "CI démarrée"
```

**Note :** Ce script est utilisé automatiquement par GitHub Actions pour envoyer des notifications lors de l'exécution de la CI.



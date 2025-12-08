# Configuration des Notifications CI

Ce document explique comment configurer les notifications Discord (ou autres services) pour recevoir des alertes lors de l'exécution de la CI.

## 📋 Prérequis

- Un compte Discord (ou Slack/Teams)
- Accès administrateur au dépôt GitHub

## 🔧 Configuration Discord

### Étape 1 : Créer un Webhook Discord

1. Ouvrez Discord et allez dans votre serveur
2. Allez dans **Paramètres du serveur** → **Intégrations** → **Webhooks**
3. Cliquez sur **Nouveau webhook**
4. Configurez le webhook :
   - **Nom** : `CI Notifications` (ou autre nom)
   - **Canal** : Sélectionnez le canal où recevoir les notifications
5. Cliquez sur **Copier l'URL du webhook**
   - L'URL ressemble à : `https://discord.com/api/webhooks/123456789/abcdefghijklmnopqrstuvwxyz`

### Étape 2 : Ajouter le Webhook comme Secret GitHub

1. Allez sur votre dépôt GitHub
2. Cliquez sur **Settings** → **Secrets and variables** → **Actions**
3. Cliquez sur **New repository secret**
4. Configurez le secret :
   - **Name** : `DISCORD_WEBHOOK`
   - **Secret** : Collez l'URL du webhook copiée à l'étape 1
5. Cliquez sur **Add secret**

## 🔔 Types de Notifications

Le système envoie automatiquement 3 types de notifications :

### 🚀 Notification de Démarrage
- **Quand** : Au début de chaque exécution de la CI
- **Couleur** : Bleu
- **Contenu** : Informations sur le dépôt, la branche et le commit

### ✅ Notification de Succès
- **Quand** : Si tous les tests passent avec succès
- **Couleur** : Vert
- **Contenu** : Confirmation que la CI est réussie

### ❌ Notification d'Échec
- **Quand** : Si un test échoue ou si la CI rencontre une erreur
- **Couleur** : Rouge
- **Contenu** : Lien vers les logs de la CI pour déboguer

## 🔄 Configuration pour Slack

Si vous préférez utiliser Slack au lieu de Discord :

1. Créez un webhook Slack :
   - Allez sur https://api.slack.com/apps
   - Créez une nouvelle app ou utilisez une existante
   - Activez les **Incoming Webhooks**
   - Créez un webhook pour votre canal

2. Ajoutez le secret GitHub :
   - **Name** : `SLACK_WEBHOOK`
   - **Secret** : URL du webhook Slack

Le script détecte automatiquement le type de webhook et utilise le format approprié.

## 🧪 Test des Notifications

Pour tester les notifications localement :

```bash
# Installer les dépendances
pipenv install --dev

# Tester une notification de démarrage
export DISCORD_WEBHOOK="votre_url_webhook"
pipenv run python scripts/send_notification.py start "Test de notification"

# Tester une notification de succès
pipenv run python scripts/send_notification.py success "Tests réussis !"

# Tester une notification d'échec
pipenv run python scripts/send_notification.py failure "Tests échoués"
```

## 📝 Format des Messages

Les notifications incluent automatiquement :
- **Repository** : Nom du dépôt GitHub
- **Branch** : Branche sur laquelle la CI s'exécute
- **Commit** : Hash du commit (avec lien)
- **Workflow** : Lien direct vers l'exécution de la CI

## 🔒 Sécurité

⚠️ **Important** : Ne partagez jamais l'URL de votre webhook publiquement. Elle permet à n'importe qui d'envoyer des messages dans votre canal Discord/Slack.

- ✅ Utilisez toujours les **Secrets GitHub** pour stocker les URLs de webhook
- ✅ Ne commitez jamais les URLs de webhook dans le code
- ✅ Régénérez le webhook si vous pensez qu'il a été compromis

## 🛠️ Dépannage

### Les notifications ne sont pas envoyées

1. Vérifiez que le secret `DISCORD_WEBHOOK` est bien configuré dans GitHub
2. Vérifiez que l'URL du webhook est correcte
3. Vérifiez les logs de la CI dans l'onglet "Actions" de GitHub
4. Testez le webhook manuellement avec curl :
   ```bash
   curl -X POST "VOTRE_URL_WEBHOOK" \
     -H "Content-Type: application/json" \
     -d '{"content": "Test"}'
   ```

### Le webhook ne fonctionne plus

- Vérifiez que le webhook n'a pas été supprimé dans Discord/Slack
- Régénérez le webhook et mettez à jour le secret GitHub


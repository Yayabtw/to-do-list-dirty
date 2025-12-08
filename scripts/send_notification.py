#!/usr/bin/env python3
"""
Script pour envoyer des notifications à Discord (ou autres services via webhook).

Usage:
    python scripts/send_notification.py <status> <message> [webhook_url]

Status: start, success, failure
"""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def send_discord_notification(webhook_url, status, message, details=None):
    """
    Envoie une notification à Discord via webhook.

    Args:
        webhook_url: URL du webhook Discord
        status: 'start', 'success', ou 'failure'
        message: Message principal
        details: Détails supplémentaires (optionnel)
    """
    # Couleurs et emojis selon le statut
    colors = {
        'start': 0x3498db,    # Bleu
        'success': 0x2ecc71,  # Vert
        'failure': 0xe74c3c   # Rouge
    }

    emojis = {
        'start': '🚀',
        'success': '✅',
        'failure': '❌'
    }

    titles = {
        'start': 'CI démarrée',
        'success': 'CI réussie',
        'failure': 'CI échouée'
    }

    # Construire l'embed Discord
    embed = {
        'title': f"{emojis.get(status, '📢')} {titles.get(status, 'Notification CI')}",
        'description': message,
        'color': colors.get(status, 0x95a5a6),
        'fields': []
    }

    # Ajouter des détails si fournis
    if details:
        if isinstance(details, dict):
            for key, value in details.items():
                embed['fields'].append({
                    'name': key,
                    'value': str(value),
                    'inline': True
                })
        else:
            embed['fields'].append({
                'name': 'Détails',
                'value': str(details),
                'inline': False
            })

    payload = {
        'embeds': [embed]
    }

    # Envoyer la requête
    try:
        payload_json = json.dumps(payload, ensure_ascii=False)
        req = Request(
            webhook_url,
            data=payload_json.encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'CI-Notifier/1.0 (+github-actions)'
            }
        )

        with urlopen(req, timeout=10) as response:
            response_body = response.read().decode('utf-8')
            if response.status == 204:
                print(f"✅ Notification envoyée avec succès ({status})")
                return True
            else:
                print(f"⚠️ Réponse inattendue: {response.status}")
                if response_body:
                    print(f"   Réponse: {response_body}")
                return False

    except HTTPError as e:
        error_body = e.read().decode('utf-8') if hasattr(e, 'read') else ''
        print(f"❌ Erreur HTTP: {e.code} - {e.reason}")
        if error_body:
            print(f"   Détails: {error_body}")
        return False
    except URLError as e:
        print(f"❌ Erreur URL: {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False


def send_slack_notification(webhook_url, status, message, details=None):
    """
    Envoie une notification à Slack via webhook.

    Args:
        webhook_url: URL du webhook Slack
        status: 'start', 'success', ou 'failure'
        message: Message principal
        details: Détails supplémentaires (optionnel)
    """
    colors = {
        'start': '#3498db',
        'success': '#2ecc71',
        'failure': '#e74c3c'
    }

    emojis = {
        'start': '🚀',
        'success': '✅',
        'failure': '❌'
    }

    payload = {
        'attachments': [{
            'color': colors.get(status, '#95a5a6'),
            'title': f"{emojis.get(status, '📢')} CI {status.upper()}",
            'text': message,
            'fields': []
        }]
    }

    if details and isinstance(details, dict):
        for key, value in details.items():
            payload['attachments'][0]['fields'].append({
                'title': key,
                'value': str(value),
                'short': True
            })

    try:
        req = Request(
            webhook_url,
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'CI-Notifier/1.0 (+github-actions)'
            }
        )

        with urlopen(req, timeout=10) as response:
            if response.status == 200:
                print(f"✅ Notification Slack envoyée avec succès ({status})")
                return True
            else:
                print(f"⚠️ Réponse inattendue: {response.status}")
                return False

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Point d'entrée principal."""
    if len(sys.argv) < 3:
        print("Usage: python scripts/send_notification.py <status> <message> [webhook_url]")
        print("Status: start, success, failure")
        print("Webhook URL peut être fournie via WEBHOOK_URL ou DISCORD_WEBHOOK")
        sys.exit(1)

    status = sys.argv[1].lower()
    message = sys.argv[2]

    if status not in ['start', 'success', 'failure']:
        print(f"❌ Statut invalide: {status}. Utilisez 'start', 'success', ou 'failure'")
        sys.exit(1)

    # Récupérer l'URL du webhook
    webhook_url = None
    if len(sys.argv) >= 4:
        webhook_url = sys.argv[3]
    else:
        # Essayer les variables d'environnement
        webhook_url = os.getenv('WEBHOOK_URL') or os.getenv('DISCORD_WEBHOOK') or os.getenv('SLACK_WEBHOOK')

    if not webhook_url:
        print("⚠️ Aucune URL de webhook fournie. Notification ignorée.")
        print("💡 Configurez WEBHOOK_URL, DISCORD_WEBHOOK ou SLACK_WEBHOOK")
        sys.exit(0)

    # Détecter le type de webhook
    webhook_type = 'discord'
    if 'slack.com' in webhook_url or 'hooks.slack.com' in webhook_url:
        webhook_type = 'slack'
    elif 'discord.com' in webhook_url or 'discordapp.com' in webhook_url:
        webhook_type = 'discord'

    # Récupérer des détails depuis les variables d'environnement GitHub Actions
    details = {}
    if os.getenv('GITHUB_REPOSITORY'):
        details['Repository'] = os.getenv('GITHUB_REPOSITORY')
    if os.getenv('GITHUB_REF'):
        branch = os.getenv('GITHUB_REF', '').replace('refs/heads/', '')
        details['Branch'] = branch
    if os.getenv('GITHUB_SHA'):
        commit_sha = os.getenv('GITHUB_SHA', '')[:7]
        details['Commit'] = f"[{commit_sha}](https://github.com/{os.getenv('GITHUB_REPOSITORY', '')}/commit/{os.getenv('GITHUB_SHA', '')})"
    if os.getenv('GITHUB_RUN_ID'):
        run_id = os.getenv('GITHUB_RUN_ID')
        repo = os.getenv('GITHUB_REPOSITORY', '')
        details['Workflow'] = f"[View Run](https://github.com/{repo}/actions/runs/{run_id})"

    # Envoyer la notification
    if webhook_type == 'discord':
        success = send_discord_notification(webhook_url, status, message, details)
    elif webhook_type == 'slack':
        success = send_slack_notification(webhook_url, status, message, details)
    else:
        print(f"⚠️ Type de webhook non reconnu: {webhook_type}. Tentative avec Discord...")
        success = send_discord_notification(webhook_url, status, message, details)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()


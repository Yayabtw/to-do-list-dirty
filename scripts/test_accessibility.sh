#!/bin/bash

# Script de test d'accessibilité WCAG 2.1 niveau A
# Utilise pa11y-ci pour tester l'accessibilité de l'application

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

echo "=========================================="
echo "Test d'accessibilité WCAG 2.1 niveau A"
echo "=========================================="

# Vérifier si le serveur Django est en cours d'exécution
if ! curl -s http://localhost:8000/ > /dev/null; then
    echo "❌ Erreur: Le serveur Django n'est pas en cours d'exécution sur http://localhost:8000/"
    echo "Veuillez démarrer le serveur avec: pipenv run python manage.py runserver"
    exit 1
fi

echo "✓ Serveur Django détecté sur http://localhost:8000/"
echo ""

# Lancer les tests pa11y
echo "Lancement des tests d'accessibilité..."
npx pa11y-ci --config .pa11yci.json

# Capturer le code de sortie
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Tests d'accessibilité réussis (100%)"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "❌ Tests d'accessibilité échoués"
    echo "Des problèmes d'accessibilité ont été détectés"
    echo "=========================================="
fi

exit $EXIT_CODE

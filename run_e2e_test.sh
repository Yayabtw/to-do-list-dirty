#!/bin/bash
# Script pour exécuter le test E2E TC016

echo "=================================="
echo "TC016 - Test End-to-End"
echo "=================================="
echo ""

# Vérifier que le serveur Django tourne
echo "🔍 Vérification que le serveur Django est accessible..."
if curl -s http://127.0.0.1:8000 > /dev/null; then
    echo "✅ Serveur Django accessible"
    echo ""
else
    echo "❌ Serveur Django non accessible sur http://127.0.0.1:8000"
    echo ""
    echo "💡 Lancez le serveur dans un autre terminal:"
    echo "   pipenv run python manage.py runserver 127.0.0.1:8000"
    echo ""
    exit 1
fi

# Vérifier que ChromeDriver est installé
if command -v chromedriver &> /dev/null; then
    echo "✅ ChromeDriver trouvé: $(chromedriver --version | head -1)"
else
    echo "⚠️  ChromeDriver non trouvé dans PATH"
    echo "💡 Installation recommandée:"
    echo "   macOS: brew install chromedriver"
    echo "   Linux: apt install chromium-chromedriver"
    echo ""
    echo "Tentative d'exécution quand même..."
fi

echo ""
echo "=================================="
echo "Lancement du test E2E..."
echo "=================================="
echo ""

# Exécuter le test
pipenv run python tests/e2e/tc016_crud_10_tasks.py "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ Test réussi!"
else
    echo ""
    echo "❌ Test échoué (code: $exit_code)"
fi

exit $exit_code

#!/bin/bash
# Script pour exécuter les tests et générer un rapport

echo "=================================="
echo "Running Django tests..."
echo "=================================="

# Exécuter les tests avec le runner JSON
pipenv run python manage.py test tasks.tests --testrunner=tests.json_test_runner.JSONTestRunner

# Vérifier si les tests ont réussi
if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "Generating test report..."
    echo "=================================="

    # Générer le rapport
    pipenv run python test_report.py
else
    echo ""
    echo "❌ Tests failed. Generating report anyway..."
    echo ""
    pipenv run python test_report.py
    exit 1
fi

#!/usr/bin/env python3
"""
Génère un rapport Markdown pour les Pull Requests à partir des résultats JSON
des tests unitaires, E2E (Selenium) et accessibilité (pa11y-ci), ainsi que
la liste des tests (test_list.yaml).
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ Erreur: Le module PyYAML n'est pas installé.")
    sys.exit(1)


def load_test_list(yaml_path='test_list.yaml'):
    """Charge la liste des tests depuis le fichier YAML."""
    try:
        with open(yaml_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('tests', [])
    except FileNotFoundError:
        return []


def load_json_if_exists(path):
    """Charge un fichier JSON s'il existe, sinon None."""
    path_obj = Path(path)
    if not path_obj.exists():
        return None
    try:
        with open(path_obj, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def load_accessibility_results(path='result_test_accessibility.json'):
    """
    Charge les résultats pa11y-ci.
    pa11y-ci --json produit du JSON, mais en cas d'échec on stocke un placeholder.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        return None

    content = path_obj.read_text(encoding='utf-8', errors='ignore')
    if content.strip().startswith('{'):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {'raw_output': content}
    return {'raw_output': content}


def get_test_status(test, results_data, selenium_data=None):
    """
    Détermine le statut d'un test en fonction des JSON.
    """
    test_number = str(test['numero'])
    test_type = test['type']

    if test_type == 'manuel':
        return '🫱', 'Manual test needed', 'manual'

    if test_type == 'auto-selenium':
        if not selenium_data:
            return '🕳', 'Not found', 'not_found'
        for result_test in selenium_data.get('tests', []):
            if result_test.get('test_number') == test_number:
                status = result_test.get('status')
                if status == 'passed':
                    return '✅', 'Passed', 'passed'
                if status in ('failed', 'error'):
                    return '❌', status.title(), 'failed'
        return '🕳', 'Not found', 'not_found'

    if test_type == 'auto-unittest':
        if not results_data:
            return '🕳', 'Not found', 'not_found'
        for result_test in results_data.get('tests', []):
            if result_test.get('test_number') == test_number:
                status = result_test.get('status')
                if status == 'passed':
                    return '✅', 'Passed', 'passed'
                if status == 'failed':
                    return '❌', 'Failed', 'failed'
                if status == 'error':
                    return '❌', 'Error', 'failed'
                if status == 'skipped':
                    return '⏭️', 'Skipped', 'skipped'
        return '🕳', 'Not found', 'not_found'

    return '❓', 'Unknown', 'unknown'


def format_test_number(numero):
    """Formate le numéro de test (ex: 3 -> TC003)."""
    return f"TC{str(numero).zfill(3)}"


def generate_markdown_report(tests, results_data, selenium_data, accessibility_data):
    """Génère un rapport Markdown (string)."""
    output = []
    output.append("# 📊 Rapport des Tests CI\n")

    stats = {
        'passed': 0,
        'failed': 0,
        'not_found': 0,
        'manual': 0,
        'skipped': 0,
        'unknown': 0,
    }

    for test in tests:
        _, _, status_key = get_test_status(test, results_data, selenium_data)
        if status_key in stats:
            stats[status_key] += 1

    total_tests = len(tests)
    output.append("## 📈 Résumé\n")
    def pct(value):  # éviter division par zéro
        return (value / total_tests * 100) if total_tests else 0
    output.append(f"- **Total**: {total_tests}")
    output.append(f"- ✅ **Réussis**: {stats['passed']} ({pct(stats['passed']):.1f}%)")
    output.append(f"- ❌ **Échoués**: {stats['failed']} ({pct(stats['failed']):.1f}%)")
    output.append(f"- 🫱 **Manuels**: {stats['manual']} ({pct(stats['manual']):.1f}%)")
    output.append(f"- 🕳 **Non trouvés**: {stats['not_found']} ({pct(stats['not_found']):.1f}%)")
    if stats['skipped'] > 0:
        output.append(f"- ⏭️ **Sautés**: {stats['skipped']} ({pct(stats['skipped']):.1f}%)")
    output.append("")

    if accessibility_data:
        output.append("## ♿ Tests d'accessibilité (pa11y-ci)\n")
        if accessibility_data.get('errors') or accessibility_data.get('raw_output'):
            output.append("❌ Des erreurs d'accessibilité ont été détectées.\n")
            raw = accessibility_data.get('raw_output')
            if raw:
                output.append("```\n" + raw[:800] + ("\n... (troncqué)" if len(raw) > 800 else "") + "\n```\n")
        else:
            output.append("✅ Aucune erreur d'accessibilité détectée.\n")

    output.append("## 📋 Détails des tests\n")
    output.append("| Test | Type | Statut |")
    output.append("|------|------|--------|")
    for test in tests:
        emoji, status_text, _ = get_test_status(test, results_data, selenium_data)
        output.append(f"| {format_test_number(test['numero'])} | {test['type']} | {emoji} {status_text} |")
    output.append("")

    manual_tests = [t for t in tests if t['type'] == 'manuel']
    if manual_tests:
        output.append("## 🫱 Tests manuels à réaliser\n")
        output.append("Les tests suivants nécessitent une validation manuelle :\n")
        for test in manual_tests:
            output.append(f"### {format_test_number(test['numero'])}: {test['nom']}")
            output.append(f"- **Description**: {test['description']}")
            if 'procedure' in test:
                output.append("- **Procédure**:")
                for step in test['procedure']:
                    output.append(f"  - {step}")
            if 'resultat_attendu' in test:
                output.append(f"- **Résultat attendu**: {test['resultat_attendu']}")
            output.append("")

    return "\n".join(output)


def main():
    tests = load_test_list()
    if not tests:
        print("❌ Aucun test trouvé dans test_list.yaml.")
        sys.exit(1)

    results_data = load_json_if_exists('result_test_auto.json')
    selenium_data = load_json_if_exists('result_test_selenium.json')
    accessibility_data = load_accessibility_results()

    report = generate_markdown_report(tests, results_data, selenium_data, accessibility_data)

    Path('pr_report.md').write_text(report, encoding='utf-8')
    print(report)


if __name__ == '__main__':
    main()


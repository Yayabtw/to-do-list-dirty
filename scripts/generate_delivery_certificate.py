#!/usr/bin/env python3
"""
Script pour générer un bon de livraison PDF certifiant que les tests sont passés.

Usage:
    python scripts/generate_delivery_certificate.py [output_file]
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ Erreur: Le module PyYAML n'est pas installé.")
    print("   Installez-le avec: pip install pyyaml")
    sys.exit(1)

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:
    print("❌ Erreur: Le module reportlab n'est pas installé.")
    print("   Installez-le avec: pip install reportlab")
    sys.exit(1)


def load_test_list(yaml_path='test_list.yaml'):
    """Charge la liste des tests depuis le fichier YAML."""
    try:
        with open(yaml_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('tests', [])
    except FileNotFoundError:
        print(f"⚠️  Fichier {yaml_path} non trouvé.")
        return []
    except yaml.YAMLError as e:
        print(f"❌ Erreur lors de la lecture du YAML: {e}")
        return []


def load_test_results(json_path='result_test_auto.json'):
    """Charge les résultats des tests automatisés."""
    if not Path(json_path).exists():
        return None
    try:
        with open(json_path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def load_selenium_results(json_path='result_test_selenium.json'):
    """Charge les résultats des tests Selenium."""
    if not Path(json_path).exists():
        return None
    try:
        with open(json_path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def load_accessibility_results(json_path='result_test_accessibility.json'):
    """Charge les résultats des tests d'accessibilité."""
    if not Path(json_path).exists():
        return None
    try:
        with open(json_path, encoding='utf-8') as f:
            content = f.read()
            if content.strip().startswith('{'):
                return json.loads(content)
            return {'raw_output': content}
    except (json.JSONDecodeError, Exception):
        return None


def get_test_status(test, results_data, selenium_data=None):
    """Détermine le statut d'un test."""
    test_number = str(test['numero'])
    test_type = test['type']

    if test_type == 'manuel':
        return '🫱', 'Test manuel', 'manual'

    if test_type == 'auto-selenium':
        if not selenium_data:
            return '🕳', 'Non exécuté', 'not_found'
        for result_test in selenium_data.get('tests', []):
            if result_test.get('test_number') == test_number:
                status = result_test.get('status')
                if status == 'passed':
                    return '✅', 'Réussi', 'passed'
                elif status == 'failed':
                    return '❌', 'Échoué', 'failed'
                elif status == 'error':
                    return '❌', 'Erreur', 'failed'
        return '🕳', 'Non exécuté', 'not_found'

    if test_type == 'auto-unittest':
        if not results_data:
            return '🕳', 'Non exécuté', 'not_found'
        for result_test in results_data.get('tests', []):
            if result_test.get('test_number') == test_number:
                status = result_test.get('status')
                if status == 'passed':
                    return '✅', 'Réussi', 'passed'
                elif status == 'failed':
                    return '❌', 'Échoué', 'failed'
                elif status == 'error':
                    return '❌', 'Erreur', 'failed'
                elif status == 'skipped':
                    return '⏭️', 'Sauté', 'skipped'
        return '🕳', 'Non exécuté', 'not_found'

    return '❓', 'Inconnu', 'unknown'


def format_test_number(numero):
    """Formate le numéro de test."""
    return f"TC{str(numero).zfill(3)}"


def generate_pdf(output_file='bon_livraison_tests.pdf', repository=None, branch=None, commit=None):
    """Génère le PDF du bon de livraison."""
    # Charger les données
    tests = load_test_list()
    results_data = load_test_results()
    selenium_data = load_selenium_results()
    load_accessibility_results()  # Chargé mais non utilisé pour l'instant

    # Créer le document PDF
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1,  # Centré
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
    )
    normal_style = styles['Normal']

    # En-tête
    story.append(Paragraph("BON DE LIVRAISON - CERTIFICAT DE TESTS", title_style))
    story.append(Spacer(1, 0.5*cm))

    # Informations générales
    story.append(Paragraph("<b>Informations du dépôt</b>", heading_style))
    info_data = []
    if repository:
        info_data.append(['Dépôt:', repository])
    if branch:
        info_data.append(['Branche:', branch])
    if commit:
        info_data.append(['Commit:', commit[:7] if len(commit) > 7 else commit])

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    info_data.append(['Date et heure:', timestamp])

    if results_data and results_data.get('timestamp'):
        try:
            test_time = datetime.fromisoformat(results_data['timestamp'].replace('Z', '+00:00'))
            info_data.append(['Date des tests:', test_time.strftime("%d/%m/%Y %H:%M:%S")])
        except Exception:
            pass

    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5*cm))

    # Statistiques
    stats = {
        'passed': 0,
        'failed': 0,
        'not_found': 0,
        'manual': 0,
        'skipped': 0,
        'total': len(tests)
    }

    for test in tests:
        emoji, status_text, status_key = get_test_status(test, results_data, selenium_data)
        if status_key == 'passed':
            stats['passed'] += 1
        elif status_key == 'failed':
            stats['failed'] += 1
        elif status_key == 'manual':
            stats['manual'] += 1
        elif status_key == 'skipped':
            stats['skipped'] += 1
        else:
            stats['not_found'] += 1

    story.append(Paragraph("<b>Résumé des tests</b>", heading_style))
    summary_data = [
        ['Total des tests:', str(stats['total'])],
        ['✅ Tests réussis:', str(stats['passed'])],
        ['❌ Tests échoués:', str(stats['failed'])],
        ['🫱 Tests manuels:', str(stats['manual'])],
        ['⏭️ Tests sautés:', str(stats['skipped'])],
        ['🕳 Tests non exécutés:', str(stats['not_found'])],
    ]

    summary_table = Table(summary_data, colWidths=[6*cm, 10*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5*cm))

    # Liste détaillée des tests
    story.append(Paragraph("<b>Détail des tests</b>", heading_style))

    # En-tête du tableau
    table_data = [['Test', 'Nom', 'Type', 'Statut']]

    for test in tests:
        emoji, status_text, status_key = get_test_status(test, results_data, selenium_data)
        test_number = format_test_number(test['numero'])
        test_name = test.get('nom', 'N/A')
        test_type = test.get('type', 'N/A')

        table_data.append([
            test_number,
            test_name[:40] + '...' if len(test_name) > 40 else test_name,
            test_type,
            f"{emoji} {status_text}"
        ])

    test_table = Table(table_data, colWidths=[2.5*cm, 7*cm, 3.5*cm, 3*cm])
    test_table.setStyle(TableStyle([
        # En-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        # Lignes de données
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        # Grille
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(test_table)
    story.append(Spacer(1, 0.5*cm))

    # Tests manuels à réaliser
    manual_tests = [t for t in tests if t['type'] == 'manuel']
    if manual_tests:
        story.append(Paragraph("<b>Tests manuels à réaliser</b>", heading_style))
        for test in manual_tests:
            test_number = format_test_number(test['numero'])
            story.append(Paragraph(
                f"<b>{test_number}:</b> {test.get('nom', 'N/A')}",
                normal_style
            ))
            story.append(Paragraph(
                f"   {test.get('description', '')}",
                normal_style
            ))
            story.append(Spacer(1, 0.2*cm))

    # Pied de page avec certificat
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "<b>CERTIFICAT</b><br/>"
        "Je certifie que les tests automatisés listés ci-dessus ont été exécutés "
        "et que leurs résultats sont conformes aux attentes.",
        ParagraphStyle(
            'Certificate',
            parent=normal_style,
            fontSize=11,
            alignment=1,  # Centré
            spaceBefore=20,
            spaceAfter=20,
        )
    ))

    # Générer le PDF
    doc.build(story)
    print(f"✅ Bon de livraison généré: {output_file}")
    return output_file


def main():
    """Point d'entrée principal."""
    output_file = sys.argv[1] if len(sys.argv) > 1 else 'bon_livraison_tests.pdf'

    # Récupérer les informations depuis les variables d'environnement GitHub Actions
    repository = os.getenv('GITHUB_REPOSITORY')
    branch = os.getenv('GITHUB_REF', '').replace('refs/heads/', '').replace('refs/pull/', 'PR-')
    commit = os.getenv('GITHUB_SHA')

    generate_pdf(output_file, repository, branch, commit)


if __name__ == '__main__':
    main()


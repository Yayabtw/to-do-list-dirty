#!/usr/bin/env python
"""
Alternative Python pour les tests d'accessibilité WCAG 2.1 niveau A
Utilise axe-selenium-python au lieu de pa11y

Installation:
    pipenv install --dev axe-selenium-python selenium

Usage:
    pipenv run python test_accessibility_python.py
"""

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe


def test_accessibility(url="http://localhost:8000/"):
    """Test l'accessibilité d'une URL avec axe-core."""
    
    print("=" * 50)
    print("Test d'accessibilité WCAG 2.1 niveau A (Python)")
    print("=" * 50)
    print()
    
    # Configuration Chrome headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        # Initialiser le driver Chrome
        print(f"Test de l'URL: {url}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Initialiser axe
        axe = Axe(driver)
        
        # Injecter axe-core dans la page
        axe.inject()
        
        # Lancer l'analyse (WCAG 2.1 niveau A)
        results = axe.run(options={
            "runOnly": {
                "type": "tag",
                "values": ["wcag2a", "wcag21a"]
            }
        })
        
        # Analyser les résultats
        violations = results.get("violations", [])
        
        if not violations:
            print()
            print("=" * 50)
            print("✓ Tests d'accessibilité réussis (100%)")
            print("=" * 50)
            return 0
        else:
            print()
            print(f"❌ {len(violations)} violation(s) détectée(s):")
            print()
            
            for i, violation in enumerate(violations, 1):
                print(f"{i}. {violation['help']}")
                print(f"   Impact: {violation['impact']}")
                print(f"   Description: {violation['description']}")
                print(f"   Éléments affectés: {len(violation['nodes'])}")
                
                # Afficher le premier élément affecté
                if violation['nodes']:
                    node = violation['nodes'][0]
                    print(f"   Sélecteur: {node['target']}")
                    if 'html' in node:
                        html = node['html']
                        if len(html) > 100:
                            html = html[:100] + "..."
                        print(f"   HTML: {html}")
                print()
            
            print("=" * 50)
            print("❌ Tests d'accessibilité échoués")
            print("=" * 50)
            
            # Générer un rapport détaillé
            axe.write_results(results, "accessibility_report.json")
            print()
            print("Rapport détaillé sauvegardé dans: accessibility_report.json")
            
            return 1
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        print()
        print("Assurez-vous que:")
        print("1. Le serveur Django est en cours d'exécution")
        print("2. Chrome/Chromium est installé")
        print("3. Les dépendances sont installées: pipenv install --dev axe-selenium-python selenium")
        return 1
        
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    exit_code = test_accessibility()
    sys.exit(exit_code)

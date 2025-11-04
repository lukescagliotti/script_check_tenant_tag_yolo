#!/usr/bin/env python3
"""
Tenant Microservices Tags Checker
Script per confrontare i tag dei microservizi di un tenant tra UAT e PROD

Uso: python3 tenant_checker.py <tenant_name>
"""

import os
import sys
import yaml
import re
from tabulate import tabulate
from pathlib import Path

# ========================================
# CONFIGURAZIONE - MODIFICA QUESTO PATH!
# ========================================
REPO_BASE_PATH = os.environ.get('REPO_PATH', '/Users/luca/Desktop/Lavoro/reusable-pipelines')

def extract_tag_from_image(image_url):
    """Estrae il tag dalla URL dell'immagine Docker"""
    if not image_url:
        return "N/A"
    
    # Cerca il pattern :vX.X.X o :latest o altri tag
    tag_match = re.search(r':([^:]+)$', image_url)
    if tag_match:
        return tag_match.group(1)
    return "N/A"

def read_config_file(file_path):
    """Legge un file YAML di configurazione e restituisce l'immagine"""
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config.get('global', {}).get('image', '')
    except Exception as e:
        print(f"⚠️  Errore nella lettura di {file_path}: {e}")
        return ''

def get_microservices_tags(tenant_name):
    """Ottiene i tag UAT e PROD per tutti i microservizi di un tenant"""
    tenant_path = Path(REPO_BASE_PATH) / "deploy" / "tenants" / tenant_name
    
    if not tenant_path.exists():
        print(f"❌ Tenant '{tenant_name}' non trovato nel path: {tenant_path}")
        return []
    
    microservices = []
    
    # Trova tutte le cartelle dei microservizi
    for service_dir in tenant_path.iterdir():
        if service_dir.is_dir() and service_dir.name not in ['api-gateway']:
            service_name = service_dir.name
            
            # Path ai file di configurazione
            uat_config = service_dir / "branches" / "uat-config.yaml"
            prod_config = service_dir / "branches" / "prod-config.yaml"
            
            # Leggi i tag
            uat_image = read_config_file(uat_config) if uat_config.exists() else ''
            prod_image = read_config_file(prod_config) if prod_config.exists() else ''
            
            uat_tag = extract_tag_from_image(uat_image)
            prod_tag = extract_tag_from_image(prod_image)
            
            # Determina lo stato (UAT vs PROD)
            if uat_tag == prod_tag:
                status = "✅ Allineato"
            elif uat_tag == "N/A" or prod_tag == "N/A":
                status = "⚠️  Config mancante"
            else:
                # Confronta le versioni numeriche se possibile
                try:
                    # Pulisci i tag per il confronto
                    uat_clean = re.sub(r'[^\d\.]', '', uat_tag.replace('v', ''))
                    prod_clean = re.sub(r'[^\d\.]', '', prod_tag.replace('v', ''))
                    
                    if uat_clean and prod_clean:
                        uat_version = [int(x) for x in uat_clean.split('.') if x.isdigit()]
                        prod_version = [int(x) for x in prod_clean.split('.') if x.isdigit()]
                        
                        if len(uat_version) >= 3 and len(prod_version) >= 3:
                            if uat_version > prod_version:
                                status = "🔼 UAT più recente"
                            elif uat_version < prod_version:
                                status = "🔽 PROD più recente"
                            else:
                                status = "✅ Allineato"
                        else:
                            status = "❓ Da verificare"
                    else:
                        status = "❓ Da verificare"
                except:
                    status = "❓ Da verificare"
            
            microservices.append({
                'service': service_name,
                'uat_tag': uat_tag,
                'prod_tag': prod_tag,
                'status': status
            })
    
    return microservices

def list_available_tenants():
    """Lista tutti i tenant disponibili"""
    tenant_base = Path(REPO_BASE_PATH) / "deploy" / "tenants"
    
    if not tenant_base.exists():
        print(f"❌ Path tenant non trovato: {tenant_base}")
        print(f"📁 Verifica che REPO_BASE_PATH sia corretto: {REPO_BASE_PATH}")
        return []
    
    tenants = []
    for tenant in sorted(tenant_base.iterdir()):
        if tenant.is_dir() and not tenant.name.startswith('.'):
            tenants.append(tenant.name)
    
    return tenants

def main():
    print(f"📁 Repository path: {REPO_BASE_PATH}")
    print()
    
    if len(sys.argv) != 2:
        print("💡 Uso: python3 tenant_checker.py <tenant_name>")
        print()
        print("🏢 Tenant disponibili:")
        
        tenants = list_available_tenants()
        if tenants:
            for tenant in tenants:
                print(f"  - {tenant}")
        else:
            print("   Nessun tenant trovato!")
            print("   Verifica il path della repository nella configurazione.")
        
        print()
        print("📝 Esempio: python3 tenant_checker.py artbkr")
        print()
        print("🔧 Per cambiare il path della repository:")
        print("   export REPO_PATH='/path/to/your/reusable-pipelines'")
        print("   oppure modifica REPO_BASE_PATH nel codice")
        sys.exit(1)
    
    tenant_name = sys.argv[1]
    
    print(f"🔍 Analizzando microservizi del tenant: {tenant_name}")
    print()
    
    microservices = get_microservices_tags(tenant_name)
    
    if not microservices:
        print(f"❌ Nessun microservizio trovato per il tenant '{tenant_name}'")
        print()
        print("🏢 Tenant disponibili:")
        tenants = list_available_tenants()
        for tenant in tenants:
            print(f"  - {tenant}")
        sys.exit(1)
    
    # Ordina per nome del servizio
    microservices.sort(key=lambda x: x['service'])
    
    # Prepara i dati per la tabella
    table_data = []
    for ms in microservices:
        table_data.append([
            ms['service'],
            ms['uat_tag'],
            ms['prod_tag'],
            ms['status']
        ])
    
    # Stampa la tabella
    headers = ['Microservizio', 'Tag UAT', 'Tag PROD', 'Status']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Statistiche
    total = len(microservices)
    aligned = len([ms for ms in microservices if '✅' in ms['status']])
    uat_newer = len([ms for ms in microservices if '🔼' in ms['status']])
    prod_newer = len([ms for ms in microservices if '🔽' in ms['status']])
    missing = len([ms for ms in microservices if '⚠️' in ms['status']])
    check_needed = len([ms for ms in microservices if '❓' in ms['status']])
    
    print(f"\n📊 Statistiche:")
    print(f"   📦 Totale microservizi: {total}")
    print(f"   ✅ Allineati: {aligned}")
    print(f"   🔼 UAT più recente: {uat_newer}")
    print(f"   🔽 PROD più recente: {prod_newer}")
    print(f"   ⚠️  Config mancanti: {missing}")
    print(f"   ❓ Da verificare manualmente: {check_needed}")
    
    # Suggerimenti
    if uat_newer > 0:
        print(f"\n💡 Suggerimento: Ci sono {uat_newer} microservizi con versioni più recenti in UAT")
        print("   Considera di fare il deploy in PROD se i test sono passati")
    
    if missing > 0:
        print(f"\n⚠️  Attenzione: {missing} microservizi hanno configurazioni mancanti")
        print("   Verifica i file uat-config.yaml e prod-config.yaml")

if __name__ == "__main__":
    main()
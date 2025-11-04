#!/usr/bin/env python3
"""
Script per confrontare i tag dei microservizi di un tenant tra UAT e PROD
Uso: python3 tenant-microservices-tags.py <tenant_name>
"""

import os
import sys
import yaml
import re
from tabulate import tabulate
from pathlib import Path

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
        print(f"Errore nella lettura di {file_path}: {e}")
        return ''

def get_microservices_tags(tenant_name):
    """Ottiene i tag UAT e PROD per tutti i microservizi di un tenant"""
    tenant_path = Path(f"deploy/tenants/{tenant_name}")
    
    if not tenant_path.exists():
        print(f"❌ Tenant '{tenant_name}' non trovato!")
        return []
    
    microservices = []
    
    # Trova tutte le cartelle dei microservizi
    for service_dir in tenant_path.iterdir():
        if service_dir.is_dir() and service_dir.name != 'api-gateway':
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
                    uat_version = [int(x) for x in uat_tag.replace('v', '').split('.')]
                    prod_version = [int(x) for x in prod_tag.replace('v', '').split('.')]
                    
                    if uat_version > prod_version:
                        status = "🔼 UAT più recente"
                    elif uat_version < prod_version:
                        status = "🔽 PROD più recente"
                    else:
                        status = "✅ Allineato"
                except:
                    status = "❓ Da verificare"
            
            microservices.append({
                'service': service_name,
                'uat_tag': uat_tag,
                'prod_tag': prod_tag,
                'status': status
            })
    
    return microservices

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 tenant-microservices-tags.py <tenant_name>")
        print("\nTenant disponibili:")
        tenant_base = Path("deploy/tenants")
        if tenant_base.exists():
            for tenant in sorted(tenant_base.iterdir()):
                if tenant.is_dir():
                    print(f"  - {tenant.name}")
        sys.exit(1)
    
    tenant_name = sys.argv[1]
    
    print(f"🔍 Analizzando microservizi del tenant: {tenant_name}\n")
    
    microservices = get_microservices_tags(tenant_name)
    
    if not microservices:
        print(f"❌ Nessun microservizio trovato per il tenant '{tenant_name}'")
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
    
    print(f"\n📊 Statistiche:")
    print(f"   Totale microservizi: {total}")
    print(f"   Allineati: {aligned}")
    print(f"   UAT più recente: {uat_newer}")
    print(f"   PROD più recente: {prod_newer}")
    print(f"   Config mancanti: {missing}")

if __name__ == "__main__":
    main()
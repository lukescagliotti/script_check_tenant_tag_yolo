#!/bin/bash

# Script bash semplificato per confrontare i tag UAT/PROD di un tenant
# Uso: ./check-tenant-tags.sh <tenant_name>

TENANT_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ -z "$TENANT_NAME" ]; then
    echo "❌ Specificare il nome del tenant"
    echo "Uso: $0 <tenant_name>"
    echo ""
    echo "🏢 Tenant disponibili:"
    ls -1 deploy/tenants/ | grep -v "^\\." | sed 's/^/  - /'
    exit 1
fi

# Verifica se esiste il tenant
if [ ! -d "deploy/tenants/$TENANT_NAME" ]; then
    echo "❌ Tenant '$TENANT_NAME' non trovato!"
    echo ""
    echo "🏢 Tenant disponibili:"
    ls -1 deploy/tenants/ | grep -v "^\\." | sed 's/^/  - /'
    exit 1
fi

echo "🚀 Avvio analisi per il tenant: $TENANT_NAME"
echo ""

# Esegui lo script Python
if [ -f "$VENV_PYTHON" ]; then
    "$VENV_PYTHON" "$SCRIPT_DIR/tenant-microservices-tags.py" "$TENANT_NAME"
else
    python3 "$SCRIPT_DIR/tenant-microservices-tags.py" "$TENANT_NAME"
fi
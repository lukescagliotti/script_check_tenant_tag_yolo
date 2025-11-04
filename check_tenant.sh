#!/bin/bash

# Script bash per avvio rapido del tenant checker
# Uso: ./check_tenant.sh <tenant_name>

TENANT_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Tenant Microservices Tags Checker${NC}"
echo ""

# Controlla se l'ambiente virtuale esiste
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtuale non trovato!${NC}"
    echo "Per configurare l'ambiente:"
    echo "  1. python3 -m venv .venv"
    echo "  2. source .venv/bin/activate"
    echo "  3. pip install pyyaml tabulate"
    echo ""
    exit 1
fi

# Se non è specificato il tenant, mostra l'help
if [ -z "$TENANT_NAME" ]; then
    echo -e "${YELLOW}❌ Specificare il nome del tenant${NC}"
    echo "Uso: $0 <tenant_name>"
    echo ""
    
    # Prova a mostrare i tenant disponibili usando lo script Python
    echo -e "${BLUE}🏢 Per vedere i tenant disponibili:${NC}"
    echo "  $0 --list"
    echo ""
    echo -e "${BLUE}📝 Esempio:${NC}"
    echo "  $0 artbkr"
    exit 1
fi

# Opzione per listare i tenant
if [ "$TENANT_NAME" = "--list" ] || [ "$TENANT_NAME" = "-l" ]; then
    echo -e "${GREEN}📋 Esecuzione lista tenant...${NC}"
    "$VENV_PYTHON" "$SCRIPT_DIR/tenant_checker.py"
    exit 0
fi

echo -e "${GREEN}🔍 Analisi del tenant: $TENANT_NAME${NC}"
echo ""

# Esegui lo script Python
"$VENV_PYTHON" "$SCRIPT_DIR/tenant_checker.py" "$TENANT_NAME"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Analisi completata con successo!${NC}"
else
    echo ""
    echo -e "${RED}❌ Errore durante l'analisi${NC}"
fi

exit $EXIT_CODE
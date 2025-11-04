#!/bin/bash

# Script di setup automatico per Tenant Microservices Tags Checker
# Questo script configura l'ambiente virtuale Python e installa le dipendenze

echo "🚀 Setup Tenant Microservices Tags Checker"
echo "=========================================="
echo ""

# Controlla se Python 3 è disponibile
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato! Installa Python 3 prima di continuare."
    exit 1
fi

echo "✅ Python 3 trovato: $(python3 --version)"

# Crea l'ambiente virtuale se non esiste
if [ ! -d ".venv" ]; then
    echo "📦 Creazione ambiente virtuale..."
    python3 -m venv .venv
    
    if [ $? -eq 0 ]; then
        echo "✅ Ambiente virtuale creato con successo"
    else
        echo "❌ Errore nella creazione dell'ambiente virtuale"
        exit 1
    fi
else
    echo "📦 Ambiente virtuale già esistente"
fi

# Attiva l'ambiente virtuale
echo "🔧 Attivazione ambiente virtuale..."
source .venv/bin/activate

if [ $? -eq 0 ]; then
    echo "✅ Ambiente virtuale attivato"
else
    echo "❌ Errore nell'attivazione dell'ambiente virtuale"
    exit 1
fi

# Aggiorna pip
echo "🔄 Aggiornamento pip..."
pip install --upgrade pip > /dev/null 2>&1

# Installa le dipendenze
echo "📥 Installazione dipendenze..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Dipendenze installate con successo"
    else
        echo "❌ Errore nell'installazione delle dipendenze"
        exit 1
    fi
else
    echo "⚠️  File requirements.txt non trovato, installazione manuale..."
    pip install pyyaml tabulate
fi

# Rendi eseguibili gli script
echo "🔨 Configurazione permessi script..."
chmod +x check_tenant.sh 2>/dev/null
chmod +x tenant_checker.py 2>/dev/null

echo ""
echo "🎉 Setup completato con successo!"
echo ""
echo "📋 Prossimi passi:"
echo "1. Modifica il path della repository nel file tenant_checker.py:"
echo "   REPO_BASE_PATH = '/path/to/your/reusable-pipelines'"
echo ""
echo "2. Oppure usa la variabile d'ambiente:"
echo "   export REPO_PATH='/path/to/your/reusable-pipelines'"
echo ""
echo "3. Testa lo script:"
echo "   ./check_tenant.sh --list"
echo "   ./check_tenant.sh artbkr"
echo ""
echo "📖 Per maggiori informazioni consulta il README.md"
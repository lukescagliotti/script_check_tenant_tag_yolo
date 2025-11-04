# Tenant Microservices Tags Checker

Uno script Python per analizzare e confrontare i tag dei microservizi tra ambiente UAT e PROD per i tenant nelle pipeline GitLab.

## 📋 Funzionalità

- ✅ Confronta i tag delle immagini Docker tra UAT e PROD
- 📊 Mostra statistiche riassuntive
- 🎨 Output formattato con tabelle e colori
- 🔍 Rileva automaticamente differenze di versione
- ⚡ Supporta configurazione dinamica del path repository

## 🛠️ Installazione

### 1. Clona o scarica i file del progetto

```bash
mkdir tenant-checker
cd tenant-checker
# Copia i file tenant_checker.py e setup.py in questa directory
```

### 2. Crea un ambiente virtuale Python

```bash
# Crea l'ambiente virtuale
python3 -m venv .venv

# Attiva l'ambiente virtuale
# Su macOS/Linux:
source .venv/bin/activate

# Su Windows:
# .venv\Scripts\activate
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

Oppure installa manualmente:

```bash
pip install pyyaml tabulate
```

## 🚀 Utilizzo

### Configurazione del path repository

Prima del primo utilizzo, modifica la variabile `REPO_BASE_PATH` nel file `tenant_checker.py`:

```python
# Imposta il path assoluto alla tua repository reusable-pipelines
REPO_BASE_PATH = "/path/to/your/reusable-pipelines"
```

### Comandi di base

```bash
# Attiva l'ambiente virtuale
source .venv/bin/activate

# Visualizza tutti i tenant disponibili
python tenant_checker.py

# Analizza un tenant specifico
python tenant_checker.py artbkr

# Analizza tenant diversi
python tenant_checker.py yolo
python tenant_checker.py italiana
```

### Script bash rapido (opzionale)

Puoi anche usare lo script bash per avvio più veloce:

```bash
# Rendi eseguibile
chmod +x check_tenant.sh

# Usa direttamente
./check_tenant.sh artbkr
```

## 📊 Output di esempio

```
🔍 Analizzando microservizi del tenant: artbkr

+----------------------------------+-------------+-------------+-------------------+
| Microservizio                    | Tag UAT     | Tag PROD    | Status            |
+==================================+=============+=============+===================+
| iad-utility-deploy               | v1.2.48     | v1.2.46     | 🔼 UAT più recente |
| payment-stripe-deploy            | v1.0.170-HF | v1.0.168-HF | 🔼 UAT più recente |
| cms-service-deploy               | v0.0.12     | v0.0.12     | ✅ Allineato       |
+----------------------------------+-------------+-------------+-------------------+

📊 Statistiche:
   Totale microservizi: 38
   Allineati: 32
   UAT più recente: 3
   PROD più recente: 0
   Config mancanti: 0
```

## 🎯 Legenda Status

- ✅ **Allineato**: I tag UAT e PROD sono identici
- 🔼 **UAT più recente**: La versione in UAT è più recente di quella in PROD
- 🔽 **PROD più recente**: La versione in PROD è più recente di quella in UAT  
- ⚠️ **Config mancante**: Manca il file di configurazione UAT o PROD
- ❓ **Da verificare**: I tag hanno formati diversi e richiedono controllo manuale

## 🔧 Configurazione avanzata

### Personalizzazione del path repository

Puoi anche passare il path come variabile d'ambiente:

```bash
export REPO_PATH="/path/to/your/reusable-pipelines"
python tenant_checker.py artbkr
```

### Modifica delle cartelle da escludere

Nel codice puoi modificare la lista dei servizi da escludere:

```python
# Nella funzione get_microservices_tags()
if service_dir.is_dir() and service_dir.name not in ['api-gateway', 'altro-da-escludere']:
```

## 🐛 Troubleshooting

### Errore "Tenant non trovato"
- Verifica che il path `REPO_BASE_PATH` sia corretto
- Controlla che la cartella `deploy/tenants/` esista nella repository

### Errore "ModuleNotFoundError"
- Assicurati di aver attivato l'ambiente virtuale: `source .venv/bin/activate`
- Reinstalla le dipendenze: `pip install -r requirements.txt`

### File YAML corrotti
- Lo script salta automaticamente i file YAML non validi e mostra un messaggio di errore

## 📁 Struttura file del progetto

```
tenant-checker/
├── .venv/                 # Ambiente virtuale Python
├── tenant_checker.py      # Script principale
├── check_tenant.sh        # Script bash di supporto
├── requirements.txt       # Dipendenze Python
└── README.md             # Questa documentazione
```

## 🤝 Contribuire

Per aggiungere nuove funzionalità o correggere bug:

1. Modifica il file `tenant_checker.py`
2. Testa con diversi tenant
3. Aggiorna la documentazione se necessario
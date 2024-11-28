
# Analisi di File EDF con MATLAB e Python

Questo progetto permette di analizzare file EDF utilizzando MATLAB e Python, generando informazioni e nomogrammi relativi ai pazienti.

---

## Prerequisiti

### MATLAB
1. **MATLAB** con **Simulink** installato.
2. **EEGLAB**, installabile tramite gli **Add-On** di MATLAB.

### Python
Assicurati di avere Python installato e installa le seguenti librerie tramite `pip`:

```bash
pip install mne numpy pandas matplotlib matlabengine
```

---

## Modalità di Esecuzione

### 1. Preparazione dei file:
- **Cartella Edf**: Popolare questa cartella con i file **.edf** da analizzare.
- **File CSV associati (opzionale)**:
  - Se necessario, per ciascun file **.edf**, aggiungere un file **.csv** con lo stesso nome (eccetto l'estensione).
  - Creare un file CSV è semplice:
    1. Creare un file di testo semplice (**.txt**).
    2. Cambiare l'estensione in **.csv**.
    3. Inserire la seguente intestazione nella prima riga:
       ```
       start,end
       ```
    4. Inserire nelle righe successive gli intervalli di tempo (in minuti), uno per riga. Esempio:
       ```
       start,end
       10,15
       52,60
       ```

### 2. Esecuzione dello script:
- Dopo aver popolato la cartella `Edf`, eseguire il seguente comando per avviare lo script principale:

```bash
python main.py
```

- Lo script analizzerà automaticamente i file presenti nella cartella.

### 3. Risultati:
- Al termine dell'elaborazione, verrà creata una cartella denominata `Risultati`.
- All'interno di questa cartella saranno presenti:
  - Informazioni sui pazienti.
  - Nomogrammi relativi a ciascun paziente.

---

## Struttura del Progetto

- `Edf/`  
  Contiene i file EDF e i relativi file CSV per l'analisi.

- `Risultati/`  
  Creata automaticamente dopo l'esecuzione dello script, contiene i risultati generati.

- `main.py`  
  Script principale per l'elaborazione dei dati.

---

## Note

- I file EDF e i relativi CSV devono avere esattamente lo stesso nome (esclusa l'estensione).
- I file CSV devono seguire il formato indicato per evitare errori durante l'elaborazione.

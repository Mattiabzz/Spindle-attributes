import mne 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import numpy as np
from datetime import datetime
import matlab.engine
import pandas as pd

dirData = "Edf"
dirRisultati ="Risultati"

c=0
percorsi_cartelle =[]
listaEta = []
listaFileNonUsati = []
listaDate = []
EtaNonValide = []

colors = []  # Lista per memorizzare i colori assegnati ai soggetti

esami_pazienti = {}
colori_pazienti = {}
etichette_pazienti = {}

patient_counter = 1

total_files = len([file for file in os.listdir(dirData) if file.endswith(".edf")])
file_counter = 0

# Crea una colormap
cmap = plt.get_cmap('viridis')

for dirpath, dirnames, filenames in os.walk(dirData):
    # print(f"Directory: {dirpath}")
    for file in filenames:
        if file.endswith('.edf'):  # Controlla se il file ha estensione .edf
            file_path = os.path.join(dirpath, file)
            
            file_counter += 1

            print(f"Processing file {file_counter} di {total_files}")

            print(f"File: {file}")

            raw = mne.io.read_raw_edf(file_path, preload=True)

            # print(f"il file path corrente è -> {file_path}")
                        # Nome del file senza estensione (ignora il case)
            base_name = os.path.splitext(file)[0]
            
            # Cerca un file CSV con lo stesso nome
            csv_file = None
            for f in os.listdir(dirpath):
                if f.lower() == f"{base_name}.csv".lower():
                    csv_file = os.path.join(dirpath, f)
                    break

            if csv_file:
                print(f"Trovato file CSV corrispondente: {csv_file}")
            else:
                print(f"Nessun file CSV trovato per {file_path}")

            if 'subject_info' in raw.info and raw.info['subject_info'] is not None:
                start_time = raw.info['meas_date']
                birthday = raw.info['subject_info'].get('birthday')
                patient_name = (raw.info['subject_info'].get('first_name', 'Unknown') + " " + raw.info['subject_info'].get('last_name', 'Unknown')).upper()

                if birthday is not None and start_time is not None:
                    # Calcola l'età in anni
                    print(f"compleanno ---> {birthday}\ndata di registrazione --->{start_time}")
                    age = (start_time.date() - birthday).days // 365
                    print("Età del paziente al momento della registrazione:", age, "anni")
                    if patient_name not in esami_pazienti:
                        esami_pazienti[patient_name] = []

                    # if all(abs(age - età_registrata) >= 1 for età_registrata in esami_pazienti[patient_name]): #controllo per 

                    esami_pazienti[patient_name].append(age)
                    listaEta.append(age)
                    listaDate.append(start_time.date())


                    nome_cartella = os.path.splitext(os.path.basename(file_path))[0]
                    percorso_cartella = os.path.join(dirRisultati, nome_cartella)

                    # percorsi_cartelle.append(percorso_cartella)
                    percorsi_cartelle.append((percorso_cartella, patient_name))

                    if patient_name not in colori_pazienti:
                        color_index = (patient_counter - 1) / len(esami_pazienti) * 1.5 # Incremento per variazione di colori
                        colori_pazienti[patient_name] = cmap(color_index)

                        # colori_pazienti[patient_name] = cmap(len(colori_pazienti) / max(1, len(filenames)))
                        etichette_pazienti[patient_name] = f"Paziente {patient_counter}"
                        patient_counter += 1

                        # print(patient_name)
                        #lancio dello script matlab
                        eng = matlab.engine.start_matlab()

                        #passaggio delle informazioni
                        eng.workspace['csv_file'] = csv_file if csv_file else ""
                        eng.workspace['input_param'] = file_path

                        #lancio dello script matlab
                        eng.run("mainLiveScript", nargout=0)

                        # Termina la sessione
                        eng.quit()
                    # else:
                    #     print(f"Il paziente '{patient_name}' nel file '{file}' è stato saltato poiché il campo età contiene già il valore {age}.")
                    #     EtaNonValide.append(file)
                else:
                    print("Data di nascita o data di registrazione non disponibile.")
                    c+=1
                    listaFileNonUsati.append(file)
            else:
                print("Informazioni del paziente non disponibili nel file EDF")
                c+=1
                listaFileNonUsati.append(file)

print(f"rilevati {patient_counter - 1} pazienti")

print(f"ci sono {c} file senza attributi\n")

if listaFileNonUsati != []:
    print(f"File non usati per mancanza d'informazioni:\n{listaFileNonUsati}")

if EtaNonValide != []:
    print(f"File non usati poiché il valore del campo età si ripete:\n{EtaNonValide}")    
# ritardi_medi = []

tutti_ritardi = []  # Lista per accumulare tutti i ritardi
eta_ripetuta_ritardi = []

tutti_isi = []
eta_ripetuta_isi = []

tutti_durate = []
eta_ripetuta_durate = []

tutti_tasso = []



for i, (percorso_cartella, patient_name) in enumerate(percorsi_cartelle):
    # print(f"Esplorando la cartella: {percorso_cartella}")
    if os.path.exists(percorso_cartella):
        df = pd.read_csv(percorso_cartella+'/dati_ritardo.csv')
    #   print(df.to_string())
    ###### lettura e preparazione ritardi
    #    # Calcolo della media di "Ritardo(s)" per il grafico
    #    ritardo_medio = df['Ritardo(s)'].mean()
    #    ritardi_medi.append(ritardo_medio)

        # colore_casuale = cmap(i / len(percorsi_cartelle))
        # colors.append(colore_casuale)

        color = colori_pazienti[patient_name]  # Usa il colore assegnato al paziente
        colors.append(color)

        # ritardi = df['Ritardo(s)'].tolist()
        ritardi = df['Ritardo(s)'].mean()
        tutti_ritardi.append(ritardi)


     ###### lettura e preparazione isi
        df = pd.read_csv(percorso_cartella+'/dati_isi.csv')

        # isi = df['isi_min(s)'].tolist()
        isi = df['isi_min(s)'].mean()
        tutti_isi.append(isi)


    ###### lettura e preparazione durate
        df = pd.read_csv(percorso_cartella+'/dati_durate.csv')

        # durata = df['durata(s)'].tolist()
        durata = df['durata(s)'].mean()
        tutti_durate.append(durata)


    ###### lettura e preparazione tasso
        df = pd.read_csv(percorso_cartella+'/dati_tasso.csv')

        tasso = df['Tasso']
        tutti_tasso.append(tasso)


    else:
        print(f"Cartella non trovata: {percorso_cartella}")

# Assegna colori ai pazienti
# for i, patient_name in enumerate(esami_pazienti.keys()):
#     color_index = i / len(esami_pazienti) * 0.9  # Cambia per maggiore varietà
#     colori_pazienti[patient_name] = cmap(color_index)

# Plottare il grafico ritardi
plt.figure(figsize=(10, 6))
etichette_visualizzate = set() 
for i in range(len(tutti_ritardi)):
    # Estrai i ritardi e ripeti l'età per ogni ritardo
    # eta_ripetuta = [listaEta[i]] * len(tutti_ritardi[i])
    eta_ripetuta = listaEta[i]
    patient_name = percorsi_cartelle[i][1]

    label = etichette_pazienti[patient_name] if etichette_pazienti[patient_name] not in etichette_visualizzate else None
    if label:
        etichette_visualizzate.add(etichette_pazienti[patient_name])

    plt.scatter(eta_ripetuta, tutti_ritardi[i], color=colori_pazienti[patient_name], label=label)

plt.xlabel("Età (anni)")
plt.ylabel("Spindle lag (s)")
plt.title("Ritardo in funzione dell'età")
plt.legend()
plt.grid(True)
# plt.show()
plt.savefig(dirRisultati+'/nomogramma_ritardi')
plt.close()

#grafico isi
plt.figure(figsize=(10, 6))
etichette_visualizzate = set() 
for i in range(len(tutti_isi)):
    # Estrai i ritardi e ripeti l'età per ogni ritardo
    # eta_ripetuta = [listaEta[i]] * len(tutti_isi[i])
    eta_ripetuta = listaEta[i]
    patient_name = percorsi_cartelle[i][1]

    label = etichette_pazienti[patient_name] if etichette_pazienti[patient_name] not in etichette_visualizzate else None
    if label:
        etichette_visualizzate.add(etichette_pazienti[patient_name])

    plt.scatter(eta_ripetuta, tutti_isi[i], color=colors[i], label=label)

plt.xlabel("Età (anni)")
plt.ylabel("Minimum isi (s)")
plt.title("Isi in funzione dell'età")
plt.legend()
plt.grid(True)
# plt.show()
plt.savefig(dirRisultati+'/nomogramma_isi')
plt.close()

#grafico durate
plt.figure(figsize=(10, 6))
etichette_visualizzate = set() 
for i in range(len(tutti_durate)):
    # Estrai i ritardi e ripeti l'età per ogni ritardo
    # eta_ripetuta = [listaEta[i]] * len(tutti_durate[i])

    eta_ripetuta = listaEta[i]
    patient_name = percorsi_cartelle[i][1]

    label = etichette_pazienti[patient_name] if etichette_pazienti[patient_name] not in etichette_visualizzate else None
    if label:
        etichette_visualizzate.add(etichette_pazienti[patient_name])

    plt.scatter(eta_ripetuta, tutti_durate[i], color=colors[i], label=label)

plt.xlabel("Età (anni)")
plt.ylabel("Spindle duration(s)")
plt.title("Durate spindle in funzione dell'età")
plt.legend()
plt.grid(True)
# plt.show()
plt.savefig(dirRisultati+'/nomogramma_durate')
plt.close()

#grafico tasso
plt.figure(figsize=(10, 6))
etichette_visualizzate = set() 
for i in range(len(tutti_tasso)):
    # Estrai i ritardi e ripeti l'età per ogni ritardo
    # eta_ripetuta = [listaEta[i]] * len(tutti_tasso[i])

    eta_ripetuta = listaEta[i]
    patient_name = percorsi_cartelle[i][1]

    label = etichette_pazienti[patient_name] if etichette_pazienti[patient_name] not in etichette_visualizzate else None
    if label:
        etichette_visualizzate.add(etichette_pazienti[patient_name])

    plt.scatter(eta_ripetuta, tutti_tasso[i], color=colors[i], label=label)

plt.xlabel("Età (anni)")
plt.ylabel("Spindle rate (#/min)")
plt.title("Risultati tasso")
plt.legend()
plt.grid(True)
# plt.show()
plt.savefig(dirRisultati+'/nomogramma_tasso')
plt.close()
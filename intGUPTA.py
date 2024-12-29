import streamlit as st
import numpy as np

def heuristique_gupta(matrice_temps):
    num_taches = len(matrice_temps)
    num_machines = len(matrice_temps[0])
    e = [1 if matrice_temps[i][0] < matrice_temps[i][-1] else -1 for i in range(num_taches)]
    s = []

    for i in range(num_taches):
        ratios = [e[i] / (matrice_temps[i][k] + matrice_temps[i][k + 1]) for k in range(num_machines - 1)]
        s.append((i, min(ratios)))

    # Trier les tâches par l'indice s dans l'ordre décroissant
    s.sort(key=lambda x: x[1], reverse=True)
    # Extraire les indices des tâches triées
    sequence_optimale = [x[0] for x in s]
    
    return sequence_optimale

def calculer_cmax(matrice_temps, sequence_optimale):
    temps_machines = [0] * len(matrice_temps[0])
    temps_debut = [0] * len(matrice_temps)
    for tache in sequence_optimale:
        temps_debut[tache] = temps_machines[0] + matrice_temps[tache][0]
        temps_machines[0] = temps_debut[tache]
        for machine in range(1, len(matrice_temps[tache])):
            temps_debut[tache] = max(temps_machines[machine], temps_debut[tache]) + matrice_temps[tache][machine]
            temps_machines[machine] = temps_debut[tache]
    return max(temps_machines)

# Interface Streamlit
st.title("Heuristique de Gupta pour Flow Shop")

# Entrée du nombre de tâches et de machines
num_taches = st.number_input("Nombre de tâches :", min_value=1, step=1)
num_machines = st.number_input("Nombre de machines :", min_value=1, step=1)

# Entrée de la matrice des temps de traitement
matrice_input = st.text_area("Saisissez la matrice des temps de traitement : chaque ligne représente une tâche, avec les temps séparés par des espaces.")

if matrice_input:
    try:
        matrice_temps = [list(map(int, line.split())) for line in matrice_input.splitlines()]
        if len(matrice_temps) != num_taches or any(len(row) != num_machines for row in matrice_temps):
            st.error(f"La matrice doit contenir {num_taches} lignes et chaque ligne doit avoir {num_machines} colonnes.")
        else:
            # Appliquer l'heuristique de Gupta
            sequence_optimale = heuristique_gupta(matrice_temps)
            cmax = calculer_cmax(matrice_temps, sequence_optimale)

            # Afficher les résultats
            sequence_optimale_noms = [f'Tâche {i+1}' for i in sequence_optimale]
            st.subheader("Résultats")
            st.write("Séquence optimale :", " → ".join(sequence_optimale_noms))
            st.write("Makespan (Cmax) optimal :", cmax)

            # Afficher la matrice de temps pour plus de clarté
            st.subheader("Matrice des temps de traitement")
            st.write(np.array(matrice_temps))
    except ValueError:
        st.error("Assurez-vous que toutes les valeurs de la matrice sont des entiers et bien formatées.")

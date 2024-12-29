import streamlit as st

def johnsons_algorithm(tasks):
    set_X = [task for task in tasks if task[1] <= task[2]]
    set_Y = [task for task in tasks if task[1] > task[2]]
    set_X.sort(key=lambda x: x[1])
    set_Y.sort(key=lambda x: x[2], reverse=True)
    return set_X + set_Y

def calculer_cmax(taches, sequence_optimale, m):
    temps_machines = [0] * m
    cmax = 0
    for index in sequence_optimale:
        tache = taches[index]
        temps_m1 = temps_machines[0] + tache[0]
        temps_machines[0] = temps_m1
        for j in range(1, m):
            temps_m1 = max(temps_m1, temps_machines[j]) + tache[j]
            temps_machines[j] = temps_m1
        cmax = max(cmax, temps_m1)
    return cmax

# Streamlit interface
st.title("Heuristique CDS pour Ordonnancement")

# Demander le nombre de tâches et de machines
num_tasks = st.number_input("Entrez le nombre de tâches :", min_value=1, step=1)
num_machines = st.number_input("Entrez le nombre de machines :", min_value=2, step=1)

# Saisie des temps de traitement pour chaque tâche
matrice_temps = []
for i in range(num_tasks):
    times = st.text_input(f"Entrez les temps de traitement pour la tâche {i+1} (séparés par un espace) :")
    if times:
        matrice_temps.append([int(time) for time in times.split()])

# Appliquer l'heuristique CDS
best_sequence = None
best_cmax = float('inf')
results = []

if st.button("Calculer la séquence optimale"):
    for k in range(1, num_machines):
        # Créer les pseudo-tâches
        pseudo_tasks = []
        for i, task in enumerate(matrice_temps):
            p1 = sum(task[:k])
            p2 = sum(task[-(num_machines-k):])
            pseudo_tasks.append((i, p1, p2))

        # Appliquer l'algorithme de Johnson
        current_sequence = johnsons_algorithm(pseudo_tasks)
        task_indices = [t[0] for t in current_sequence]
        current_cmax = calculer_cmax(matrice_temps, task_indices, num_machines)

        # Enregistrer les résultats pour chaque k
        best_sequence_readable = [f"Tache{t+1}" for t in task_indices]
        results.append((k, best_sequence_readable, current_cmax))

        if current_cmax < best_cmax:
            best_cmax = current_cmax
            best_sequence = task_indices

    # Afficher les résultats pour chaque k
    for k, seq, cmax in results:
        st.subheader(f"Pour k={k}:")
        st.write(f"Séquence : {seq}")
        st.write(f"Cmax (makespan) : {cmax}")

    # Afficher la meilleure séquence
    best_sequence_readable = [f"Tache{t+1}" for t in best_sequence]
    st.subheader("Meilleure séquence :")
    st.write(best_sequence_readable)
    st.write(f"Cmax (makespan) optimal : {best_cmax}")

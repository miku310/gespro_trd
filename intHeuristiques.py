import streamlit as st
import numpy as np

# Heuristique H1
def heuristic_h1(cost_matrix, duration_matrix, available_times):
    cost_matrix = np.array(cost_matrix, dtype=float)
    duration_matrix = np.array(duration_matrix, dtype=float)
    available_times = np.array(available_times, dtype=float)

    tasks = set(range(cost_matrix.shape[1]))
    assignment = []
    total_cost = 0

    while tasks:
        min_found = False
        for _ in range(cost_matrix.size):
            min_value = np.inf
            chosen_task = None
            chosen_machine = None

            for i in range(cost_matrix.shape[0]):
                for j in tasks:
                    if cost_matrix[i, j] < min_value and duration_matrix[i, j] <= available_times[i]:
                        min_value = cost_matrix[i, j]
                        chosen_machine = i
                        chosen_task = j

            if chosen_task is not None:
                assignment.append((chosen_task + 1, chosen_machine + 1))
                available_times[chosen_machine] -= duration_matrix[chosen_machine, chosen_task]
                total_cost += cost_matrix[chosen_machine, chosen_task]
                tasks.remove(chosen_task)
                min_found = True
                break

        if not min_found:
            break

    return assignment, available_times, total_cost

# Heuristique H2
def heuristic_h2(cost_matrix, duration_matrix, available_times):
    cost_matrix = np.array(cost_matrix, dtype=float)
    duration_matrix = np.array(duration_matrix, dtype=float)
    available_times = np.array(available_times, dtype=float)

    tasks = set(range(cost_matrix.shape[1]))
    assignment = []
    total_cost = 0

    while tasks:
        min_found = False
        for _ in range(duration_matrix.size):
            min_value = np.inf
            chosen_task = None
            chosen_machine = None

            for i in range(duration_matrix.shape[0]):
                for j in tasks:
                    if duration_matrix[i, j] < min_value and duration_matrix[i, j] <= available_times[i]:
                        min_value = duration_matrix[i, j]
                        chosen_machine = i
                        chosen_task = j

            if chosen_task is not None:
                assignment.append((chosen_task + 1, chosen_machine + 1))
                available_times[chosen_machine] -= duration_matrix[chosen_machine, chosen_task]
                total_cost += cost_matrix[chosen_machine, chosen_task]
                tasks.remove(chosen_task)
                min_found = True
                break

        if not min_found:
            break

    return assignment, available_times, total_cost

# Interface Streamlit
st.title("Interface pour les Heuristiques H1 et H2")
st.header("Paramètres d'entrée")

rows = st.number_input("Nombre de machines", min_value=1, value=3, step=1)
cols = st.number_input("Nombre de tâches", min_value=1, value=5, step=1)

st.write("Matricule des coûts (Cij)")
cost_matrix = []
for i in range(int(rows)):
    row = st.text_input(f"Ligne {i + 1} (séparée par des virgules)", value="9,8,6,4,6", key=f"cost_matrix_{i}")
    cost_matrix.append(list(map(float, row.split(','))))

st.write("Matricule des durées (Pij)")
duration_matrix = []
for i in range(int(rows)):
    row = st.text_input(f"Ligne {i + 1} (séparée par des virgules)", value="9,8,6,4,6", key=f"duration_matrix_{i}")
    duration_matrix.append(list(map(float, row.split(','))))

available_times = st.text_input("Temps disponibles pour chaque machine (t_i, séparés par des virgules)", value="18,17,14", key="available_times")
available_times = list(map(float, available_times.split(',')))

# Choisir l'heuristique
heuristic_choice = st.selectbox("Choisissez une heuristique :", ["H1 - Basée sur les coûts", "H2 - Basée sur les durées"], key="heuristic_choice")

# Exécuter l'heuristique
if st.button("Exécuter", key="execute_button"):
    if heuristic_choice == "H1 - Basée sur les coûts":
        assignment, remaining_times, total_cost = heuristic_h1(cost_matrix, duration_matrix, available_times)
    else:
        assignment, remaining_times, total_cost = heuristic_h2(cost_matrix, duration_matrix, available_times)

    st.subheader("Résultats")
    st.write("**Tâches assignées :**")
    for task, machine in assignment:
        st.write(f"- La tâche {task} est assignée à la machine {machine}")

    st.write("**Temps restants pour chaque machine :**")
    for i, time in enumerate(remaining_times, start=1):
        st.write(f"- Machine {i} : {time} unités de temps restantes")

    st.write("**Coût total :**", total_cost)

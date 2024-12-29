import streamlit as st

class Task:
    def __init__(self, task_id, pi1, pi2):
        self.id = task_id
        self.pi1 = pi1
        self.pi2 = pi2

def johnson_algorithm(tasks):
    X = []   # Tâches où pi1 <= pi2
    TX = []  # Tâches où pi1 > pi2

    # Séparation des tâches dans X et TX
    for task in tasks:
        if task.pi1 <= task.pi2:
            X.append(task)
        else:
            TX.append(task)

    # Tri de X par pi1 croissant
    X.sort(key=lambda t: t.pi1)

    # Tri de TX par pi2 décroissant
    TX.sort(key=lambda t: t.pi2, reverse=True)

    # Récupérer l'ordonnancement final
    schedule = [task.id for task in X] + [task.id for task in TX]
    return schedule

def calculate_cmax(tasks, ordonnancement):
    n = len(ordonnancement)
    C1 = [0] * n  # Temps de complétion sur machine 1
    C2 = [0] * n  # Temps de complétion sur machine 2

    # Calcul des temps de complétion sur les deux machines
    for i in range(n):
        task_id = ordonnancement[i] - 1  # Obtenir l'indice de la tâche

        # Complétion sur machine 1
        C1[i] = tasks[task_id].pi1 if i == 0 else C1[i - 1] + tasks[task_id].pi1

        # Complétion sur machine 2
        C2[i] = (
            C1[i] + tasks[task_id].pi2 if i == 0
            else max(C1[i], C2[i - 1]) + tasks[task_id].pi2
        )

    # Le Cmax est le dernier temps de complétion sur machine 2
    return C2[-1]

# Interface Streamlit
def app():
    st.title("Algorithme de Johnson et Calcul du Cmax")

    # Entrée des tâches
    st.subheader("Entrez les informations des tâches")

    num_tasks = st.number_input("Nombre de tâches", min_value=1, max_value=20, value=5)
    
    tasks = []
    for i in range(num_tasks):
        task_id = i + 1
        pi1 = st.number_input(f"Durée de la tâche {task_id} sur la machine 1", value=3)
        pi2 = st.number_input(f"Durée de la tâche {task_id} sur la machine 2", value=3)
        tasks.append(Task(task_id, pi1, pi2))

    if st.button("Calculer l'ordonnancement et Cmax"):
        ordonnancement = johnson_algorithm(tasks)

        st.subheader("Ordonnancement optimal")
        st.write(ordonnancement)

        # Calculer le Cmax
        Cmax = calculate_cmax(tasks, ordonnancement)
        st.subheader("Cmax optimal")
        st.write(Cmax)

# Lancer l'application Streamlit
if __name__ == "__main__":
    app()

import streamlit as st

class Task:
    def __init__(self, id, timeM1, timeM2, gamme):
        self.id = id
        self.timeM1 = timeM1
        self.timeM2 = timeM2
        self.gamme = gamme

# Fonction pour partitionner les tâches
def partitionTasks(tasks):
    O1, O2, O12, O21 = [], [], [], []
    for task in tasks:
        if task.timeM1 > 0 and task.timeM2 == 0:
            O1.append(task)
        elif task.timeM1 == 0 and task.timeM2 > 0:
            O2.append(task)
        elif task.timeM1 > 0 and task.timeM2 > 0:
            if task.gamme == "M1->M2":
                O12.append(task)
            elif task.gamme == "M2->M1":
                O21.append(task)
    return O1, O2, O12, O21

# Fonction pour appliquer l'algorithme de Johnson
def johnsonAlgorithm(tasks, isO21=False):
    X, T_X = [], []
    for task in tasks:
        if isO21:
            if task.timeM2 <= task.timeM1:
                X.append(task)
            else:
                T_X.append(task)
        else:
            if task.timeM1 <= task.timeM2:
                X.append(task)
            else:
                T_X.append(task)

    X.sort(key=lambda task: task.timeM1)
    T_X.sort(key=lambda task: task.timeM1, reverse=True)

    return X + T_X

# Fonction pour calculer Cmax
def calculateCmax(scheduleM1, scheduleM2):
    currentTimeM1, currentTimeM2 = 0, 0
    for task in scheduleM1:
        currentTimeM1 += task.timeM1
    for task in scheduleM2:
        currentTimeM2 += task.timeM2
    return max(currentTimeM1, currentTimeM2)

# Interface principale Streamlit
def main():
    st.title("Ordonnancement Flow Shop à 2 machines")

    # Étape 1 : Entrer le nombre total de tâches
    total_tasks = st.number_input("Entrez le nombre total de tâches :", min_value=1, value=5, step=1)

    # Initialiser les tâches
    if "tasks" not in st.session_state or len(st.session_state["tasks"]) != total_tasks:
        st.session_state["tasks"] = [Task(i + 1, 0, 0, "M1->M2") for i in range(total_tasks)]

    # Étape 2 : Entrer les données pour chaque tâche
    st.subheader("Entrez les données pour chaque tâche")
    for task in st.session_state["tasks"]:
        st.write(f"### Tâche {task.id}")
        task.timeM1 = st.number_input(f"Temps sur M1 pour Tâche {task.id} (≥ 0)", min_value=0, value=task.timeM1, key=f"timeM1_{task.id}")
        task.timeM2 = st.number_input(f"Temps sur M2 pour Tâche {task.id} (≥ 0)", min_value=0, value=task.timeM2, key=f"timeM2_{task.id}")
        task.gamme = st.selectbox(f"Gamme pour Tâche {task.id}", ["M1->M2", "M2->M1", "M1", "M2"], index=["M1->M2", "M2->M1", "M1", "M2"].index(task.gamme), key=f"gamme_{task.id}")

    # Étape 3 : Calculer l'ordonnancement et Cmax
    if st.button("Calculer l'ordonnancement"):
        st.subheader("Résultats")

        # Partitionner les tâches
        O1, O2, O12, O21 = partitionTasks(st.session_state["tasks"])

        # Appliquer l'algorithme de Johnson
        orderedO12 = johnsonAlgorithm(O12)
        orderedO21 = johnsonAlgorithm(O21, True)

        # Combiner les ordonnancements
        scheduleM1 = orderedO12 + O1 + orderedO21
        scheduleM2 = orderedO21 + O2 + orderedO12

        # Afficher les ordonnancements
        st.write("Ordonnancement sur M1 :", [f"T{task.id}" for task in scheduleM1])
        st.write("Ordonnancement sur M2 :", [f"T{task.id}" for task in scheduleM2])

        # Calculer et afficher Cmax
        cmax = calculateCmax(scheduleM1, scheduleM2)
        st.write(f"Cmax : {cmax}")

if __name__ == "__main__":
    main()

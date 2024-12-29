import streamlit as st

def neh_heuristique(matrice_temps):
    num_taches = len(matrice_temps)
    # Calculer la somme des temps de traitement sur toutes les machines pour chaque tâche
    somme_temps = [sum(tache) for tache in matrice_temps]
    # Trier les tâches par la somme des temps de traitement en ordre décroissant
    taches_triees = sorted(range(num_taches), key=lambda i: somme_temps[i], reverse=True)
    sequence = [taches_triees.pop(0)]  # Commencer avec la tâche ayant le plus grand temps total

    # Ajouter chaque tâche dans la meilleure position
    for tache in taches_triees:
        best_cmax = float('inf')
        best_position = 0
        # Essayer d'insérer la tâche à chaque position possible et trouver le meilleur Cmax
        for position in range(len(sequence) + 1):
            nouvelle_sequence = sequence[:position] + [tache] + sequence[position:]
            cmax = calculer_cmax(matrice_temps, nouvelle_sequence)
            if cmax < best_cmax:
                best_cmax = cmax
                best_position = position
        sequence.insert(best_position, tache)
    return sequence, best_cmax

def calculer_cmax(matrice_temps, sequence):
    num_machines = len(matrice_temps[0])
    temps_fin = [0] * num_machines
    for tache in sequence:
        temps_debut = temps_fin[0] + matrice_temps[tache][0]
        temps_fin[0] = temps_debut
        for machine in range(1, num_machines):
            temps_debut = max(temps_fin[machine], temps_debut) + matrice_temps[tache][machine]
            temps_fin[machine] = temps_debut
    return temps_fin[-1]

# Interface Streamlit
def app():
    st.title("Heuristique NEH pour l'ordonnancement de tâches")

    # Entrée des tâches et des machines
    st.subheader("Entrez les informations des tâches et des machines")

    num_taches = st.number_input("Nombre de tâches", min_value=1, max_value=20, value=5)
    num_machines = st.number_input("Nombre de machines", min_value=2, max_value=10, value=3)

    matrice_temps = []
    for i in range(num_taches):
        temps = []
        for j in range(num_machines):
            t = st.number_input(f"Temps de la tâche {i+1} sur la machine {j+1}", value=3)
            temps.append(t)
        matrice_temps.append(temps)

    if st.button("Calculer la séquence optimale et Cmax"):
        # Appliquer l'heuristique NEH
        sequence_optimale, cmax = neh_heuristique(matrice_temps)

        # Afficher la séquence optimale et le Cmax
        sequence_optimale_noms = [f"Tâche {i+1}" for i in sequence_optimale]
        st.subheader("La séquence optimale est :")
        st.write(sequence_optimale_noms)
        st.subheader("Le Cmax (makespan) optimal est :")
        st.write(cmax)

# Lancer l'application Streamlit
if __name__ == "__main__":
    app()

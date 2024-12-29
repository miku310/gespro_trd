import streamlit as st

# Fonction pour trouver la tâche la plus longue pour l'autre machine
def LTache(machine_actuelle, taches):
    if machine_actuelle == 'M1':
        return max(taches, key=lambda t: taches[t]['p2'])
    else:
        return max(taches, key=lambda t: taches[t]['p1'])

# Fonction pour calculer le Cmax
def calculer_cmax(sequence_M1, taches):
    return sum(taches[tache]['p1'] for tache in sequence_M1)

# Interface Streamlit
def main():
    st.title("Méthode LAPT")
    
    # Entrer le nombre de tâches
    nombre_taches = st.number_input("Nombre de tâches", min_value=1, step=1, format="%d")
    
    taches = {}
    if "saisie_terminee" not in st.session_state:
        st.session_state.saisie_terminee = False
    
    # Saisie des tâches
    if not st.session_state.saisie_terminee:
        for i in range(1, nombre_taches + 1):
            tache_id = "T" + str(i)
            with st.expander(f"Tâche {tache_id}"):
                temps_M1 = st.number_input(f"Temps sur M1 pour {tache_id}", min_value=0, step=1, format="%d", key=f"{tache_id}_M1")
                temps_M2 = st.number_input(f"Temps sur M2 pour {tache_id}", min_value=0, step=1, format="%d", key=f"{tache_id}_M2")
                if temps_M1 > 0 or temps_M2 > 0:
                    taches[tache_id] = {"p1": temps_M1, "p2": temps_M2}
        
        if st.button("Terminer la saisie des tâches"):
            st.session_state.saisie_terminee = True

    # Calculer les séquences et le Cmax
    if st.session_state.saisie_terminee:
        if taches:
            # Algorithme de planification
            copie_taches = taches.copy()
            taches_M1 = []
            taches_M2 = []
            temps_M1 = 0
            temps_M2 = 0

            while copie_taches:
                if temps_M1 <= temps_M2:
                    tache = LTache('M1', copie_taches)
                    taches_M1.append(tache)
                    temps_M1 += copie_taches[tache]['p1']
                else:
                    tache = LTache('M2', copie_taches)
                    taches_M2.append(tache)
                    temps_M2 += copie_taches[tache]['p2']

                del copie_taches[tache]

            # Construire les séquences finales pour M1 et M2
            sequence_M1 = taches_M1 + taches_M2
            sequence_M2 = taches_M2 + taches_M1

            # Calculer Cmax
            cmax = calculer_cmax(sequence_M1, taches)

            # Afficher les résultats
            st.subheader("Résultats")
            st.write("Séquence M1 :", " → ".join(sequence_M1))
            st.write("Séquence M2 :", " → ".join(sequence_M2))
            st.write(f"Cmax : {cmax}")
        else:
            st.error("Aucune tâche saisie.")

        if st.button("Réinitialiser"):
            st.session_state.saisie_terminee = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()

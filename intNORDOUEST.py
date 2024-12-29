import streamlit as st

def methode_coin_superieur_gauche(offres, demandes, couts):
    # Initialiser la matrice des coûts et le coût total à zéro
    matrice_couts = [[0 for j in range(len(demandes))] for i in range(len(offres))]
    cout_total = 0

    i = j = 0

    while i < len(offres) and j < len(demandes):
        # Trouver la quantité à transporter
        quantite_min = min(offres[i], demandes[j])
        matrice_couts[i][j] = quantite_min
        offres[i] -= quantite_min
        demandes[j] -= quantite_min

        # Calculer le coût pour cette allocation et l'ajouter au coût total
        cout_total += matrice_couts[i][j] * couts[i][j]

        # Mettre à jour les indices pour la prochaine itération
        if offres[i] == 0 and i < len(offres):
            i += 1
        if demandes[j] == 0 and j < len(demandes):
            j += 1

    return matrice_couts, cout_total

def afficher_matrice(matrice):
    return "\n".join(["\t".join(map(str, ligne)) for ligne in matrice])

st.title("Méthode du Coin Supérieur Gauche")

# Saisie des dimensions
n = st.number_input("Nombre de sources (n)", min_value=1, value=3, step=1)
m = st.number_input("Nombre de destinations (m)", min_value=1, value=4, step=1)

# Dynamiquement générer les champs pour la matrice des coûts
st.subheader("Matrice des coûts")
couts = []
for i in range(int(n)):
    row = st.text_input(f"Ligne {i + 1} (séparer les valeurs par des espaces)", key=f"row_{i}")
    if row:  # Vérifier si la ligne est saisie avant de l'ajouter
        try:
            row_values = list(map(int, row.split()))
            if len(row_values) != m:
                st.error(f"La ligne {i + 1} doit contenir exactement {m} valeurs.")
            else:
                couts.append(row_values)
        except ValueError:
            st.error(f"La ligne {i + 1} contient des valeurs invalides.")

# Offres
offres_input = st.text_input("Offres (séparer les valeurs par des espaces)")
offres = []
if offres_input:
    try:
        offres = list(map(int, offres_input.split()))
        if len(offres) != n:
            st.error("Le nombre d'offres doit correspondre au nombre de sources.")
    except ValueError:
        st.error("Les offres doivent être des entiers séparés par des espaces.")

# Demandes
demandes_input = st.text_input("Demandes (séparer les valeurs par des espaces)")
demandes = []
if demandes_input:
    try:
        demandes = list(map(int, demandes_input.split()))
        if len(demandes) != m:
            st.error("Le nombre de demandes doit correspondre au nombre de destinations.")
    except ValueError:
        st.error("Les demandes doivent être des entiers séparés par des espaces.")

# Calculer et afficher les résultats
if st.button("Exécuter la méthode"):
    if len(offres) == n and len(demandes) == m and len(couts) == n:
        matrice_couts, cout_total = methode_coin_superieur_gauche(offres, demandes, couts)
        st.subheader("Résultats")
        st.text(f"Matrice des coûts alloués :\n{afficher_matrice(matrice_couts)}")
        st.text(f"Coût total : {cout_total}")
    else:
        st.error("Veuillez vérifier vos entrées pour les offres, les demandes et la matrice des coûts.")
